"""
Setup dan Installation Guide untuk CV ATS Maker
"""

# ============================================================================
# CV ATS MAKER - COMPLETE SETUP GUIDE
# ============================================================================

"""
📋 TABLE OF CONTENTS
1. Prerequisites
2. Installation Steps
3. Configuration
4. Running the Application
5. Usage Examples
6. Troubleshooting
7. Advanced Configuration
"""

# ============================================================================
# 1. PREREQUISITES
# ============================================================================

"""
Sebelum memulai, pastikan Anda memiliki:

✓ Python 3.8 atau lebih tinggi
✓ pip (Python package manager)
✓ Git (untuk clone repository)
✓ Gemini API Key (dari https://aistudio.google.com)

Cek Python version:
  Windows: python --version
  Linux/Mac: python3 --version

Jika belum terinstall, download dari https://www.python.org
"""

# ============================================================================
# 2. INSTALLATION STEPS
# ============================================================================

"""
LANGKAH 1: Clone atau Download Repository
=========================================

Option A - Menggunakan Git:
  git clone https://github.com/your-repo/cv-ats-maker.git
  cd "CV maker"

Option B - Download Manual:
  1. Download dari GitHub sebagai ZIP
  2. Extract ke folder yang diinginkan
  3. Buka terminal di folder tersebut

LANGKAH 2: Setup Python Environment
===================================

Untuk Windows (Command Prompt atau PowerShell):
  python -m venv venv
  venv\\Scripts\\activate

Untuk Linux/Mac:
  python3 -m venv venv
  source venv/bin/activate

Setelah activate, prompt akan menunjukkan (venv) di depan.

LANGKAH 3: Install Dependencies
===============================

Pastikan sudah dalam virtual environment (seharusnya (venv) terlihat).

  pip install -r requirements.txt

Ini akan install semua package yang diperlukan:
- google-generativeai
- python-dotenv
- flask (untuk web interface)
- reportlab (untuk PDF - optional)
- python-docx (untuk DOCX - optional)

LANGKAH 4: Setup Gemini API Key
===============================

A. Dapatkan API Key:
   1. Kunjungi https://aistudio.google.com
   2. Klik "Create new API key" atau "Get API key"
   3. Pilih project (create new jika perlu)
   4. Copy API key yang di-generate

B. Setup Environment Variable:

   WINDOWS (Command Prompt):
   setx GEMINI_API_KEY "your_api_key_here"

   WINDOWS (PowerShell):
   $env:GEMINI_API_KEY = "your_api_key_here"
   
   WINDOWS (Permanent - Edit .env file):
   GEMINI_API_KEY=your_api_key_here

   LINUX/MAC:
   export GEMINI_API_KEY="your_api_key_here"
   
   LINUX/MAC (Permanent - Add to ~/.bashrc atau ~/.zshrc):
   echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc

C. Verify Setup:
   
   WINDOWS:
   echo %GEMINI_API_KEY%

   LINUX/MAC:
   echo $GEMINI_API_KEY

   Harus menampilkan API key Anda, bukan kosong.

LANGKAH 5: Restart Terminal
===========================

Setelah setup environment variable, RESTART terminal Anda agar perubahan
diaplikasikan dengan benar.
"""

# ============================================================================
# 3. CONFIGURATION
# ============================================================================

"""
File Configuration Utama:
========================

1. .env
   - Buat copy dari .env.example ke .env
   - Edit .env dan isi GEMINI_API_KEY
   - Opsional: customize settings lainnya

2. config.py
   - Berisi default configuration
   - Bisa disesuaikan sesuai kebutuhan

Contoh .env file:

  GEMINI_API_KEY=gsk_abc123xyz...
  OUTPUT_DIRECTORY=cv_output
  OUTPUT_FORMATS=txt,json
  SUMMARY_MAX_LENGTH=150
  ATS_FRIENDLY_FORMATTING=true

"""

# ============================================================================
# 4. RUNNING THE APPLICATION
# ============================================================================

"""
Ada 3 cara menjalankan aplikasi:

OPTION 1: Command Line (Simple)
================================

  python CVmaker.py

- Menjalankan aplikasi dengan sample CV
- Menunjukkan demo dari semua fitur
- Output disimpan di cv_output/

OPTION 2: Interactive CLI
==========================

  python cli.py

- Menu-driven interface
- Tambah info CV secara interaktif
- Optimize dan save CV

OPTION 3: Web Interface
=======================

  python app.py

- Browser-based interface
- Visual dan user-friendly
- Akses di http://localhost:5000

OPTION 4: Run Examples
=======================

  python example_usage.py

- Run multiple examples
- Demonstrasi berbagai fitur
- Learning purpose

"""

# ============================================================================
# 5. USAGE EXAMPLES
# ============================================================================

"""
EXAMPLE 1: Basic Usage (Python Code)
====================================

from CVmaker import CVMaker

# Initialize
cv_maker = CVMaker()

# Add info
cv_maker.cv.personal_info["full_name"] = "John Doe"
cv_maker.cv.add_experience("Developer", "Company", "2022", "2023", "...")
cv_maker.cv.add_skill("Python")

# Optimize
cv_maker.optimize_cv_for_ats()

# Save
cv_maker.save_cv("my_cv")


EXAMPLE 2: Text Summarization
=============================

from CVmaker import CVMaker

cv_maker = CVMaker()

text = "Long experience description..."
summary = cv_maker.summarize_experience(text)
print(summary)


EXAMPLE 3: Load and Modify
===========================

from CVmaker import CVData

# Load
cv = CVData.from_json("cv_output/my_cv.json")

# Modify
cv.add_skill("Kubernetes")

# Save
cv.to_json("cv_output/modified_cv.json")


EXAMPLE 4: Batch Processing
============================

from CVmaker import CVMaker
import glob

cv_files = glob.glob("input_cvs/*.json")
for filepath in cv_files:
    cv_maker = CVMaker()
    cv_maker.cv = CVData.from_json(filepath)
    cv_maker.optimize_cv_for_ats()
    cv_maker.save_cv(f"optimized_{filepath}")

"""

# ============================================================================
# 6. TROUBLESHOOTING
# ============================================================================

"""
PROBLEM 1: "GEMINI_API_KEY tidak ditemukan"
============================================

Solusi:
1. Verify API key sudah di-set dengan benar
   Windows: echo %GEMINI_API_KEY%
   Linux/Mac: echo $GEMINI_API_KEY

2. Restart terminal setelah set environment variable

3. Gunakan .env file:
   - Copy .env.example ke .env
   - Edit .env dan isi GEMINI_API_KEY=your_key

4. Verify di Python:
   import os
   print(os.getenv("GEMINI_API_KEY"))


PROBLEM 2: "ModuleNotFoundError: No module named 'google.generativeai'"
=====================================================================

Solusi:
1. Pastikan virtual environment sudah activate
2. Reinstall packages: pip install -r requirements.txt
3. Verify installation: pip list


PROBLEM 3: "Error menggunakan Gemini API"
=========================================

Solusi:
1. Check internet connection
2. Verify API key valid: https://aistudio.google.com/app/apikey
3. Check API quota dan rate limits
4. Try again later jika API quota habis
5. Fallback mechanism sudah built-in (gunakan original text)


PROBLEM 4: "Permission denied" saat save file
=============================================

Solusi:
1. Check folder permissions
2. Gunakan absolute path
3. Create cv_output folder manually: mkdir cv_output
4. Run as administrator (Windows)


PROBLEM 5: "ImportError: No module named 'config'"
==================================================

Solusi:
1. Pastikan sudah di folder yang benar (CV maker folder)
2. Verify file structure:
   CV maker/
   ├── CVmaker.py
   ├── config.py
   ├── cli.py
   └── ...

3. Run dengan: python CVmaker.py (dari folder yang benar)


PROBLEM 6: CLI menu tidak muncul sempurna di Windows
====================================================

Solusi:
1. Set terminal charset ke UTF-8:
   chcp 65001

2. Gunakan Windows Terminal (bukan Command Prompt lama)

3. Update Python ke versi terbaru


PROBLEM 7: Web interface tidak bisa diakses
===========================================

Solusi:
1. Install Flask: pip install flask
2. Check port 5000 tidak digunakan aplikasi lain
3. Gunakan port berbeda:
   app.run(port=8000)

4. Access dengan IP:
   http://127.0.0.1:5000
   http://localhost:5000

"""

# ============================================================================
# 7. ADVANCED CONFIGURATION
# ============================================================================

"""
CUSTOM OUTPUT FORMATS
=====================

Untuk generate PDF, edit CVExporter di CVmaker.py:

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def export_to_pdf(cv_data, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    # Implementation...
    doc.build(content)

BATCH OPTIMIZATION
==================

Optimize multiple CVs otomatis:

import os
from pathlib import Path
from CVmaker import CVMaker

cv_dir = Path("cv_input")
for cv_file in cv_dir.glob("*.json"):
    maker = CVMaker()
    maker.cv = CVData.from_json(str(cv_file))
    maker.optimize_cv_for_ats()
    maker.save_cv(f"optimized_{cv_file.stem}")

CUSTOM ATS KEYWORDS
===================

Edit ATSOptimizer.ATS_KEYWORDS dalam CVmaker.py:

ATS_KEYWORDS = [
    "responsible", "managed", "led", "developed",
    # Tambah custom keywords
    "collaborated", "implemented", "improved"
]

PROXY CONFIGURATION (Untuk di-behind corporate proxy)
=====================================================

import google.generativeai as genai
import os

os.environ['http_proxy'] = 'http://proxy.company.com:8080'
os.environ['https_proxy'] = 'https://proxy.company.com:8080'

genai.configure(api_key=GEMINI_API_KEY)

"""

# ============================================================================
# QUICK COMMAND REFERENCE
# ============================================================================

"""
WINDOWS COMMANDS
================

Setup:
  python -m venv venv
  venv\\Scripts\\activate
  pip install -r requirements.txt
  setx GEMINI_API_KEY "your_key"

Run:
  python CVmaker.py
  python cli.py
  python app.py

Deactivate venv:
  deactivate

LINUX/MAC COMMANDS
==================

Setup:
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  export GEMINI_API_KEY="your_key"

Run:
  python3 CVmaker.py
  python3 cli.py
  python3 app.py

Deactivate venv:
  deactivate

"""

# ============================================================================
# SUPPORT & RESOURCES
# ============================================================================

"""
📚 Resources
============

- Gemini API Documentation: https://ai.google.dev/
- ATS Best Practices: https://www.indeed.com/career-advice/cvs-cover-letters/applicant-tracking-system-ats
- Python Documentation: https://docs.python.org/
- Flask Documentation: https://flask.palletsprojects.com/
- GitHub Repository: https://github.com/your-repo/cv-ats-maker

📞 Getting Help
===============

1. Check README.md untuk overview
2. Lihat example_usage.py untuk contoh
3. Check troubleshooting section di atas
4. Review log files di cv_output/
5. Create issue di GitHub repository

🐛 Reporting Bugs
=================

Saat report bug, sertakan:
1. OS dan Python version
2. Error message lengkap
3. Steps untuk reproduce
4. Expected vs actual behavior
5. Log file jika ada

"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                  CV ATS MAKER - SETUP GUIDE LOADED                        ║
║                                                                            ║
║  Baca dokumentasi ini untuk setup yang benar dan troubleshooting.         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
