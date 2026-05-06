#!/usr/bin/env python3
"""
start.py - Single entrypoint to start CV Maker Pro

Usage:
  python start.py [--no-checks] [--no-browser]

This script:
 - loads .env if present
 - checks for common Python dependencies (advisory)
 - ensures `cv_data/` and `cv_output/` folders exist
 - starts the server (runs `server.py`)
 - optionally opens the browser at http://localhost:5000

"""
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except Exception:
    DOTENV_AVAILABLE = False


def load_env():
    if DOTENV_AVAILABLE and Path('.env').exists():
        load_dotenv()
        print('Loaded .env')


def ensure_folders():
    for d in ('cv_data', 'cv_output', 'templates'):
        p = Path(d)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            print(f'Created folder: {d}/')
        else:
            print(f'Folder exists: {d}/')


def check_dependencies():
    """Basic advisory dependency checks (non-fatal).

    Returns True if core deps present, False otherwise.
    """
    print('\nChecking key Python packages (advisory)')
    required = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('google.generativeai', 'google-generativeai'),
    ]
    missing = []
    for module, nice in required:
        try:
            __import__(module)
            print(f'  ✓ {nice}')
        except Exception:
            print(f'  ✗ {nice} (missing)')
            missing.append(nice)

    # Optional OCR stack
    optional = [
        ('PyPDF2', 'PyPDF2'),
        ('pdf2image', 'pdf2image'),
        ('pytesseract', 'pytesseract'),
    ]
    print('\nOptional OCR packages:')
    for module, nice in optional:
        try:
            __import__(module)
            print(f'  ✓ {nice}')
        except Exception:
            print(f'  - {nice} (optional)')

    if missing:
        print('\nMissing core packages detected:')
        for m in missing:
            print(f' - {m}')
        print('\nInstall all required packages with:')
        print('  pip install -r requirements.txt')
        return False
    return True


def check_api_key():
    key = os.getenv('GEMINI_API_KEY')
    if not key:
        print('\nWARNING: GEMINI_API_KEY is not set. Gemini AI features will not work until you set this environment variable or create a .env file.')
        return False
    print('\nGEMINI_API_KEY is set')
    return True


def start_server(open_browser=True):
    # Start server.py using the same python executable
    server_path = Path('server.py')
    if not server_path.exists():
        print('Error: server.py not found in project root.')
        sys.exit(1)

    print('\nStarting server (this runs `python server.py`)...')
    proc = subprocess.Popen([sys.executable, str(server_path)], cwd=str(Path.cwd()))

    # Wait briefly for server to start
    time.sleep(1.5)
    url = f'http://localhost:{os.getenv("FLASK_PORT", "5000")}'
    if open_browser:
        try:
            webbrowser.open(url)
            print(f'Opened browser at {url}')
        except Exception:
            print('Could not open browser automatically. Open your browser to ' + url)

    try:
        proc.wait()
    except KeyboardInterrupt:
        print('\nStopping server...')
        proc.terminate()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Start CV Maker Pro (server + helpers)')
    parser.add_argument('--no-checks', action='store_true', help='Skip dependency and API key checks')
    parser.add_argument('--no-browser', action='store_true', help='Do not open the browser automatically')
    args = parser.parse_args()

    load_env()
    ensure_folders()

    if not args.no_checks:
        ok = check_dependencies()
        check_api_key()
        if not ok:
            print('\nSome required packages are missing. Fix before continuing, or run with --no-checks to start anyway.')
            # Let user choose to continue or exit
            resp = input('Continue anyway? [y/N]: ').strip().lower()
            if resp != 'y':
                print('Aborting startup.')
                sys.exit(1)

    start_server(open_browser=not args.no_browser)


if __name__ == '__main__':
    main()
