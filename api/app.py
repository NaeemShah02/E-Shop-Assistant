# api/app.py
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so we can import chatbot.py
current = Path(__file__).resolve()
project_root = current.parent.parent
sys.path.append(str(project_root))

# Import the Flask app instance exported in chatbot.py
import chatbot
app = chatbot.app  # Vercel will look for 'app'
