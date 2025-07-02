import streamlit as st
import sys, os
import json

# Add app directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.services.pipeline import run_query
from app.core.validation_dspy import DSPyValidationModule

st.set_page_config(page_title="📄 Intelligent Document Assistant", page_icon="🤖")
st.title("📄 Intelligent Document Assistant")

# 🔧 Optional Debug Toggle
debug = st.sidebar.checkbox("🧪 Show Debug Info")

# 🧠 Initialize session state
for key in ["history", "result", "errors", "follow_ups", "next_field_to_ask", "final_json"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "history" else None

# 💬 Render history
for u, a in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(u)
    with st.chat_message("assistant"):
        st.markdown(a)

# ✍️ User input + processing
if user_input := st.chat_input("Ask something about your document..."):
    with st.chat_message("user"):
        st.markdown(user_input)

    result, errors, follow_ups, next_field, final_json = run_query(
        user_query=user_input,
        existing_data=st.session_state.result or {},
        field_being_asked=st.session_state.next_field_to_ask,
    )

    st.session_state.update(
        result=result,
        errors=errors,
        follow_ups=follow_ups,
        next_field_to_ask=next_field,
        final_json=final_json
    )

    # 🧾 Build assistant response
    assistant_msg = "### ✅ Extracted Fields\n"
    for k, v in result.items():
        val = str(v).strip()
        if "not mentioned" in val.lower() or "none" in val.lower():
            val = "not mentioned"
        assistant_msg += f"- **{k}**: {val}\n"

    if errors:
        assistant_msg += "\n### ⚠️ Validation Warnings\n"
        for e in errors:
            assistant_msg += f"- `{e}` is missing or invalid\n"

    if follow_ups:
        assistant_msg += "\n### 💬 Suggested Follow-Up\n"
        for q in follow_ups:
            assistant_msg += f"- {q}\n"

    if final_json:
        assistant_msg += "\n### 📦 Final Structured Output\n"
        assistant_msg += "All fields are complete. Here's your document payload:"

    with st.chat_message("assistant"):
        st.markdown(assistant_msg)

        if final_json:
            st.json(final_json)

    st.session_state.history.append((user_input, assistant_msg))

    # 🐞 Optional debug info
    if debug:
        with st.expander("🧪 Debug Logs"):
            st.json({
                "result": result,
                "errors": errors,
                "follow_ups": follow_ups,
                "next_field": next_field,
                "final_json": final_json
            })

# 🔁 Manual re-validation
if st.button("🔁 Re-Validate Fields"):
    st.session_state.errors = DSPyValidationModule().forward(st.session_state.result)
    st.success("Validation updated — ask for any missing field.")