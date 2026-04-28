"""
CV ATS MAKER - QUICK START GUIDE
Panduan cepat untuk mulai dalam 5 menit
"""

QUICK_START = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    CV ATS MAKER - QUICK START (5 MINUTES)                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

⚡ STEP 1: Get Gemini API Key (1 minute)
═════════════════════════════════════════

1. Go to: https://aistudio.google.com
2. Click "Create new API key" (jika belum ada)
3. Select project (atau create new)
4. Copy API key

⚡ STEP 2: Setup Environment (2 minutes)
═════════════════════════════════════════

Windows (Command Prompt):
  1. Open Command Prompt
  2. cd to folder "CV maker"
  3. Run: python -m venv venv
  4. Run: venv\\Scripts\\activate
  5. Run: pip install -r requirements.txt
  6. Run: setx GEMINI_API_KEY "paste_your_api_key_here"
  7. Close & reopen Command Prompt

Windows (PowerShell):
  1. Open PowerShell
  2. cd to folder "CV maker"
  3. Run: python -m venv venv
  4. Run: .\\venv\\Scripts\\Activate.ps1
  5. Run: pip install -r requirements.txt
  6. Run: $env:GEMINI_API_KEY = "paste_your_api_key_here"

Linux/Mac:
  1. Open Terminal
  2. cd to folder "CV maker"
  3. Run: python3 -m venv venv
  4. Run: source venv/bin/activate
  5. Run: pip install -r requirements.txt
  6. Run: export GEMINI_API_KEY="paste_your_api_key_here"

⚡ STEP 3: Run Application (1 minute)
═════════════════════════════════════

Option A - Command Line Demo (Fastest):
  python CVmaker.py

Option B - Interactive CLI:
  python cli.py

Option C - Web Interface:
  python app.py
  Then open: http://localhost:5000

Option D - Run Examples:
  python example_usage.py

⚡ STEP 4: View Output (1 minute)
═════════════════════════════════

Output files are in: cv_output/

- cv_ats_optimized.txt (Plain text - for ATS)
- cv_ats_optimized.json (Structured - for editing)

════════════════════════════════════════════════════════════════════════════════

🎯 BASIC WORKFLOW

1. Run CLI or Web interface
2. Add your information:
   - Personal info (name, email, phone)
   - Work experience
   - Education
   - Skills
3. Let AI summarize your experience (optional)
4. Optimize for ATS
5. Save CV
6. Get two formats: TXT and JSON

════════════════════════════════════════════════════════════════════════════════

💡 TIPS & TRICKS

✓ Use plain text format (.txt) untuk job application portals
✓ Keep JSON backup untuk easy editing later
✓ Summarize long descriptions untuk lebih concise CV
✓ Run optimization multiple times untuk best results
✓ Load JSON to make quick edits

════════════════════════════════════════════════════════════════════════════════

❌ COMMON ISSUES & QUICK FIXES

Issue: "GEMINI_API_KEY not found"
Fix: 1. Verify API key set dengan: echo %GEMINI_API_KEY% (Windows)
     2. Restart terminal
     3. Try setting in .env file

Issue: "ModuleNotFoundError: No module named 'google.generativeai'"
Fix: 1. Activate virtual environment
     2. Run: pip install -r requirements.txt

Issue: "Cannot access http://localhost:5000"
Fix: 1. Install Flask: pip install flask
     2. Check port 5000 tidak dipakai aplikasi lain
     3. Try port berbeda

════════════════════════════════════════════════════════════════════════════════

📚 NEXT STEPS

After Quick Start:
  ✓ Read README.md for full documentation
  ✓ Check example_usage.py for advanced usage
  ✓ Read PROJECT_ARCHITECTURE.md untuk understand structure
  ✓ Customize config.py untuk your needs
  ✓ Try batch processing untuk multiple CVs

════════════════════════════════════════════════════════════════════════════════

🆘 NEED HELP?

1. Check SETUP_GUIDE.py untuk detailed troubleshooting
2. Review README.md untuk comprehensive guide
3. Check example_usage.py untuk usage patterns
4. Review PROJECT_ARCHITECTURE.md untuk technical details

════════════════════════════════════════════════════════════════════════════════

✅ YOU'RE READY!

Setelah langkah-langkah di atas, Anda siap membuat CV yang optimal untuk ATS!

Selamat menggunakan CV ATS Maker! 🚀

════════════════════════════════════════════════════════════════════════════════
"""

# QUICK REFERENCE
QUICK_REFERENCE = """
╔════════════════════════════════════════════════════════════════════════════╗
║  QUICK REFERENCE - Commands & Usage                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

FILE PURPOSES
═════════════

CVmaker.py              → Main application, run this first
cli.py                  → Interactive menu-based interface
app.py                  → Web browser interface
example_usage.py        → See usage examples
config.py               → Configuration settings
requirements.txt        → Dependencies to install
README.md               → Full documentation
SETUP_GUIDE.py          → Installation & troubleshooting
PROJECT_ARCHITECTURE.md → Technical architecture


COMMAND REFERENCE
═════════════════

# Setup (one time)
python -m venv venv
venv\\Scripts\\activate (Windows) atau source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
setx GEMINI_API_KEY "your_api_key" (Windows) atau export GEMINI_API_KEY="your_api_key" (Mac/Linux)

# Run Application
python CVmaker.py                   # Demo dengan sample CV
python cli.py                       # Interactive menu
python app.py                       # Web interface (localhost:5000)
python example_usage.py             # See examples

# Deactivate virtual environment
deactivate


PYTHON API USAGE
════════════════

from CVmaker import CVMaker

# Initialize
cv_maker = CVMaker()

# Use sample
cv_maker.cv = cv_maker.create_sample_cv()

# Add info
cv_maker.cv.personal_info["full_name"] = "Your Name"
cv_maker.cv.add_experience("Title", "Company", "2022", "2023", "Description")
cv_maker.cv.add_skill("Python")

# Summarize
summary = cv_maker.summarize_experience("Long description...")

# Optimize
cv_maker.optimize_cv_for_ats()

# Save
cv_maker.save_cv("my_cv_name")


FILE STRUCTURE
══════════════

CV maker/
├── CVmaker.py                   Main application
├── cli.py                       CLI interface
├── app.py                       Web interface
├── config.py                    Configuration
├── example_usage.py             Examples
├── requirements.txt             Dependencies
├── README.md                    Documentation
├── SETUP_GUIDE.py               Setup help
├── PROJECT_ARCHITECTURE.md      Architecture
├── QUICK_START.py              This file
├── .env.example                 Environment template
└── cv_output/                   Generated CVs
    ├── my_cv.txt
    └── my_cv.json


KEY FEATURES AT A GLANCE
════════════════════════

✓ Gemini AI integration untuk summarization & optimization
✓ ATS optimization untuk applicant tracking systems
✓ Multiple output formats (TXT, JSON)
✓ Multiple interfaces (CLI, Web, Python API)
✓ Batch processing support
✓ Backup & restore via JSON
✓ Custom keyword injection
✓ Professional formatting


TYPICAL WORKFLOW
════════════════

1. Run: python CVmaker.py (atau python cli.py)
2. Add your information
3. Optional: Summarize long descriptions
4. Run: Optimize for ATS
5. Save: Generate TXT & JSON files
6. Copy TXT content ke job portals
7. Keep JSON for future edits


OUTPUT FORMATS
══════════════

Plain Text (.txt)
  ✓ ATS-optimized
  ✓ Paste directly to forms
  ✓ Simple formatting
  ✓ Universal compatibility

JSON (.json)
  ✓ Structured data
  ✓ Easy to edit programmatically
  ✓ Backup & restore
  ✓ Version control friendly


IMPORTANT NOTES
═══════════════

⚠️ NEVER share your GEMINI_API_KEY
⚠️ Don't commit .env file to git
⚠️ Always use virtual environment
⚠️ Keep backups of your CV JSON files
✓ Test dengan sample data first
✓ Use plain text format untuk ATS systems
✓ Keep multiple CV versions untuk different jobs


SUPPORT MATRIX
══════════════

Windows + Python 3.8+      ✓ Fully supported
Mac + Python 3.8+          ✓ Fully supported
Linux + Python 3.8+        ✓ Fully supported
Python 3.7 atau lebih      ⚠️ May work but not tested
Python 2.x                 ❌ Not supported


TROUBLESHOOTING 101
═══════════════════

Problem                           | Quick Fix
─────────────────────────────────┼──────────────────────────────
API key tidak ditemukan           | Restart terminal, set env var
ModuleNotFoundError               | pip install -r requirements.txt
Web app tidak bisa diakses        | pip install flask, check port 5000
File permission denied            | Run as admin, check path
Summarization tidak bekerja       | Check internet, verify API key


GET HELP
════════

1. QUICK FIXES:
   - Restart terminal/IDE
   - Reinstall dependencies: pip install -r requirements.txt
   - Verify API key: echo $GEMINI_API_KEY

2. DETAILED HELP:
   - Read: SETUP_GUIDE.py
   - Read: README.md
   - See: example_usage.py

3. DEBUG:
   - Check cv_output folder untuk output files
   - Review error messages carefully
   - Try running with sample first

════════════════════════════════════════════════════════════════════════════════
"""

def main():
    """Print quick start guide"""
    print(QUICK_START)
    print(QUICK_REFERENCE)
    
    print("\n" + "="*80)
    print("✅ QUICK START GUIDE COMPLETE!")
    print("👉 Next: python CVmaker.py atau python cli.py")
    print("📖 Full docs: README.md dan SETUP_GUIDE.py")
    print("="*80)


if __name__ == "__main__":
    main()
