"""
Flask API Server untuk CV Maker dengan Job Fit Analyzer

Endpoints:
- POST /api/cv/analyze-ats - Analyze ATS score dari CV data
- POST /api/job/analyze-fit - Analyze job fit
- GET /api/health - Health check
"""

import os
import json
from typing import Any, Optional, Dict, List, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
from pathlib import Path
from CVmaker import CVData, CVMaker, JobFitAnalyzer, ATSOptimizer
from datetime import datetime
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

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
    """Serve frontend index.html if available, otherwise return API status."""
    index_path = Path("index.html")
    if index_path.exists():
        return send_file(str(index_path))
    return jsonify({
        "status": "running",
        "message": "CV Maker API Server",
        "version": "2.0",
        "docs": "Visit /api/docs untuk API documentation",
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


@app.route("/api/linkedin/fetch", methods=["POST"])
def fetch_linkedin_profile():
    """Fetch data dari public LinkedIn profile URL dan ubah ke struktur CV."""
    try:
        data = request.get_json() or {}
        linkedin_url = (data.get("url") or "").strip()

        if not linkedin_url:
            return APIResponse.error("LinkedIn URL is required", status=400)

        normalized_url = normalize_linkedin_url(linkedin_url)
        response = requests.get(
            normalized_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            timeout=20,
        )

        if response.status_code in {401, 403, 429, 999}:
            return APIResponse.error(
                "LinkedIn membatasi akses ke profil ini. Pastikan URL mengarah ke profil publik yang bisa dibuka tanpa login.",
                status=502,
                data={"status_code": response.status_code},
            )

        response_text_lower = response.text.lower()
        if any(marker in response_text_lower for marker in ["sign in", "join linkedin", "authwall", "checkpoint"]) and "linkedin" in response_text_lower:
            return APIResponse.error(
                "LinkedIn page terlihat meminta login. Gunakan public profile URL yang benar-benar bisa dibuka tanpa masuk akun.",
                status=502,
            )

        response.raise_for_status()

        cv_data, profile_meta = parse_linkedin_profile_html(response.text, normalized_url)

        return APIResponse.success(
            {
                "source_url": normalized_url,
                "resolved_url": response.url,
                "profile_meta": profile_meta,
                "cv_data": cv_data,
            },
            message="LinkedIn profile fetched successfully",
        )

    except ValueError as e:
        return APIResponse.error(str(e), status=400)
    except requests.RequestException as e:
        return APIResponse.error(f"Error fetching LinkedIn profile: {str(e)}", status=502)
    except Exception as e:
        return APIResponse.error(f"Error fetching LinkedIn profile: {str(e)}", status=500)


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


def normalize_linkedin_url(linkedin_url: str) -> str:
    """Normalize LinkedIn URL agar bisa difetch dengan konsisten."""
    cleaned_url = linkedin_url.strip()
    if not cleaned_url:
        raise ValueError("LinkedIn URL is required")

    if not cleaned_url.startswith(("http://", "https://")):
        cleaned_url = f"https://{cleaned_url}"

    parsed_url = urlparse(cleaned_url)
    if "linkedin.com" not in parsed_url.netloc.lower():
        raise ValueError("URL harus mengarah ke domain linkedin.com")

    profile_match = re.match(r"^/(in|pub)/[^/]+", parsed_url.path)
    normalized_path = profile_match.group(0) if profile_match else parsed_url.path.rstrip("/")
    if not normalized_path:
        raise ValueError("LinkedIn profile path is required")

    return f"{parsed_url.scheme}://{parsed_url.netloc}{normalized_path}"


def extract_json_ld_objects(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract JSON-LD objects from a LinkedIn HTML document."""
    objects: List[Dict[str, Any]] = []

    for script_tag in soup.find_all("script", type="application/ld+json"):
        raw_text = (script_tag.string or script_tag.get_text() or "").strip()
        if not raw_text:
            continue

        try:
            parsed_json = json.loads(raw_text)
        except json.JSONDecodeError:
            continue

        if isinstance(parsed_json, list):
            objects.extend([item for item in parsed_json if isinstance(item, dict)])
        elif isinstance(parsed_json, dict):
            objects.append(parsed_json)

    return objects


def first_non_empty(*values: Optional[str]) -> str:
    for value in values:
        if value and str(value).strip():
            return str(value).strip()
    return ""


def build_linkedin_profile_meta(soup: BeautifulSoup, page_url: str) -> dict:
    """Collect basic metadata from a LinkedIn profile page."""
    meta_tags = {
        tag.get("property") or tag.get("name"): tag.get("content", "")
        for tag in soup.find_all("meta")
        if tag.get("content")
    }

    json_ld_objects = extract_json_ld_objects(soup)
    person_object = next(
        (
            item
            for item in json_ld_objects
            if any(str(type_name).lower() in {"person", "profilepage"} for type_name in (item.get("@type", []) if isinstance(item.get("@type", []), list) else [item.get("@type", "")]))
        ),
        {},
    )

    og_title = meta_tags.get("og:title", "")
    og_description = meta_tags.get("og:description", "")
    page_title = soup.title.get_text(strip=True) if soup.title else ""

    full_name = first_non_empty(
        person_object.get("name"),
        og_title.split("|")[0].split("-")[0] if og_title else "",
        page_title.split("|")[0].split("-")[0] if page_title else "",
    )

    headline = first_non_empty(
        person_object.get("headline"),
        og_description,
        meta_tags.get("description", ""),
    )

    return {
        "full_name": full_name,
        "headline": headline,
        "image": first_non_empty(person_object.get("image"), meta_tags.get("og:image", "")),
        "url": first_non_empty(person_object.get("url"), page_url),
        "same_as": person_object.get("sameAs", []),
        "raw_title": page_title,
        "raw_description": meta_tags.get("description", ""),
        "og_title": og_title,
        "og_description": og_description,
    }


def parse_linkedin_profile_html(html: str, page_url: str) -> Tuple[dict, dict]:
    """Parse public LinkedIn HTML into CV-shaped data.

    This is best-effort only and works only for profiles that are publicly accessible.
    """
    soup = BeautifulSoup(html, "html.parser")
    profile_meta = build_linkedin_profile_meta(soup, page_url)

    page_text = soup.get_text("\n", strip=True)
    main_tag = soup.find("main")
    if main_tag:
        main_text = main_tag.get_text("\n", strip=True)
        if len(main_text) > len(page_text) * 0.5:
            page_text = main_text

    parsed_cv = parse_cv_text_to_structured(page_text)

    parsed_cv["personal_info"] = parsed_cv.get("personal_info", {}) or {}
    parsed_cv["personal_info"]["full_name"] = first_non_empty(
        profile_meta.get("full_name"),
        parsed_cv["personal_info"].get("full_name", ""),
    )
    parsed_cv["personal_info"]["linkedin"] = page_url
    parsed_cv["professional_summary"] = first_non_empty(
        profile_meta.get("headline"),
        parsed_cv.get("professional_summary", ""),
    )

    if profile_meta.get("headline") and not parsed_cv.get("skills"):
        headline_parts = [part.strip() for part in re.split(r"[|,/]", profile_meta["headline"]) if part.strip()]
        parsed_cv["skills"] = headline_parts[:12]

    parsed_cv["experience"] = ensure_items_have_ids(parsed_cv.get("experience", []), "experience")
    parsed_cv["education"] = ensure_items_have_ids(parsed_cv.get("education", []), "education")

    return parsed_cv, profile_meta


def ensure_items_have_ids(items: List[Dict[str, Any]], item_type: str) -> List[Dict[str, Any]]:
    """Ensure experience and education entries are editable in the UI."""
    normalized_items = []
    for index, item in enumerate(items or []):
        normalized_item = dict(item)
        if normalized_item.get("id") is None:
            normalized_item["id"] = index

        if item_type == "experience":
            normalized_item["job_title"] = first_non_empty(
                normalized_item.get("job_title"),
                normalized_item.get("title"),
                normalized_item.get("position"),
            )
            normalized_item["company"] = first_non_empty(normalized_item.get("company"))
            normalized_item["start_date"] = first_non_empty(normalized_item.get("start_date"), normalized_item.get("dates"))
            normalized_item["end_date"] = first_non_empty(normalized_item.get("end_date"))
            normalized_item["description"] = first_non_empty(normalized_item.get("description"))
        elif item_type == "education":
            normalized_item["degree"] = first_non_empty(normalized_item.get("degree"))
            normalized_item["institution"] = first_non_empty(normalized_item.get("institution"))
            normalized_item["field"] = first_non_empty(normalized_item.get("field"))
            normalized_item["graduation_year"] = first_non_empty(
                normalized_item.get("graduation_year"),
                normalized_item.get("year"),
            )

        normalized_items.append(normalized_item)

    return normalized_items


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
            "POST /api/linkedin/fetch": {
                "description": "Fetch data dari public LinkedIn profile URL",
                "params": ["url"],
                "returns": ["source_url", "resolved_url", "profile_meta", "cv_data"]
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
