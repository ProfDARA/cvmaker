import os
import json
import re
from datetime import datetime
from typing import Optional, Dict, List
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

# Load environment variables dari .env file
load_dotenv()


class GeminiConfig:
    """Configuration untuk Gemini API"""
    def __init__(self, api_key: Optional[str] = None):
        # Try: parameter -> .env file -> environment variable
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "❌ GEMINI_API_KEY tidak ditemukan.\n\n"
                "Solusi:\n"
                "1. Buat file .env di folder project\n"
                "2. Tambah: GEMINI_API_KEY=your_api_key_here\n"
                "3. Atau set environment variable:\n"
                "   Windows: setx GEMINI_API_KEY \"your_api_key_here\"\n"
                "   Linux/Mac: export GEMINI_API_KEY=\"your_api_key_here\"\n\n"
                "Dapatkan API key dari: https://aistudio.google.com"
            )
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-pro")
        except Exception as e:
            raise ValueError(f"❌ Error mengonfigurasi Gemini API: {e}")
    
    def summarize_text(self, text: str, max_length: int = 150) -> str:
        """Merangkum teks menggunakan Gemini API"""
        prompt = f"""Buatkan ringkasan singkat (maksimal {max_length} kata) dari teks berikut dalam bahasa Indonesia:

{text}

Ringkasan harus fokus pada poin-poin penting dan sesuai untuk CV."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error menggunakan Gemini API: {e}")
            return text[:max_length] + "..." if len(text) > max_length else text
    
    def optimize_cv_content(self, content: str) -> str:
        """Mengoptimalkan konten CV untuk ATS"""
        prompt = f"""Optimalkan konten CV berikut untuk ATS (Applicant Tracking System) dan buat lebih profesional:

{content}

Pedoman:
1. Gunakan keyword industri yang relevan
2. Hindari format kompleks (bullets simple, tidak ada simbol khusus)
3. Gunakan kata kerja aksi yang kuat
4. Buat lebih konkret dan terukur
5. Gunakan bahasa profesional

Berikan hasil yang siap pakai untuk ATS."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error menggunakan Gemini API: {e}")
            return content
    
    def analyze_job_fit(self, cv_content: str, job_description: str) -> Dict:
        """Analisis kecocokan CV dengan job description menggunakan Gemini API"""
        prompt = f"""Analisis kecocokan antara CV dan job description berikut. 

CV:
{cv_content}

JOB DESCRIPTION:
{job_description}

Berikan analisis dalam format JSON dengan struktur berikut:
{{
    "fit_score": <1-100>,
    "fit_level": "<EXCELLENT/GOOD/MODERATE/POOR>",
    "matched_skills": [<list skills yang match>],
    "missing_skills": [<list skills yang tidak ada di CV>],
    "matched_experience": [<list pengalaman relevan>],
    "strengths": [<list kekuatan CV untuk role ini>],
    "weaknesses": [<list kelemahan CV untuk role ini>],
    "recommendations": [<list rekomendasi untuk improve CV>],
    "summary": "<ringkasan overall fit>"
}}

Gunakan bahasa Indonesia. Berikan analisis yang objektif dan terperinci."""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Coba extract JSON dari response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                # Fallback jika parsing gagal
                return {
                    "fit_score": 0,
                    "fit_level": "UNKNOWN",
                    "analysis": response_text
                }
        except Exception as e:
            print(f"Error menganalisis job fit: {e}")
            return {
                "fit_score": 0,
                "fit_level": "ERROR",
                "error": str(e)
            }


class CVData:
    """Model data untuk CV"""
    def __init__(self):
        self.personal_info = {
            "full_name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "website": ""
        }
        self.professional_summary = ""
        self.experience: List[Dict] = []
        self.education: List[Dict] = []
        self.skills: List[str] = []
        self.certifications: List[Dict] = []
        self.languages: List[Dict] = []
        self.projects: List[Dict] = []
    
    def add_experience(self, job_title: str, company: str, start_date: str, 
                      end_date: str, description: str):
        """Tambah pengalaman kerja"""
        self.experience.append({
            "job_title": job_title,
            "company": company,
            "start_date": start_date,
            "end_date": end_date,
            "description": description
        })
    
    def add_education(self, degree: str, institution: str, field: str, graduation_year: str):
        """Tambah pendidikan"""
        self.education.append({
            "degree": degree,
            "institution": institution,
            "field": field,
            "graduation_year": graduation_year
        })
    
    def add_skill(self, skill: str):
        """Tambah skill"""
        if skill not in self.skills:
            self.skills.append(skill)
    
    def add_certification(self, name: str, issuer: str, issue_date: str):
        """Tambah sertifikasi"""
        self.certifications.append({
            "name": name,
            "issuer": issuer,
            "issue_date": issue_date
        })
    
    def to_dict(self) -> Dict:
        """Convert ke dictionary"""
        return {
            "personal_info": self.personal_info,
            "professional_summary": self.professional_summary,
            "experience": self.experience,
            "education": self.education,
            "skills": self.skills,
            "certifications": self.certifications,
            "languages": self.languages,
            "projects": self.projects
        }
    
    def to_json(self, filepath: str):
        """Simpan CV ke JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"CV berhasil disimpan ke {filepath}")
    
    @staticmethod
    def from_json(filepath: str) -> 'CVData':
        """Load CV dari JSON"""
        cv = CVData()
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cv.personal_info = data.get("personal_info", {})
            cv.professional_summary = data.get("professional_summary", "")
            cv.experience = data.get("experience", [])
            cv.education = data.get("education", [])
            cv.skills = data.get("skills", [])
            cv.certifications = data.get("certifications", [])
            cv.languages = data.get("languages", [])
            cv.projects = data.get("projects", [])
        return cv


class ATSOptimizer:
    """Optimasi CV untuk ATS"""
    
    ATS_KEYWORDS = [
        "responsible", "managed", "led", "developed", "implemented",
        "designed", "created", "improved", "increased", "reduced",
        "streamlined", "optimized", "analyzed", "coordinated", "collaborated",
        "team", "project", "process", "system", "solution"
    ]
    
    @staticmethod
    def remove_special_formatting(text: str) -> str:
        """Hapus formatting khusus yang tidak ATS-friendly"""
        # Hapus simbol khusus kecuali yang umum
        text = re.sub(r'[^a-zA-Z0-9\s\-().,;:\'""/&@#+%]', '', text)
        return text
    
    @staticmethod
    def optimize_formatting(text: str) -> str:
        """Optimalkan format untuk ATS"""
        # Gunakan bullet points sederhana
        text = text.replace("•", "-")
        text = text.replace("●", "-")
        text = text.replace("■", "-")
        # Hapus multiple spaces
        text = re.sub(r'\s+', ' ', text)
        return text
    
    @staticmethod
    def add_ats_keywords(experience_description: str) -> str:
        """Tambah action keywords untuk ATS"""
        action_verbs = [
            "Achieved", "Accelerated", "Accomplished", "Advanced",
            "Boosted", "Captured", "Completed", "Delivered",
            "Enhanced", "Established", "Exceeded", "Expanded",
            "Generated", "Improved", "Increased", "Launched",
            "Maximized", "Optimized", "Produced", "Reduced",
            "Resolved", "Spearheaded", "Streamlined", "Strengthened"
        ]
        
        # Check jika sudah ada action verb
        for verb in action_verbs:
            if verb.lower() in experience_description.lower():
                return experience_description
        
        # Tambah action verb jika tidak ada
        if experience_description:
            first_verb = action_verbs[0]
            return f"{first_verb} {experience_description.lower()}"
        return experience_description


class JobFitAnalyzer:
    """Analisis kecocokan CV dengan job description"""
    
    def __init__(self, gemini_config: GeminiConfig):
        """Initialize dengan GeminiConfig instance"""
        self.gemini = gemini_config
    
    @staticmethod
    def load_job_description(filepath: str) -> str:
        """Baca job description dari file txt"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            raise FileNotFoundError(f"File job description tidak ditemukan: {filepath}")
        except Exception as e:
            raise Exception(f"Error membaca file job description: {e}")
    
    def format_cv_for_analysis(self, cv_data: CVData) -> str:
        """Format CV data menjadi string untuk analisis"""
        cv_text = []
        
        # Personal Info
        pi = cv_data.personal_info
        cv_text.append(f"Nama: {pi.get('full_name', '')}")
        cv_text.append(f"Email: {pi.get('email', '')}")
        cv_text.append(f"Phone: {pi.get('phone', '')}")
        cv_text.append(f"Location: {pi.get('location', '')}")
        
        # Professional Summary
        if cv_data.professional_summary:
            cv_text.append(f"\nProfessional Summary:\n{cv_data.professional_summary}")
        
        # Skills
        if cv_data.skills:
            cv_text.append(f"\nSkills: {', '.join(cv_data.skills)}")
        
        # Experience
        if cv_data.experience:
            cv_text.append("\nExperience:")
            for exp in cv_data.experience:
                cv_text.append(f"\n{exp['job_title']} at {exp['company']}")
                cv_text.append(f"{exp['start_date']} - {exp['end_date']}")
                cv_text.append(f"Description: {exp['description']}")
        
        # Education
        if cv_data.education:
            cv_text.append("\nEducation:")
            for edu in cv_data.education:
                cv_text.append(f"{edu['degree']} in {edu['field']}")
                cv_text.append(f"{edu['institution']} ({edu['graduation_year']})")
        
        # Certifications
        if cv_data.certifications:
            cv_text.append("\nCertifications:")
            for cert in cv_data.certifications:
                cv_text.append(f"{cert['name']} - {cert['issuer']} ({cert['issue_date']})")
        
        return "\n".join(cv_text)
    
    def analyze_fit(self, cv_data: CVData, job_description: str) -> Dict:
        """Analisis kecocokan CV dengan job description"""
        cv_text = self.format_cv_for_analysis(cv_data)
        return self.gemini.analyze_job_fit(cv_text, job_description)
    
    def analyze_fit_from_file(self, cv_data: CVData, job_file_path: str) -> Dict:
        """Analisis kecocokan CV dengan job description dari file"""
        job_description = self.load_job_description(job_file_path)
        return self.analyze_fit(cv_data, job_description)
    
    def save_fit_analysis(self, analysis: Dict, output_path: str):
        """Simpan hasil analisis ke file JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"Hasil analisis disimpan ke {output_path}")
    
    @staticmethod
    def display_fit_analysis(analysis: Dict):
        """Tampilkan hasil analisis dengan format yang rapi"""
        print("\n" + "=" * 70)
        print("JOB FIT ANALYSIS RESULT")
        print("=" * 70)
        
        if "error" in analysis:
            print(f"❌ Error: {analysis['error']}")
            return
        
        # Fit Score
        fit_score = analysis.get("fit_score", 0)
        fit_level = analysis.get("fit_level", "UNKNOWN")
        
        # Visual score bar
        bar_length = 50
        filled = int(bar_length * fit_score / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(f"\n📊 FIT SCORE: {fit_score}/100 [{bar}]")
        print(f"📈 FIT LEVEL: {fit_level}")
        
        # Summary
        if "summary" in analysis:
            print(f"\n📝 Summary:\n{analysis['summary']}")
        
        # Matched Skills
        if analysis.get("matched_skills"):
            print(f"\n✅ Matched Skills ({len(analysis['matched_skills'])}):")
            for skill in analysis["matched_skills"][:10]:
                print(f"   • {skill}")
            if len(analysis["matched_skills"]) > 10:
                print(f"   ... dan {len(analysis['matched_skills']) - 10} skill lainnya")
        
        # Missing Skills
        if analysis.get("missing_skills"):
            print(f"\n❌ Missing Skills ({len(analysis['missing_skills'])}):")
            for skill in analysis["missing_skills"][:8]:
                print(f"   • {skill}")
            if len(analysis["missing_skills"]) > 8:
                print(f"   ... dan {len(analysis['missing_skills']) - 8} skill lainnya")
        
        # Strengths
        if analysis.get("strengths"):
            print(f"\n💪 Strengths:")
            for strength in analysis["strengths"]:
                print(f"   • {strength}")
        
        # Weaknesses
        if analysis.get("weaknesses"):
            print(f"\n⚠️  Weaknesses:")
            for weakness in analysis["weaknesses"]:
                print(f"   • {weakness}")
        
        # Recommendations
        if analysis.get("recommendations"):
            print(f"\n💡 Recommendations:")
            for rec in analysis["recommendations"]:
                print(f"   • {rec}")
        
        print("\n" + "=" * 70)


class CVExporter:
    """Export CV ke berbagai format"""

    @staticmethod
    def export_to_pdf(cv_data: CVData, output_path: str):
        """Export ke PDF ATS-friendly standar"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CVTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            spaceAfter=10,
            alignment=TA_LEFT,
        )
        header_style = ParagraphStyle(
            "CVHeader",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            spaceBefore=10,
            spaceAfter=6,
            textColor="#111111",
            alignment=TA_LEFT,
        )
        body_style = ParagraphStyle(
            "CVBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            spaceAfter=4,
            alignment=TA_LEFT,
        )
        small_style = ParagraphStyle(
            "CVSmall",
            parent=body_style,
            fontSize=8.8,
            leading=11,
        )

        story = []
        pi = cv_data.personal_info
        full_name = pi.get("full_name", "").strip() or "CV ATS Maker"
        story.append(Paragraph(full_name, title_style))

        contact_parts = [
            pi.get("email", "").strip(),
            pi.get("phone", "").strip(),
            pi.get("location", "").strip(),
            pi.get("linkedin", "").strip(),
            pi.get("website", "").strip(),
        ]
        contact_text = " | ".join([part for part in contact_parts if part])
        if contact_text:
            story.append(Paragraph(contact_text, small_style))

        if cv_data.professional_summary:
            story.append(Paragraph("Professional Summary", header_style))
            story.append(Paragraph(cv_data.professional_summary, body_style))

        if cv_data.experience:
            story.append(Paragraph("Experience", header_style))
            for exp in cv_data.experience:
                title = f"{exp.get('job_title', '')} - {exp.get('company', '')}"
                period = f"{exp.get('start_date', '')} - {exp.get('end_date', '')}"
                story.append(Paragraph(title, body_style))
                story.append(Paragraph(period, small_style))
                story.append(Paragraph(f"- {exp.get('description', '')}", body_style))

        if cv_data.education:
            story.append(Paragraph("Education", header_style))
            for edu in cv_data.education:
                education_line = f"{edu.get('degree', '')} in {edu.get('field', '')} - {edu.get('institution', '')} ({edu.get('graduation_year', '')})"
                story.append(Paragraph(education_line, body_style))

        if cv_data.skills:
            story.append(Paragraph("Skills", header_style))
            story.append(Paragraph(", ".join(cv_data.skills), body_style))

        if cv_data.certifications:
            story.append(Paragraph("Certifications", header_style))
            for cert in cv_data.certifications:
                cert_line = f"{cert.get('name', '')} - {cert.get('issuer', '')} ({cert.get('issue_date', '')})"
                story.append(Paragraph(cert_line, body_style))

        doc.build(story)
    
    @staticmethod
    def export_to_plain_text(cv_data: CVData, output_path: str):
        """Export ke plain text (ATS-friendly)"""
        content = []
        
        # Header
        pi = cv_data.personal_info
        content.append(pi["full_name"].upper())
        if pi["email"]:
            content.append(f"Email: {pi['email']}")
        if pi["phone"]:
            content.append(f"Phone: {pi['phone']}")
        if pi["location"]:
            content.append(f"Location: {pi['location']}")
        if pi["linkedin"]:
            content.append(f"LinkedIn: {pi['linkedin']}")
        content.append("---")
        
        # Professional Summary
        if cv_data.professional_summary:
            content.append("\nPROFESSIONAL SUMMARY")
            content.append(cv_data.professional_summary)
        
        # Experience
        if cv_data.experience:
            content.append("\nEXPERIENCE")
            for exp in cv_data.experience:
                content.append(f"\n{exp['job_title']} at {exp['company']}")
                content.append(f"{exp['start_date']} - {exp['end_date']}")
                content.append(exp['description'])
        
        # Education
        if cv_data.education:
            content.append("\nEDUCATION")
            for edu in cv_data.education:
                content.append(f"\n{edu['degree']} in {edu['field']}")
                content.append(f"{edu['institution']} ({edu['graduation_year']})")
        
        # Skills
        if cv_data.skills:
            content.append("\nSKILLS")
            content.append(", ".join(cv_data.skills))
        
        # Certifications
        if cv_data.certifications:
            content.append("\nCERTIFICATIONS")
            for cert in cv_data.certifications:
                content.append(f"\n{cert['name']} - {cert['issuer']} ({cert['issue_date']})")
        
        # Save
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        print(f"CV berhasil diekspor ke {output_path}")
    
    @staticmethod
    def export_to_json(cv_data: CVData, output_path: str):
        """Export ke JSON format"""
        cv_data.to_json(output_path)


class CVMaker:
    """Main application class"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.gemini = GeminiConfig(api_key)
        self.cv = CVData()
        self.ats_optimizer = ATSOptimizer()
        self.job_fit_analyzer = JobFitAnalyzer(self.gemini)
    
    def create_sample_cv(self) -> CVData:
        """Buat sample CV untuk testing"""
        cv = CVData()
        
        # Personal Info
        cv.personal_info = {
            "full_name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+62-812-3456-7890",
            "location": "Jakarta, Indonesia",
            "linkedin": "linkedin.com/in/johndoe",
            "website": "johndoe.com"
        }
        
        # Professional Summary
        cv.professional_summary = "Experienced Full Stack Developer dengan 5+ tahun pengalaman dalam mengembangkan aplikasi web dan mobile. Ahli dalam Python, JavaScript, dan cloud technologies."
        
        # Experience
        cv.add_experience(
            "Senior Full Stack Developer",
            "Tech Company XYZ",
            "Jan 2022",
            "Present",
            "Led development team of 5 engineers. Designed and implemented microservices architecture using Python and Node.js. Improved application performance by 40% through optimization."
        )
        
        cv.add_experience(
            "Full Stack Developer",
            "Startup ABC",
            "Jun 2020",
            "Dec 2021",
            "Developed and maintained web applications using React and Django. Implemented CI/CD pipeline using GitHub Actions. Collaborated with design team to deliver responsive UI."
        )
        
        # Education
        cv.add_education(
            "Bachelor of Computer Science",
            "University of Indonesia",
            "Computer Science",
            "2020"
        )
        
        # Skills
        skills = ["Python", "JavaScript", "React", "Django", "PostgreSQL", "Docker", 
                 "AWS", "Git", "REST API", "Machine Learning", "Agile"]
        for skill in skills:
            cv.add_skill(skill)
        
        # Certifications
        cv.add_certification(
            "AWS Certified Solutions Architect",
            "Amazon Web Services",
            "2023"
        )
        
        return cv
    
    def summarize_experience(self, experience_description: str) -> str:
        """Rangkum pengalaman kerja"""
        print("Merangkum pengalaman menggunakan Gemini API...")
        return self.gemini.summarize_text(experience_description, max_length=100)
    
    def optimize_cv_for_ats(self) -> CVData:
        """Optimalkan seluruh CV untuk ATS"""
        print("Mengoptimalkan CV untuk ATS...")
        
        # Optimize professional summary
        if self.cv.professional_summary:
            self.cv.professional_summary = self.gemini.optimize_cv_content(
                self.cv.professional_summary
            )
        
        # Optimize experience descriptions
        for exp in self.cv.experience:
            exp['description'] = self.ats_optimizer.add_ats_keywords(exp['description'])
            exp['description'] = self.ats_optimizer.optimize_formatting(exp['description'])
        
        return self.cv
    
    def save_cv(self, filename: str = "cv_output"):
        """Simpan CV dalam berbagai format"""
        output_dir = Path("cv_output")
        output_dir.mkdir(exist_ok=True)
        
        # Export ke text
        text_path = output_dir / f"{filename}.txt"
        CVExporter.export_to_plain_text(self.cv, str(text_path))
        
        # Export ke JSON
        json_path = output_dir / f"{filename}.json"
        CVExporter.export_to_json(self.cv, str(json_path))

        # Export ke PDF
        pdf_path = output_dir / f"{filename}.pdf"
        CVExporter.export_to_pdf(self.cv, str(pdf_path))
        
        print(f"\nCV berhasil disimpan di folder: {output_dir}")
        print(f"- Plain text: {text_path}")
        print(f"- JSON: {json_path}")
        print(f"- PDF: {pdf_path}")


def main():
    """Main function"""
    print("=" * 60)
    print("CV ATS MAKER - Dengan Text Summarizer (Gemini API)")
    print("=" * 60)
    
    try:
        # Initialize CV Maker
        cv_maker = CVMaker()
        
        # Create sample CV
        print("\nMemuat sample CV...")
        cv_maker.cv = cv_maker.create_sample_cv()
        
        # Display CV info
        print("\n[1] Original CV:")
        print("-" * 60)
        print(f"Nama: {cv_maker.cv.personal_info['full_name']}")
        print(f"Email: {cv_maker.cv.personal_info['email']}")
        print(f"Phone: {cv_maker.cv.personal_info['phone']}")
        print(f"\nProfessional Summary:")
        print(cv_maker.cv.professional_summary)
        print(f"\nSkills: {', '.join(cv_maker.cv.skills)}")
        
        # Summarize first experience
        if cv_maker.cv.experience:
            print("\n[2] Merangkum pengalaman pertama...")
            first_exp = cv_maker.cv.experience[0]
            summarized = cv_maker.summarize_experience(first_exp['description'])
            print(f"Original: {first_exp['description']}")
            print(f"Summarized: {summarized}")
        
        # Optimize for ATS
        print("\n[3] Mengoptimalkan CV untuk ATS...")
        cv_maker.optimize_cv_for_ats()
        print("CV berhasil dioptimalkan!")
        
        # Save CV
        print("\n[4] Menyimpan CV...")
        cv_maker.save_cv("my_cv_ats_optimized")
        
        print("\n" + "=" * 60)
        print("CV ATS Maker selesai!")
        print("=" * 60)
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nCara setup:")
        print("1. Dapatkan API key dari https://aistudio.google.com")
        print("2. Set environment variable:")
        print("   Windows: set GEMINI_API_KEY=your_api_key")
        print("   Linux/Mac: export GEMINI_API_KEY=your_api_key")


if __name__ == "__main__":
    main()
