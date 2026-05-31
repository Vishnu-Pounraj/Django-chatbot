import os
import sys
import subprocess
import webbrowser
import time

def runserver():
    print("Starting server...")
    venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "activate")

    if os.path.exists(venv_path):
        print("Activating virtual environment...")
        subprocess.call(venv_path, shell=True)
        print("Virtual environment Activated...")

    # Start Django server in background
    process = subprocess.Popen(
        [sys.executable, "manage.py", "runserver"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait a bit for server to 
    print("Server Started wait for sometime.....")
    time.sleep(2)
    print("Opening your browser......")

    # Open browser
    webbrowser.open("http://127.0.0.1:8000/")

    # Keep script running
    process.wait()
    

if __name__ == "__main__":
    runserver()