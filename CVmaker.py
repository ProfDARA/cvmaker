import os
import json
import re
from datetime import datetime
from typing import Optional, Dict, List
import google.generativeai as genai
from pathlib import Path


class GeminiConfig:
    """Configuration untuk Gemini API"""
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan. Silakan set environment variable atau pass api_key.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")
    
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
        text = re.sub(r'[^a-zA-Z0-9\s\-().,;:\''"/&@#+%]', '', text)
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


class CVExporter:
    """Export CV ke berbagai format"""
    
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
        
        print(f"\nCV berhasil disimpan di folder: {output_dir}")
        print(f"- Plain text: {text_path}")
        print(f"- JSON: {json_path}")


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
