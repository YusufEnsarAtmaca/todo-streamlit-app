"""
Todo List Application - Entry Point
This module serves as the main entry point for the Streamlit todo list application.
"""

import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "5000"])
