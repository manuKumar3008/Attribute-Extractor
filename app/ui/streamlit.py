import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.services.pipeline import run_query
from app.core.validation import validate_output

st.set_page_config(page_title="DocBot", page_icon="📄")

# --- Custom styling (simplified) ---
st.markdown("""<style>body { background-color: #eaf4fb; }</style>""", unsafe_allow_html=True)

st.title("📄 DocBot - Document Attribute Extractor")

# --- Session state initialization ---
if "messages" not in st.session_state: st.session_state.messages = []
if "query_done" not in st.session_state: st.session_state.query_done = False
if "result" not in st.session_state: st.session_state.result = {}
if "follow_ups" not in st.session_state: st.session_state.follow_ups = []
if "current_question" not in st.session_state: st.session_state.current_question = None
if "errors" not in st.session_state: st.session_state.errors = []
if "next_field" not in st.session_state: st.session_state.next_field = None

# --- Display previous messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User input ---
user_input = st.chat_input("Ask me about a document...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- First-time query ---
    if not st.session_state.query_done:
        result, errors, follow_ups, next_field = run_query(user_input)

        st.session_state.result = result
        st.session_state.errors = errors
        st.session_state.follow_ups = follow_ups
        st.session_state.next_field = next_field
        st.session_state.query_done = True
        st.session_state.current_question = follow_ups[0] if follow_ups else None

        response = "Here's what I found:\n"
        for k, v in result.items():
            response += f"- **{k}**: {v}\n"

        if follow_ups:
            response += f"\nI need a bit more info:\n{st.session_state.current_question}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

    # --- Follow-up input processing ---
    elif st.session_state.current_question:
        q = st.session_state.current_question.lower()
        val = user_input.strip()

        # Map follow-up input to field
        if "first name" in q: st.session_state.result["firstname"] = val
        elif "last name" in q: st.session_state.result["lastname"] = val
        elif "start date" in q: st.session_state.result["start_date"] = val
        elif "end date" in q: st.session_state.result["end_date"] = val
        elif "year" in q: st.session_state.result["year"] = val
        elif "amount" in q: st.session_state.result["amount"] = val
        elif "currency" in q: st.session_state.result["currency"] = val
        elif "document id" in q: st.session_state.result["document_id"] = val
        elif "document type" in q:st.session_state.result["document_type"] = val

        # Re-validate
        st.session_state.errors = validate_output(st.session_state.result)

        # Recalculate follow-ups
        new_follow_ups = []
        result = st.session_state.result
        errors = st.session_state.errors

        if result["firstname"] == "not mentioned" or "First name must be alphabetic." in errors:
            new_follow_ups.append("🧑 What is the first name?")
        if result["lastname"] == "not mentioned" or "Last name must be alphabetic." in errors:
            new_follow_ups.append("🧑 What is the last name?")
        if result["start_date"] == "not mentioned":
            new_follow_ups.append("📅 What is the start date of the document? (DD-MM-YYYY)")
        if result["end_date"] == "not mentioned":
            new_follow_ups.append("📅 What is the end date of the document? (DD-MM-YYYY)")
        if result["year"] == "not mentioned":
            new_follow_ups.append("📆 Which year is relevant to this document?")
        if result["amount"] == "not mentioned" or "Amount must be numeric." in errors:
            new_follow_ups.append("💰 What is the amount?")
        if result["currency"] == "not mentioned" or "Currency must be 3-letter ISO code." in errors:
            new_follow_ups.append("💱 What is the currency (3-letter code)?")
        if result["document_id"] == "not mentioned" or "Document ID must be exactly 6 alphanumeric characters." in errors:
            new_follow_ups.append("🆔 What is the correct Document ID? (6 alphanumeric characters)")
        

        st.session_state.follow_ups = [f for f in new_follow_ups if f != st.session_state.current_question]
        st.session_state.current_question = st.session_state.follow_ups[0] if st.session_state.follow_ups else None

        response = "✅ Updated. Here's what I have now:\n"
        for k, v in result.items():
            response += f"- **{k}**: {v}\n"

        if st.session_state.current_question:
            response += f"\n📝 {st.session_state.current_question}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# --- Final Output ---
if st.session_state.query_done and not st.session_state.follow_ups:
    with st.expander("✅ Final Document Summary", expanded=True):
        st.json(st.session_state.result)
        if st.session_state.errors:
            st.warning("⚠️ Errors:")
            for err in st.session_state.errors:
                st.write("- " + err)

    if st.button("🔄 Reset"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
