"""
Web Interface untuk CV ATS Maker
Flask-based web application untuk UI yang lebih user-friendly
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
from datetime import datetime
from pathlib import Path
from CVmaker import CVMaker, CVData
import os

BASE_DIR = Path(__file__).resolve().parent
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)
app.config['JSON_AS_ASCII'] = False

# Initialize CV Maker
try:
    cv_maker = CVMaker()
    current_cv = CVData()
except ValueError as e:
    print(f"Error: {e}")
    cv_maker = None


@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')


@app.route('/api/cv/new', methods=['POST'])
def create_new_cv():
    """Create new CV"""
    global current_cv
    current_cv = CVData()
    return jsonify({"status": "success", "message": "CV baru berhasil dibuat"})


@app.route('/api/cv/personal-info', methods=['POST'])
def update_personal_info():
    """Update personal info"""
    global current_cv
    data = request.json
    current_cv.personal_info = {
        "full_name": data.get("full_name", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "location": data.get("location", ""),
        "linkedin": data.get("linkedin", ""),
        "website": data.get("website", "")
    }
    return jsonify({"status": "success", "message": "Personal info berhasil diupdate"})


@app.route('/api/cv/summary', methods=['POST'])
def update_summary():
    """Update professional summary"""
    global current_cv
    data = request.json
    current_cv.professional_summary = data.get("summary", "")
    return jsonify({"status": "success", "message": "Summary berhasil diupdate"})


@app.route('/api/cv/experience', methods=['POST'])
def add_experience():
    """Add experience"""
    global current_cv
    data = request.json
    current_cv.add_experience(
        data.get("job_title"),
        data.get("company"),
        data.get("start_date"),
        data.get("end_date"),
        data.get("description")
    )
    return jsonify({"status": "success", "message": "Experience berhasil ditambahkan"})


@app.route('/api/cv/education', methods=['POST'])
def add_education():
    """Add education"""
    global current_cv
    data = request.json
    current_cv.add_education(
        data.get("degree"),
        data.get("institution"),
        data.get("field"),
        data.get("graduation_year")
    )
    return jsonify({"status": "success", "message": "Education berhasil ditambahkan"})


@app.route('/api/cv/skills', methods=['POST'])
def add_skills():
    """Add skills"""
    global current_cv
    data = request.json
    skills = data.get("skills", "").split(",")
    for skill in skills:
        current_cv.add_skill(skill.strip())
    return jsonify({"status": "success", "message": "Skills berhasil ditambahkan"})


@app.route('/api/cv/preview', methods=['GET'])
def get_cv_preview():
    """Get CV preview"""
    global current_cv
    return jsonify(current_cv.to_dict())


@app.route('/api/cv/summarize', methods=['POST'])
def summarize_experience():
    """Summarize experience text"""
    global cv_maker
    data = request.json
    text = data.get("text", "")
    
    if not cv_maker:
        return jsonify({"error": "Gemini API not configured"}), 500
    
    summary = cv_maker.summarize_experience(text)
    return jsonify({"summary": summary})


@app.route('/api/cv/optimize', methods=['POST'])
def optimize_ats():
    """Optimize CV untuk ATS"""
    global current_cv, cv_maker
    
    if not cv_maker:
        return jsonify({"error": "Gemini API not configured"}), 500
    
    cv_maker.cv = current_cv
    cv_maker.optimize_cv_for_ats()
    current_cv = cv_maker.cv
    
    return jsonify({"status": "success", "message": "CV berhasil dioptimalkan untuk ATS"})


@app.route('/api/cv/save', methods=['POST'])
def save_cv():
    """Save CV"""
    global current_cv, cv_maker
    data = request.json
    filename = data.get("filename", "my_cv")
    
    cv_maker.cv = current_cv
    cv_maker.save_cv(filename)
    
    return jsonify({"status": "success", "message": f"CV berhasil disimpan: {filename}"})


@app.route('/api/cv/load', methods=['POST'])
def load_cv():
    """Load CV from JSON"""
    global current_cv
    data = request.json
    filepath = data.get("filepath")
    
    try:
        current_cv = CVData.from_json(filepath)
        return jsonify({"status": "success", "message": "CV berhasil dimuat"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/cv/sample', methods=['POST'])
def load_sample():
    """Load sample CV"""
    global current_cv, cv_maker
    current_cv = cv_maker.create_sample_cv()
    return jsonify(current_cv.to_dict())


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    gemini_ok = cv_maker is not None
    return jsonify({
        "status": "ok" if gemini_ok else "error",
        "gemini_configured": gemini_ok,
        "timestamp": datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({"error": "Endpoint tidak ditemukan"}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({"error": "Internal server error"}), 500


def create_app():
    """Application factory"""
    return app


if __name__ == '__main__':
    print("\n" + "="*60)
    print("CV ATS Maker - Web Interface")
    print("="*60)
    print("\n🚀 Server running on http://localhost:5000")
    print("📖 Buka browser dan kunjungi http://localhost:5000")
    print("\nTekan Ctrl+C untuk stop server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
