"""
Configuration file untuk CV ATS Maker
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Application Settings
APP_NAME = "CV ATS Maker"
APP_VERSION = "1.0.0"

# Output Settings
OUTPUT_DIRECTORY = "cv_output"
DEFAULT_OUTPUT_FORMAT = ["txt", "json"]  # Bisa ditambah "pdf", "docx"

# ATS Optimization Settings
ATS_FRIENDLY_FORMATTING = True
REMOVE_SPECIAL_CHARACTERS = True
USE_ACTION_VERBS = True

# Text Summarization Settings
SUMMARY_MAX_LENGTH = 150  # kata
SUMMARY_LANGUAGE = "indonesian"

# Gemini Model Settings
GEMINI_MODEL = "gemini-pro"
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 1000

print(f"✓ Configuration loaded: {APP_NAME} v{APP_VERSION}")
