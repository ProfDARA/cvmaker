# CV Maker Pro v2.0

**Full-Stack Web Application untuk Optimasi CV dan Analisis Job Fit menggunakan Gemini AI**

![Version](https://img.shields.io/badge/version-2.0-blue)
![Status](https://img.shields.io/badge/status-production-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Fitur Utama

### CV Editor
- Interactive form dengan tabs (Personal, Experience, Education, Skills, Storage)
- Tambah/hapus pengalaman kerja, pendidikan, skills dinamis
- Real-time form validation
- Professional UI dengan responsive design

### Real-Time ATS Optimizer
- Instant ATS score (0-100)
- Level classification (EXCELLENT/GOOD/MODERATE/POOR)
- Actionable improvement suggestions
- Visual score display dengan progress bar

### Job Fit Analyzer
- Paste job description → Get fit score
- Matched skills identification
- Missing skills gap analysis
- Personalized AI recommendations
- Experience relevance scoring

### Smart Storage
- Save CV ke JSON file (local storage)
- Load any previously saved CV
- List all saved CVs dengan metadata
- Delete unwanted CVs
- No cloud sync required (complete privacy)

### Modern UI
- Beautiful gradient design
- Smooth animations & transitions
- Responsive (desktop, tablet, mobile)
- Intuitive navigation dengan tabs
- Real-time visual feedback

---

## Quick Start

### Installation

```bash
# Clone atau download project
cd "CV maker"

# Install dependencies
pip install -r requirements.txt

# Set Gemini API Key
# Windows:
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac:
export GEMINI_API_KEY="your_api_key_here"

# Or create .env file:
echo GEMINI_API_KEY=your_api_key_here > .env
```

#### OCR prerequisites (optional, required to load PDF CVs via OCR)

- Tesseract OCR (system dependency)
   - Windows: install from https://github.com/tesseract-ocr/tesseract and add to PATH
   - macOS (Homebrew): `brew install tesseract`
   - Linux (apt): `sudo apt-get install tesseract-ocr`

- Poppler (required by pdf2image)
   - Windows: download from https://blog.alivate.com.au/poppler-windows/ and add `bin` to PATH
   - macOS (Homebrew): `brew install poppler`
   - Linux (apt): `sudo apt-get install poppler-utils`

After system deps are installed, install Python packages:

```bash
pip install -r requirements.txt
```

### Start Application

```bash
# Terminal 1 - Start backend server
python server.py

# Terminal 2 - Open frontend
# Double-click index.html
# atau: file:///path/to/index.html
```

### Get Gemini API Key

1. Visit: https://aistudio.google.com
2. Click "Get API Key"
3. Copy API key
4. Set sebagai environment variable

---

## How to Use

### Create & Optimize CV

1. **Fill Personal Information**
   - Name, email, phone, location
   - LinkedIn, website (optional)

2. **Add Experience**
   - Click "+ Add Experience"
   - Enter job title, company, dates, description
   - Add multiple positions

3. **Add Education**
   - Degree, institution, field, graduation year
   - Click "+ Add Education" untuk tambah lebih

4. **Add Skills**
   - Enter skill name
   - Click "+ Add"
   - Repeat untuk semua skills

5. **Check ATS Score**
   - Click "Check ATS Score"
   - View suggestions
   - Edit CV based on feedback

6. **Save CV**
   - Go to "Storage" tab
   - Click "Save CV"
   - CV saved to `cv_data/` folder

### Analyze Job Fit

1. **Paste Job Description**
   - Copy job posting text
   - Paste ke textarea

2. **Click Analyze Fit**
   - Click "Analyze Fit"
   - Wait for AI analysis

3. **View Results**
   - Fit score (0-100)
   - Matched skills
   - Missing skills
   - Recommendations

4. **Improve & Repeat**
   - Edit CV based on recommendations
   - Re-analyze for same job
   - Compare fit scores

---

## Architecture

### Full-Stack Design

```
Frontend (index.html)
    ↓ HTTP/JSON
Backend API (server.py)
    ↓ Python Objects
Core Logic (CVmaker.py)
    ↓ API Calls
Gemini AI + Local Storage
```

### Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla, no frameworks)
- **Backend:** Flask 3.0, Flask-CORS
- **Core Logic:** Python 3.8+
- **AI:** Google Generative AI (Gemini)
- **Storage:** JSON files (local)
- **Database:** None (lightweight)

---

## API Endpoints

### Analyze ATS Score
```
POST /api/cv/analyze-ats
```
**Request:** CV data (JSON)
**Response:** `{ ats_score, level, suggestions, optimized_cv }`

### Analyze Job Fit
```
POST /api/job/analyze-fit
```
**Request:** `{ cv, job_description }`
**Response:** `{ fit_score, fit_level, matched_skills, missing_skills, recommendations }`

### Save CV
```
POST /api/cv/save
```
**Request:** `{ cv_data, filename }`
**Response:** `{ filename, filepath, saved_at }`

### Load CV
```
GET /api/cv/load/{filename}
```
**Response:** CV data (JSON)

### List Saved CVs
```
GET /api/cv/list
```
**Response:** `{ count, cvs[] }`

### More Endpoints
See [SETUP_FULLSTACK.md](SETUP_FULLSTACK.md) untuk full API documentation.

---

## Project Structure

```
CV maker/
├── index.html                 # Frontend UI
├── server.py                  # Backend API
├── CVmaker.py                 # Core logic
├── requirements.txt           # Dependencies
├── cv_data/                   # Saved CVs (JSON)
├── cv_output/                 # Exports (PDF, TXT)
│
├── DOCUMENTATION
│   ├── README.md              # This file
│   ├── SETUP_FULLSTACK.md     # Setup guide
│   ├── ARCHITECTURE_v2.md     # Architecture details
│   ├── JOBFIT_GUIDE.md        # Job Fit feature
│   └── quickstart.py          # Quick start helper
│
└── .env                       # Environment variables
```

---

## Configuration

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your_api_key_here

# Optional (defaults shown)
FLASK_DEBUG=False
FLASK_PORT=5000
```

### Create .env File

```bash
# Windows/Mac/Linux
echo GEMINI_API_KEY=your_key > .env
```

---

## 🎯 ATS Score Breakdown

| Category | Points | Description |
|----------|--------|-------------|
| Personal Info | 10 | Name, email, phone, location, LinkedIn |
| Professional Summary | 10 | Clear, detailed overview |
| Experience | 30 | Multiple roles, action verbs, metrics |
| Education | 15 | Degrees, institutions, graduation year |
| Skills | 20 | Relevant technical and soft skills |
| Certifications | 10 | Industry recognized certifications |
| Formatting | 5 | Clean format, no special characters |
| **Total** | **100** | **Overall fit score** |

---

## Real-Time Analysis

### ATS Optimizer
```
Input: CV data
   ↓
Calculate score based on completeness
   ↓
Generate improvement suggestions
   ↓
Output: Score + Recommendations
```

### Job Fit Analyzer
```
Input: CV + Job description
   ↓
Use Gemini AI for intelligent matching
   ↓
Identify skill gaps
   ↓
Output: Fit score + Analysis + Recommendations
```

---

## Data Privacy

- ✅ All data stored **locally** on your computer
- ✅ No cloud upload or sync
- ✅ No login or account required
- ✅ Complete control over your data
- ✅ Can backup or delete anytime

---

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### GEMINI_API_KEY Error
```bash
# Check if set
echo $GEMINI_API_KEY  # Linux/Mac
echo %GEMINI_API_KEY%  # Windows

# Get new key from https://aistudio.google.com
# Restart server after setting new key
```

### Frontend Not Connecting
- Check backend server is running (port 5000)
- Open browser console (F12) for errors
- Verify API_BASE_URL in index.html

### CV Not Saving
- Check `cv_data/` folder exists
- Check file permissions
- Try different filename

---

## 📚 Documentation

| Document | Content |
|----------|---------|
| **SETUP_FULLSTACK.md** | Complete setup guide + API docs + features |
| **ARCHITECTURE_v2.md** | Full architecture explanation + changes |
| **JOBFIT_GUIDE.md** | Job Fit Analyzer feature documentation |
| **JOBFIT_IMPLEMENTATION.md** | Implementation details + examples |
| **quickstart.py** | Quick start helper script |

---

## 💡 Tips for Best Results

### ATS Optimization
1. ✅ Include all relevant experience
2. ✅ Use strong action verbs (managed, led, developed, etc)
3. ✅ Quantify achievements (increased by 40%, managed team of 5, etc)
4. ✅ Add relevant certifications
5. ✅ Keep descriptions concise but detailed

### Job Fit Analysis
1. ✅ Paste complete job posting
2. ✅ Include requirements and responsibilities
3. ✅ CV should have all relevant experience
4. ✅ Re-analyze after CV updates
5. ✅ Compare multiple job postings

---

## 🚀 Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Set GEMINI_API_KEY
3. ✅ Run quickstart: `python quickstart.py`
4. ✅ Start server: `python server.py`
5. ✅ Open browser: `index.html`
6. ✅ Create your CV and analyze!

---

## 📝 Examples

### Example 1: Optimize Resume for ATS
```
1. Open index.html
2. Fill in your CV information
3. Click "⚡ Check ATS Score"
4. View score and suggestions
5. Make improvements
6. Re-check score
7. Save CV when satisfied
```

### Example 2: Check Job Fit
```
1. Load saved CV or fill new one
2. Paste job description
3. Click "🎯 Analyze Fit"
4. View matched/missing skills
5. Read recommendations
6. Update CV if needed
```

---

## 🌟 Features Showcase

### Interactive UI
- 📱 Responsive design (mobile-friendly)
- 🎨 Modern gradient interface
- ✨ Smooth animations
- 📊 Real-time visualizations
- 🎯 Intuitive navigation

### Powerful Analysis
- 🤖 AI-powered matching
- 📈 Intelligent scoring
- 💡 Smart recommendations
- 🔍 Gap analysis
- 📊 Detailed reporting

### User-Friendly
- 💾 One-click save/load
- 📝 Easy CV editing
- 🎯 Clear instructions
- 🚀 Quick analysis
- 📱 Works offline*

---

## ✅ What's New in v2.0

### Major Changes
- ✅ Modern web UI (replaced CLI)
- ✅ Real-time ATS scoring
- ✅ Interactive CV editor
- ✅ Job Fit analyzer
- ✅ Local JSON storage
- ✅ Beautiful responsive design

### Maintained Features
- ✅ CVmaker.py core logic (backward compatible)
- ✅ Gemini AI integration
- ✅ ATS optimization
- ✅ Export capabilities
- ✅ Job Fit analysis

---

## 🤝 Contributing

Improvements and suggestions welcome! Areas to enhance:
- Additional CV templates
- More export formats
- Interview prep mode
- Salary insights
- Company research

---

## 📄 License

MIT License - feel free to use and modify!

---

## 🙋 Support

Need help? Check these resources:
1. **SETUP_FULLSTACK.md** - Comprehensive setup guide
2. **quickstart.py** - Automatic verification script
3. **Browser console (F12)** - Check for errors
4. **File:// protocol** - Open index.html directly

---

## 🎉 Get Started Now!

1. Install dependencies
2. Set Gemini API key
3. Run `python server.py`
4. Open `index.html`
5. Create your optimized CV!

---

**Status:** ✅ Production Ready | **Version:** 2.0 | **Type:** Full-Stack Web App

*Built with ❤️ for job seekers. Optimize your CV, land your dream job!*


## ✨ Fitur Utama

- **CV Data Management**: Manajemen data CV terstruktur dengan informasi lengkap
- **ATS Optimization**: Otomatis mengoptimalkan CV untuk sistem ATS
- **Text Summarizer**: Merangkum deskripsi pekerjaan menggunakan Gemini API
- **Job Fit Analyzer** ⭐ NEW: Analisis kecocokan CV dengan job description menggunakan AI
- **Multi-Format Export**: Export ke Plain Text (ATS-friendly) dan JSON
- **Professional Keywords**: Menambahkan action verbs dan keywords industri
- **Format Cleaning**: Menghapus formatting kompleks yang tidak ATS-friendly

## 🚀 Quick Start

### 1. Setup Environment

**Windows:**
```bash
# Clone atau download repository
cd "CV maker"

# Install dependencies
pip install -r requirements.txt

# Set Gemini API Key (Windows PowerShell)
$env:GEMINI_API_KEY = "your_api_key_here"

# Atau set permanent (Windows CMD)
setx GEMINI_API_KEY "your_api_key_here"
```

**Linux/Mac:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set Gemini API Key
export GEMINI_API_KEY="your_api_key_here"

# Untuk permanent, tambah ke ~/.bashrc atau ~/.zshrc
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
```

### 2. Dapatkan Gemini API Key

1. Kunjungi https://aistudio.google.com
2. Click "Get API Key" atau "Create new API key"
3. Copy API key Anda
4. Set sebagai environment variable

### 3. Run Aplikasi

```bash
python CVmaker.py
```

## 📖 Penggunaan

### Basic Usage

```python
from CVmaker import CVMaker

# Initialize CV Maker
cv_maker = CVMaker(api_key="your_api_key")

# Create CV object
cv = cv_maker.cv

# Add personal info
cv.personal_info = {
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+62-812-1234-5678",
    "location": "Jakarta, Indonesia",
    "linkedin": "linkedin.com/in/johndoe"
}

# Add experience
cv.add_experience(
    job_title="Senior Developer",
    company="Tech Company",
    start_date="Jan 2022",
    end_date="Present",
    description="Managed development team and delivered projects on time"
)

# Add education
cv.add_education(
    degree="Bachelor",
    institution="University",
    field="Computer Science",
    graduation_year="2020"
)

# Add skills
cv.add_skill("Python")
cv.add_skill("JavaScript")
cv.add_skill("Docker")

# Optimize for ATS
cv_maker.optimize_cv_for_ats()

# Save CV
cv_maker.save_cv("my_cv")
```

### Summarize Experience

```python
# Summarize experience description
summary = cv_maker.summarize_experience(
    "Bertanggung jawab atas pengembangan dan maintenance aplikasi web, "
    "implementasi CI/CD pipeline, dan kolaborasi dengan tim design"
)
print(summary)
```

### Job Fit Analyzer (NEW)

Analisis kecocokan CV Anda dengan job description menggunakan AI:

```python
from CVmaker import JobFitAnalyzer

# Method 1: Direct job description
job_desc = """
SENIOR DEVELOPER

Requirements:
- 5+ years Python experience
- Django expertise
- PostgreSQL & Docker
- AWS cloud platforms
"""

analysis = cv_maker.check_job_fit(job_desc)
JobFitAnalyzer.display_fit_analysis(analysis)

# Method 2: Load from file
analysis = cv_maker.check_job_fit_from_file("job_description.txt")
JobFitAnalyzer.display_fit_analysis(analysis)

# Save results
cv_maker.save_job_fit_analysis(analysis, "my_analysis")
```

**Output:**
- Fit Score (0-100)
- Matched & Missing Skills
- Strengths & Weaknesses
- AI-Generated Recommendations
- Saved to JSON format

Lihat [JOBFIT_GUIDE.md](JOBFIT_GUIDE.md) untuk dokumentasi lengkap.

## 📁 Struktur File

```
CV maker/
├── CVmaker.py          # Main application
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── README.md          # Documentation (this file)
├── .env               # Environment variables (create manually)
└── cv_output/         # Output folder (auto-created)
    ├── my_cv_ats_optimized.txt
    └── my_cv_ats_optimized.json
```

## 🏗️ Arsitektur Aplikasi

### Classes

1. **GeminiConfig**
   - Konfigurasi dan komunikasi dengan Gemini API
   - Summarize text
   - Optimize CV content

2. **CVData**
   - Model untuk data CV
   - Methods untuk add experience, education, skills, dll
   - Export ke dict, JSON

3. **ATSOptimizer**
   - Optimasi formatting untuk ATS
   - Remove special characters
   - Add action keywords

4. **JobFitAnalyzer** ⭐ NEW
   - Analisis kecocokan CV dengan job description
   - Load job description dari file
   - Generate recommendations
   - Display hasil dengan formatting rapi

5. **CVExporter**
   - Export CV ke berbagai format
   - Plain text format (ATS-friendly)
   - JSON format

6. **CVMaker**
   - Main application class
   - Koordinasi semua components
   - Workflow management

## 🎯 ATS Optimization Features

### Formatting Optimization
- Hapus simbol khusus yang tidak standard
- Ubah bullet points ke format sederhana
- Remove excessive spaces

### Content Optimization
- Tambah action verbs (achieved, led, managed, dll)
- Professional language
- Structured information

### Keyword Enhancement
- Industry-specific keywords
- Measurable achievements
- Clear role descriptions

## 📊 Output Format

### Plain Text (TXT)
```
JOHN DOE
Email: john@example.com
Phone: +62-812-1234-5678
---

PROFESSIONAL SUMMARY
Experienced developer...

EXPERIENCE

Senior Developer at Tech Company
Jan 2022 - Present
Led development team...

EDUCATION

Bachelor in Computer Science
University (2020)

SKILLS
Python, JavaScript, Docker, AWS
```

### JSON Format
```json
{
  "personal_info": {
    "full_name": "John Doe",
    "email": "john@example.com",
    ...
  },
  "professional_summary": "...",
  "experience": [...],
  "education": [...],
  "skills": [...]
}
```

## 🔧 Advanced Usage

### Custom CV Processing

```python
from CVmaker import CVMaker, CVExporter, ATSOptimizer

cv_maker = CVMaker()

# Load existing CV from JSON
cv = CVMaker.from_json("existing_cv.json")
cv_maker.cv = cv

# Optimize specific experience
for exp in cv_maker.cv.experience:
    optimized_desc = ATSOptimizer.add_ats_keywords(exp['description'])
    exp['description'] = optimized_desc

# Save
cv_maker.save_cv("optimized_cv")
```

### Batch Processing

```python
import glob

# Process multiple CVs
cv_files = glob.glob("input_cvs/*.json")
for cv_file in cv_files:
    cv_maker = CVMaker()
    cv_maker.cv = CVData.from_json(cv_file)
    cv_maker.optimize_cv_for_ats()
    filename = cv_file.split('/')[-1].replace('.json', '')
    cv_maker.save_cv(f"optimized_{filename}")
```

## 🐛 Troubleshooting

### "GEMINI_API_KEY tidak ditemukan"
- Setup environment variable sesuai OS Anda
- Pastikan API key valid dari https://aistudio.google.com
- Restart terminal/IDE setelah set environment variable

### "Error menggunakan Gemini API"
- Check internet connection
- Verify API key masih valid
- Check quota di Google AI Studio
- Fallback mechanism sudah ada (use original text)

### File not found
- Pastikan working directory sudah benar
- Gunakan absolute path jika perlu
- Create cv_output folder manually jika needed

## 📝 Environment Variables

Buat file `.env` di root folder:

```
GEMINI_API_KEY=your_api_key_here
```

## 🔐 Security Tips

- ⚠️ Jangan commit `.env` file dengan API key
- Gunakan `.gitignore` untuk `.env`
- Rotate API key secara berkala
- Jangan share API key di public repository

## 📚 Dependencies

- **google-generativeai**: Gemini API client
- **python-dotenv**: Environment variable management
- **reportlab**: PDF generation (optional)
- **python-docx**: DOCX generation (optional)

## 🎓 Learning Resources

- [Gemini API Documentation](https://ai.google.dev/)
- [ATS Best Practices](https://www.indeed.com/career-advice/cvs-cover-letters/applicant-tracking-system-ats)
- [Google AI Studio](https://aistudio.google.com)

## 📄 License

MIT License - Feel free to use and modify

## 👨‍💻 Author

Created with ❤️ for better CV optimization

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:
1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Create Pull Request

## 📞 Support

Untuk pertanyaan atau issues, silakan create issue di repository.

---

**Happy CV Making! 🚀**
