import subprocess
import time
import os
import sys
import signal

def run_app():
    # Get absolute path to project root
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 Starting Japanese Learning Web App...")
    
    # 1. Start Backend (Uvicorn)
    print("🔹 Launching Backend (FastAPI)...")
    backend_cmd = [
        sys.executable, "-m", "uvicorn", 
        "web_app.backend.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000",
        "--reload"
    ]
    backend_process = subprocess.Popen(backend_cmd, cwd=ROOT_DIR)
    
    # Wait for backend to be ready (naive wait)
    time.sleep(3)
    
    # 2. Start Frontend (Streamlit)
    print("🔹 Launching Frontend (Streamlit)...")
    frontend_cmd = [
        sys.executable, "-m", "streamlit", 
        "run", "web_app/frontend/app.py", 
        "--server.port", "8501"
    ]
    frontend_process = subprocess.Popen(frontend_cmd, cwd=ROOT_DIR)
    
    print("\n✅ Web App Running!")
    print("👉 Frontend: http://localhost:8501")
    print("👉 Backend API: http://127.0.0.1:8000/docs")
    print("\nPress Ctrl+C to stop.")

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping App...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Goodbye!")

if __name__ == "__main__":
    run_app()
