import subprocess
import sys
import os
import threading
import time

def run_ui():
    streamlit_file = os.path.abspath("D:/python/ollama/doc_extractor_Dspy/app/ui/streamlit.py")
    print(f"🔍 Checking for Streamlit file at: {streamlit_file}")

    # Wait briefly if file system is slow
    for _ in range(5):
        if os.path.exists(streamlit_file):
            break
        print("⏳ Waiting for streamlit.py to appear...")
        time.sleep(1)
    else:
        raise FileNotFoundError(f"❌ Streamlit file not found at expected location:\n{streamlit_file}")

    print("✅ Launching Streamlit UI...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_file])

def run_api():
    print("🚀 Launching API with Uvicorn...")
    subprocess.run(["uvicorn", "app.api.api:app", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    threading.Thread(target=run_ui).start()
    threading.Thread(target=run_api).start()
