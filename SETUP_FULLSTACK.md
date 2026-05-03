# 🚀 CV Maker Pro - Full-Stack Architecture Setup Guide

## 📋 Architecture Overview

Aplikasi sekarang menggunakan **modern full-stack architecture**:

```
┌─────────────────────────────────────┐
│   Frontend (HTML/CSS/JavaScript)    │
│         index.html                  │
│  - CV Form dengan Tabs              │
│  - Real-time ATS Score              │
│  - Job Fit Analyzer                 │
│  - Save/Load ke JSON                │
└──────────────┬──────────────────────┘
               │ HTTP/JSON
┌──────────────▼──────────────────────┐
│   Backend API (Flask)               │
│         server.py                   │
│  - /api/cv/analyze-ats              │
│  - /api/job/analyze-fit             │
│  - /api/cv/save                     │
│  - /api/cv/load                     │
│  - /api/cv/list                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Core Logic (Python)               │
│         CVmaker.py                  │
│  - CV Optimization                  │
│  - Job Fit Analysis                 │
│  - ATS Scoring                      │
└─────────────────────────────────────┘
```

---

## ⚙️ Setup Instructions

### 1️⃣ **Install Dependencies**

```bash
# Install all required packages
pip install -r requirements.txt
```

**Required packages:**
- `flask` - Backend API server
- `flask-cors` - Cross-origin requests
- `google-generativeai` - Gemini API
- `python-dotenv` - Environment variables
- `reportlab` - PDF export

### 2️⃣ **Configure Gemini API Key**

**Option A: Create `.env` file**
```bash
# Windows/Mac/Linux
echo GEMINI_API_KEY=your_api_key_here > .env
```

**Option B: Set environment variable**
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY = "your_api_key_here"

# Windows (CMD)
setx GEMINI_API_KEY "your_api_key_here"

# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"
```

**Get API Key:**
1. Visit: https://aistudio.google.com
2. Click "Get API Key"
3. Copy and save your key

---

## 🎯 Running the Application

### Step 1: Start Backend Server

```bash
# Terminal 1 - Start Flask server
python server.py
```

**Expected output:**
```
======================================================================
CV MAKER API SERVER
======================================================================

🚀 Starting server on http://localhost:5000
📖 Documentation: http://localhost:5000/api/docs
🌐 Frontend: Open index.html in browser

======================================================================
```

### Step 2: Open Frontend

```bash
# Option 1: Double-click index.html
#   or
# Option 2: Open in browser
# URL: file:///path/to/index.html
```

---

## 📱 Features Overview

### ✨ CV Editor
- **Personal Information** - Name, email, phone, location, LinkedIn, website
- **Experience** - Multiple jobs with dates and descriptions
- **Education** - Degree, institution, field of study, graduation year
- **Skills** - Add/remove skills dynamically
- **Storage** - Save/load CV from JSON files

### 🔍 ATS Score Analyzer (Real-time)
- **Score Display** - 0-100 scoring system
- **Level Badge** - EXCELLENT/GOOD/MODERATE/POOR
- **Suggestions** - AI-powered improvement tips
- **Optimization** - Real-time CV optimization

### 🎯 Job Fit Analyzer
- **Paste Job Description** - Input job posting text
- **Get Fit Score** - Instant compatibility analysis
- **Matched Skills** - Skills that match the job
- **Missing Skills** - Skills to develop
- **Recommendations** - Personalized suggestions

### 💾 Local Storage
- **Save CV** - Save to JSON file locally
- **Load CV** - Load previously saved CVs
- **List CVs** - View all saved CVs
- **Delete CV** - Remove saved CVs

---

## 📡 API Endpoints

### Health Check
```
GET /api/health
Response: { status: 'healthy', api_key_set: true }
```

### Analyze ATS Score
```
POST /api/cv/analyze-ats
Request: { personal_info, professional_summary, experience, education, skills, ... }
Response: { ats_score: 75, level: 'GOOD', suggestions: [...], optimized_cv: {...} }
```

### Analyze Job Fit
```
POST /api/job/analyze-fit
Request: { cv: {...}, job_description: "..." }
Response: { fit_score: 80, fit_level: 'EXCELLENT', matched_skills: [...], ... }
```

### Save CV
```
POST /api/cv/save
Request: { cv_data: {...}, filename: "my_cv" }
Response: { filename: 'my_cv', filepath: '...', saved_at: '...' }
```

### Load CV
```
GET /api/cv/load/{filename}
Response: { personal_info: {...}, experience: [...], ... }
```

### List CVs
```
GET /api/cv/list
Response: { count: 3, cvs: [{filename, name, size, created}, ...] }
```

### Delete CV
```
DELETE /api/cv/delete/{filename}
Response: { deleted: 'filename' }
```

---

## 📂 Folder Structure

```
CV maker/
├── server.py                    # Flask backend API
├── CVmaker.py                  # Core CV optimization logic
├── index.html                  # Frontend UI
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── JOBFIT_GUIDE.md            # Job Fit feature guide
├── cv_data/                    # Saved CV JSON files
│   ├── my_cv.json
│   ├── my_cv_2024.json
│   └── ...
├── cv_output/                  # Export outputs
│   ├── my_cv.pdf
│   ├── my_cv.txt
│   └── ...
├── templates/                  # (Optional) HTML templates
│   └── index.html             # Main template
└── .env                        # Environment variables (create manually)
```

---

## 🎨 UI Components

### Left Panel: CV Editor
- **Tabs:** Personal | Experience | Education | Skills | Storage
- **Form Fields:** Dynamic input with validation
- **Add/Remove Items:** Add multiple experiences, educations, skills
- **Save/Load:** Manage CV persistence

### Right Panel: Analysis
- **Tabs:** ATS Score | Job Fit
- **Score Display:** Visual score card with progress bar
- **Level Badge:** Color-coded fit level
- **Suggestions:** Actionable improvement tips
- **Stats Grid:** Quick metrics display

### Colors & Design
- **Primary:** #4f46e5 (Indigo)
- **Success:** #10b981 (Green)
- **Warning:** #f59e0b (Amber)
- **Danger:** #ef4444 (Red)
- **Responsive:** Works on desktop, tablet, mobile

---

## 💡 Usage Examples

### Example 1: Create & Optimize CV

1. **Fill Personal Info**
   - Enter your name, email, phone, location
   - Add LinkedIn and website links

2. **Add Experience**
   - Click "+ Add Experience"
   - Fill job title, company, dates, description
   - Add multiple positions

3. **Add Education**
   - Click "+ Add Education"
   - Enter degree, institution, field, graduation year

4. **Add Skills**
   - Enter skill name
   - Click "+ Add"
   - Repeat for all skills

5. **Check ATS Score**
   - Click "⚡ Check ATS Score"
   - View score and suggestions
   - Make improvements based on feedback

6. **Save CV**
   - Go to "Storage" tab
   - Click "💾 Save CV"
   - CV saved to `cv_data/` folder

### Example 2: Analyze Job Fit

1. **Load Your CV**
   - Use "📂 Load CV" button to load previously saved CV
   - Or create new CV in editor

2. **Paste Job Description**
   - Copy job posting text
   - Paste into "Job Description" field

3. **Analyze Fit**
   - Click "🎯 Analyze Fit"
   - View fit score and matching skills
   - Check recommendations

4. **Iterate & Improve**
   - Edit CV based on recommendations
   - Save updated version
   - Reanalyze for new positions

### Example 3: Compare Multiple Jobs

1. **Save Base CV**
   - Save your complete CV

2. **For Each Job:**
   - Paste job description
   - Click "Analyze Fit"
   - Note fit score and missing skills

3. **Compare Results**
   - Identify pattern in missing skills
   - Decide which role is best fit
   - Focus improvement efforts

---

## 🔧 Configuration

### Server Configuration
```python
# server.py
DEBUG = os.getenv("FLASK_DEBUG", False)  # Set to True for development
PORT = int(os.getenv("FLASK_PORT", 5000))
UPLOAD_FOLDER = Path("cv_data")
```

### Frontend Configuration
```javascript
// index.html
const API_BASE_URL = 'http://localhost:5000/api';
```

---

## ⚡ Performance Tips

1. **Save CV Regularly**
   - Don't lose work
   - Use unique filenames for versions

2. **Cache Results**
   - Screenshots of analysis results
   - Store recommendations in notes

3. **Batch Analysis**
   - Analyze multiple jobs in one session
   - Compare scores and recommendations

4. **Optimize Descriptions**
   - Use action verbs
   - Include metrics and achievements
   - Keep descriptions concise

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows - Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### API Not Responding
```bash
# Check server is running
# Terminal should show: 🚀 Starting server on http://localhost:5000

# Check GEMINI_API_KEY is set
echo $GEMINI_API_KEY  # Linux/Mac
echo %GEMINI_API_KEY%  # Windows
```

### CORS Errors
- Ensure `flask-cors` is installed
- Frontend and backend running on same machine
- Check browser console for specific errors

### CV Not Saving
- Check `cv_data/` folder exists
- Check file permissions
- Try different filename

---

## 📊 Real-time Scoring Breakdown

### ATS Score Calculation
- **Personal Info** (10 pts) - Name, email, phone, location, LinkedIn
- **Professional Summary** (10 pts) - Clear, detailed overview
- **Experience** (30 pts) - Multiple roles, descriptions with action verbs
- **Education** (15 pts) - Degrees and institutions
- **Skills** (20 pts) - Relevant technical and soft skills
- **Certifications** (10 pts) - Industry recognized certs
- **Formatting** (5 pts) - Clean, no special characters

### Job Fit Calculation
- **Skill Match** - Percentage of required skills present
- **Experience Match** - Relevant job history alignment
- **Education Match** - Relevant degree/field
- **Keyword Density** - Industry-specific keywords
- **Overall Fit** - Combined weighted score

---

## 🚀 Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Set GEMINI_API_KEY
3. ✅ Start server: `python server.py`
4. ✅ Open browser: `file:///path/to/index.html`
5. ✅ Create CV and test features
6. ✅ Analyze jobs and compare fits
7. ✅ Save and reload CVs
8. ✅ Share with friends!

---

## 📚 Documentation Files

- **README.md** - Project overview
- **JOBFIT_GUIDE.md** - Job Fit feature details
- **JOBFIT_IMPLEMENTATION.md** - Implementation summary
- **SETUP_GUIDE.py** - Step-by-step setup
- **This file** - Full-stack architecture guide

---

## 🎯 Key Features Summary

| Feature | Status | Location |
|---------|--------|----------|
| CV Editor | ✅ Complete | index.html (left panel) |
| Save/Load CV | ✅ Complete | Storage tab |
| Real-time ATS Score | ✅ Complete | Analysis tab |
| Job Fit Analyzer | ✅ Complete | Job Fit tab |
| API Backend | ✅ Complete | server.py |
| Responsive Design | ✅ Complete | index.html (CSS) |
| Error Handling | ✅ Complete | Frontend + Backend |
| Local Storage | ✅ Complete | cv_data/ folder |

---

## 🌟 Tips for Best Results

1. **Comprehensive CV**
   - Include all relevant experience
   - Add multiple skills
   - Detail achievements with metrics

2. **Good Job Descriptions**
   - Paste complete job posting
   - Include requirements section
   - Mention skills and responsibilities

3. **Action-Oriented Content**
   - Use strong action verbs
   - Quantify achievements
   - Show impact and results

4. **Regular Updates**
   - Keep CV current
   - Add new skills and certifications
   - Update with recent projects

---

*Last Updated: May 3, 2026*
*Version: 2.0 - Full-Stack Architecture*
*Status: ✅ READY FOR PRODUCTION*
