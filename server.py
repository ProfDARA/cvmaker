"""
Flask API Server untuk CV Maker dengan Job Fit Analyzer

Endpoints:
- POST /api/cv/analyze-ats - Analyze ATS score dari CV data
- POST /api/job/analyze-fit - Analyze job fit
- GET /api/health - Health check
"""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from CVmaker import CVData, CVMaker, JobFitAnalyzer, ATSOptimizer
from datetime import datetime
import re

# OCR imports (optional at runtime)
try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
    from PyPDF2 import PdfReader
    OCR_AVAILABLE = True
except Exception:
    # If OCR libs or system deps (poppler, tesseract) not available, fall back to text extraction only
    OCR_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Configuration
DEBUG = os.getenv("FLASK_DEBUG", False)
PORT = int(os.getenv("FLASK_PORT", 5000))
UPLOAD_FOLDER = Path("cv_data")
UPLOAD_FOLDER.mkdir(exist_ok=True)


class APIResponse:
    """Helper class untuk format response API"""
    
    @staticmethod
    def success(data, message="Success", status=200):
        """Return success response"""
        return jsonify({
            "status": "success",
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }), status
    
    @staticmethod
    def error(message, status=400, data=None):
        """Return error response"""
        return jsonify({
            "status": "error",
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }), status


# ==================== ROUTES ====================

@app.route("/", methods=["GET"])
def index():
    """Redirect ke frontend"""
    return jsonify({
        "status": "running",
        "message": "CV Maker API Server",
        "version": "2.0",
        "docs": "Visit /api/docs untuk API documentation",
        "frontend": "Open index.html in browser"
    })


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    try:
        # Try initialize CV Maker
        cv_maker = CVMaker()
        return APIResponse.success({"status": "healthy", "api_key_set": True})
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            return APIResponse.error(
                "GEMINI_API_KEY not configured",
                status=503,
                data={"configured": False}
            )
        return APIResponse.error(str(e), status=500)


@app.route("/api/cv/analyze-ats", methods=["POST"])
def analyze_ats():
    """
    Analyze CV untuk ATS score
    
    Request body:
    {
        "personal_info": {...},
        "professional_summary": "...",
        "experience": [...],
        "education": [...],
        "skills": [...],
        "certifications": [...]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return APIResponse.error("No JSON data provided", status=400)
        
        # Convert JSON ke CVData object
        cv = CVData()
        cv.personal_info = data.get("personal_info", {})
        cv.professional_summary = data.get("professional_summary", "")
        cv.experience = data.get("experience", [])
        cv.education = data.get("education", [])
        cv.skills = data.get("skills", [])
        cv.certifications = data.get("certifications", [])
        cv.languages = data.get("languages", [])
        cv.projects = data.get("projects", [])
        
        # Optimize untuk ATS
        cv_maker = CVMaker()
        
        # Calculate ATS score based on various factors
        ats_score = calculate_ats_score(cv)
        
        # Optimize content
        optimized_experience = []
        for exp in cv.experience:
            optimized_exp = exp.copy()
            optimized_exp['description'] = ATSOptimizer.add_ats_keywords(
                exp.get('description', '')
            )
            optimized_exp['description'] = ATSOptimizer.optimize_formatting(
                optimized_exp['description']
            )
            optimized_experience.append(optimized_exp)
        
        # Get optimization suggestions
        suggestions = get_ats_suggestions(cv, ats_score)
        
        return APIResponse.success({
            "ats_score": ats_score,
            "level": get_ats_level(ats_score),
            "suggestions": suggestions,
            "optimized_cv": {
                "personal_info": cv.personal_info,
                "professional_summary": cv.professional_summary,
                "experience": optimized_experience,
                "education": cv.education,
                "skills": cv.skills,
                "certifications": cv.certifications
            }
        }, message="ATS analysis completed")
    
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            return APIResponse.error("GEMINI_API_KEY not configured", status=503)
        return APIResponse.error(str(e), status=400)
    
    except Exception as e:
        return APIResponse.error(f"Error analyzing ATS: {str(e)}", status=500)


@app.route("/api/job/analyze-fit", methods=["POST"])
def analyze_job_fit():
    """
    Analyze job fit between CV dan job description
    
    Request body:
    {
        "cv": {...},  // CV data object
        "job_description": "..."  // Job description text
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return APIResponse.error("No JSON data provided", status=400)
        
        cv_data_dict = data.get("cv")
        job_description = data.get("job_description", "")
        
        if not cv_data_dict:
            return APIResponse.error("CV data is required", status=400)
        
        if not job_description:
            return APIResponse.error("Job description is required", status=400)
        
        # Convert JSON ke CVData object
        cv = CVData()
        cv.personal_info = cv_data_dict.get("personal_info", {})
        cv.professional_summary = cv_data_dict.get("professional_summary", "")
        cv.experience = cv_data_dict.get("experience", [])
        cv.education = cv_data_dict.get("education", [])
        cv.skills = cv_data_dict.get("skills", [])
        cv.certifications = cv_data_dict.get("certifications", [])
        cv.languages = cv_data_dict.get("languages", [])
        cv.projects = cv_data_dict.get("projects", [])
        
        # Analyze job fit
        cv_maker = CVMaker()
        cv_maker.cv = cv
        analysis = cv_maker.check_job_fit(job_description)
        
        return APIResponse.success(analysis, message="Job fit analysis completed")
    
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            return APIResponse.error("GEMINI_API_KEY not configured", status=503)
        return APIResponse.error(str(e), status=400)
    
    except Exception as e:
        return APIResponse.error(f"Error analyzing job fit: {str(e)}", status=500)


@app.route("/api/cv/save", methods=["POST"])
def save_cv():
    """
    Save CV data ke file JSON
    
    Request body:
    {
        "filename": "my_cv",  // Optional, default: cv_TIMESTAMP
        "cv_data": {...}      // CV object
    }
    """
    try:
        data = request.get_json()
        cv_data = data.get("cv_data")
        filename = data.get("filename", f"cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        if not cv_data:
            return APIResponse.error("CV data is required", status=400)
        
        # Save to file
        filepath = UPLOAD_FOLDER / f"{filename}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cv_data, f, indent=2, ensure_ascii=False)
        
        return APIResponse.success({
            "filename": filename,
            "filepath": str(filepath),
            "saved_at": datetime.now().isoformat()
        }, message="CV saved successfully")
    
    except Exception as e:
        return APIResponse.error(f"Error saving CV: {str(e)}", status=500)


@app.route("/api/cv/load/<filename>", methods=["GET"])
def load_cv(filename):
    """Load CV data dari file JSON"""
    try:
        # Prefer JSON CV if exists
        json_path = UPLOAD_FOLDER / f"{filename}.json"
        pdf_path = UPLOAD_FOLDER / f"{filename}.pdf"

        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                cv_data = json.load(f)
            return APIResponse.success(cv_data, message="CV loaded successfully (from JSON)")

        # If JSON not found, try PDF (extract text and parse)
        if pdf_path.exists():
            try:
                extracted_text = extract_text_from_pdf(str(pdf_path))
                parsed_cv = parse_cv_text_to_structured(extracted_text)
                # include raw_text for user
                parsed_cv['raw_text'] = extracted_text
                return APIResponse.success(parsed_cv, message="CV loaded successfully (from PDF via OCR/text extraction)")
            except Exception as e:
                return APIResponse.error(f"Error extracting text from PDF: {str(e)}", status=500)

        return APIResponse.error(f"CV file not found: {filename}", status=404)
    
    except Exception as e:
        return APIResponse.error(f"Error loading CV: {str(e)}", status=500)


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF. Try direct text extraction first, then OCR if needed.

    Requires PyPDF2 for text extraction. For OCR, requires pdf2image + pytesseract + poppler + tesseract installed.
    """
    # Try PyPDF2 text extraction
    text_chunks = []
    try:
        if 'PdfReader' in globals():
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                try:
                    page_text = page.extract_text() or ''
                    text_chunks.append(page_text)
                except Exception:
                    continue
    except Exception:
        # ignore and continue to OCR fallback
        pass

    combined = "\n".join([t for t in text_chunks if t])
    # If extraction returned enough text, return it
    if combined and len(combined) > 200:
        return combined

    # Fallback to OCR if available
    if OCR_AVAILABLE:
        images = convert_from_path(pdf_path)
        ocr_texts = []
        for img in images:
            try:
                text = pytesseract.image_to_string(img)
                ocr_texts.append(text)
            except Exception:
                continue
        return "\n".join(ocr_texts)

    # If OCR not available and PyPDF2 failed, return whatever we have (even if short)
    return combined


def parse_cv_text_to_structured(text: str) -> dict:
    """Attempt basic parsing of CV text into structured CV data.

    This is heuristic-based: extracts name (first lines), email, phone, and sections by keywords.
    Falls back to raw_text in fields when uncertain.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    cv = {
        "personal_info": {},
        "professional_summary": "",
        "experience": [],
        "education": [],
        "skills": [],
        "certifications": [],
        "languages": [],
        "projects": []
    }

    # Basic personal info heuristics
    if lines:
        cv['personal_info']['full_name'] = lines[0]

    # Email and phone regex
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone_match = re.search(r"(\+?\d[\d\s\-().]{6,}\d)", text)
    if email_match:
        cv['personal_info']['email'] = email_match.group(0)
    if phone_match:
        cv['personal_info']['phone'] = phone_match.group(0)

    # Attempt to split sections by common headings
    lowered = text.lower()
    # Find summary
    for heading in ["professional summary", "summary", "profile", "about me"]:
        idx = lowered.find(heading)
        if idx != -1:
            # take following 400 chars as summary
            cv['professional_summary'] = text[idx + len(heading):].strip().split('\n\n')[0][:800].strip()
            break

    # Skills: look for "skills" section
    skills_idx = lowered.find("skills")
    if skills_idx != -1:
        # extract a short window after heading
        skills_block = text[skills_idx:skills_idx+400]
        # split by commas or line breaks and filter
        parts = re.split(r'[\n,;•\-]', skills_block)
        skills = [p.strip() for p in parts if len(p.strip())>1 and not p.lower().startswith('skills')]
        cv['skills'] = skills[:50]

    # Experience: try to find lines with years or company keywords
    exp_lines = []
    for ln in lines:
        if re.search(r"\b(\d{4})\b", ln) or any(k in ln.lower() for k in ['company', 'experience', 'worked at', 'engineer','developer','manager']):
            exp_lines.append(ln)
    if exp_lines:
        for e in exp_lines[:10]:
            cv['experience'].append({"title": e, "company":"", "dates":"", "description":e})

    # Education: look for education keywords
    edu_lines = [ln for ln in lines if any(k in ln.lower() for k in ['university', 'bachelor', 'master', 'degree', 'college', 'education'])]
    for e in edu_lines[:5]:
        cv['education'].append({"degree": e, "institution":"", "year":""})

    # If professional_summary still empty, take first paragraph after name
    if not cv['professional_summary'] and len(lines) > 1:
        cv['professional_summary'] = lines[1][:800]

    return cv


@app.route("/api/cv/list", methods=["GET"])
def list_cvs():
    """List semua saved CV files"""
    try:
        cv_files = list(UPLOAD_FOLDER.glob("*.json"))
        
        cvs = []
        for filepath in cv_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    cv_data = json.load(f)
                
                cvs.append({
                    "filename": filepath.stem,
                    "name": cv_data.get("personal_info", {}).get("full_name", "Unknown"),
                    "size": filepath.stat().st_size,
                    "created": datetime.fromtimestamp(filepath.stat().st_ctime).isoformat()
                })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
        
        return APIResponse.success({"count": len(cvs), "cvs": cvs})
    
    except Exception as e:
        return APIResponse.error(f"Error listing CVs: {str(e)}", status=500)


@app.route("/api/cv/delete/<filename>", methods=["DELETE"])
def delete_cv(filename):
    """Delete saved CV file"""
    try:
        filepath = UPLOAD_FOLDER / f"{filename}.json"
        
        if not filepath.exists():
            return APIResponse.error(f"CV file not found: {filename}", status=404)
        
        filepath.unlink()
        return APIResponse.success({"deleted": filename}, message="CV deleted successfully")
    
    except Exception as e:
        return APIResponse.error(f"Error deleting CV: {str(e)}", status=500)


@app.route("/api/docs", methods=["GET"])
def api_docs():
    """API Documentation"""
    docs = {
        "title": "CV Maker API",
        "version": "2.0",
        "endpoints": {
            "POST /api/cv/analyze-ats": {
                "description": "Analyze CV untuk ATS score",
                "params": ["personal_info", "professional_summary", "experience", "education", "skills", "certifications"],
                "returns": ["ats_score", "level", "suggestions", "optimized_cv"]
            },
            "POST /api/job/analyze-fit": {
                "description": "Analyze kecocokan CV dengan job description",
                "params": ["cv", "job_description"],
                "returns": ["fit_score", "fit_level", "matched_skills", "missing_skills", "recommendations"]
            },
            "POST /api/cv/save": {
                "description": "Save CV data ke JSON file",
                "params": ["cv_data", "filename"],
                "returns": ["filename", "filepath", "saved_at"]
            },
            "GET /api/cv/load/{filename}": {
                "description": "Load CV data dari file",
                "params": ["filename"],
                "returns": ["cv_data"]
            },
            "GET /api/cv/list": {
                "description": "List semua saved CV files",
                "returns": ["count", "cvs[]"]
            },
            "DELETE /api/cv/delete/{filename}": {
                "description": "Delete saved CV file",
                "params": ["filename"]
            }
        }
    }
    return jsonify(docs)


# ==================== HELPER FUNCTIONS ====================

def calculate_ats_score(cv_data: CVData) -> int:
    """Calculate ATS score berdasarkan CV data"""
    score = 0
    max_score = 100
    
    # Personal info (10 points)
    personal_info = cv_data.personal_info
    if personal_info.get("full_name"):
        score += 2
    if personal_info.get("email"):
        score += 2
    if personal_info.get("phone"):
        score += 2
    if personal_info.get("location"):
        score += 2
    if personal_info.get("linkedin"):
        score += 2
    
    # Professional summary (10 points)
    if cv_data.professional_summary and len(cv_data.professional_summary) > 50:
        score += 10
    elif cv_data.professional_summary:
        score += 5
    
    # Experience (30 points)
    if cv_data.experience:
        score += min(len(cv_data.experience) * 5, 15)
        
        for exp in cv_data.experience:
            desc = exp.get('description', '')
            if desc and len(desc) > 100:
                score += 2
            if any(verb in desc.lower() for verb in 
                   ["achieved", "managed", "led", "implemented", "developed"]):
                score += 3
    
    # Education (15 points)
    if cv_data.education:
        score += min(len(cv_data.education) * 5, 15)
    
    # Skills (20 points)
    if cv_data.skills:
        score += min(len(cv_data.skills) * 2, 20)
    
    # Certifications (10 points)
    if cv_data.certifications:
        score += min(len(cv_data.certifications) * 3, 10)
    
    # Formatting (5 points)
    all_text = str(cv_data.to_dict())
    if all_text and not any(c in all_text for c in ["◆", "■", "●"]):
        score += 5
    
    return min(score, max_score)


def get_ats_level(score: int) -> str:
    """Get ATS level berdasarkan score"""
    if score >= 80:
        return "EXCELLENT"
    elif score >= 60:
        return "GOOD"
    elif score >= 40:
        return "MODERATE"
    else:
        return "POOR"


def get_ats_suggestions(cv_data: CVData, score: int) -> list:
    """Get improvement suggestions untuk ATS"""
    suggestions = []
    
    # Check personal info
    personal_info = cv_data.personal_info
    if not personal_info.get("email"):
        suggestions.append("Add email address to personal information")
    if not personal_info.get("phone"):
        suggestions.append("Add phone number to personal information")
    if not personal_info.get("linkedin"):
        suggestions.append("Add LinkedIn profile link")
    
    # Check professional summary
    if not cv_data.professional_summary:
        suggestions.append("Add a professional summary (improves ATS score)")
    elif len(cv_data.professional_summary) < 100:
        suggestions.append("Expand professional summary (at least 100 characters)")
    
    # Check experience
    if not cv_data.experience:
        suggestions.append("Add work experience to CV")
    else:
        for i, exp in enumerate(cv_data.experience):
            if not exp.get('description') or len(exp.get('description', '')) < 50:
                suggestions.append(f"Expand description for experience #{i+1}")
    
    # Check education
    if not cv_data.education:
        suggestions.append("Add educational background")
    
    # Check skills
    if not cv_data.skills or len(cv_data.skills) < 5:
        suggestions.append("Add more relevant skills (minimum 5 recommended)")
    
    # Formatting suggestions
    all_text = str(cv_data.to_dict())
    if any(c in all_text for c in ["◆", "■", "●"]):
        suggestions.append("Remove special characters and use simple bullet points")
    
    return suggestions


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return APIResponse.error("Endpoint not found", status=404)


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return APIResponse.error("Internal server error", status=500)


# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CV MAKER API SERVER")
    print("=" * 70)
    print(f"\n🚀 Starting server on http://localhost:{PORT}")
    print("\n📖 Documentation: http://localhost:{PORT}/api/docs")
    print("🌐 Frontend: Open index.html in browser")
    print("\n" + "=" * 70 + "\n")
    
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
