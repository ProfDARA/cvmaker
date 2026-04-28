"""
CLI Interface untuk CV ATS Maker
Interactive command-line interface untuk aplikasi CV ATS Maker
"""

import sys
import os
from pathlib import Path
from CVmaker import CVMaker, CVData
from config import GEMINI_API_KEY


class CVMakerCLI:
    """CLI Interface untuk CV ATS Maker"""
    
    def __init__(self):
        self.cv_maker = None
        self.current_cv = None
        
        try:
            self.cv_maker = CVMaker(api_key=GEMINI_API_KEY)
            self.current_cv = CVData()
        except ValueError as e:
            print(f"❌ Error: {e}")
            print("\n📖 Cara setup:")
            print("1. Dapatkan API key dari https://aistudio.google.com")
            print("2. Set environment variable:")
            print("   Windows: setx GEMINI_API_KEY your_api_key")
            print("   Linux/Mac: export GEMINI_API_KEY=your_api_key")
            sys.exit(1)
    
    def display_menu(self):
        """Tampilkan main menu"""
        print("\n" + "="*60)
        print("CV ATS MAKER - Interactive CLI")
        print("="*60)
        print("\n📋 Main Menu:")
        print("1. ➕ Tambah Personal Info")
        print("2. ➕ Tambah Experience")
        print("3. ➕ Tambah Education")
        print("4. ➕ Tambah Skills")
        print("5. ➕ Tambah Certification")
        print("6. 📄 Lihat CV Preview")
        print("7. 🧠 Rangkum Experience dengan Gemini")
        print("8. ✨ Optimize CV untuk ATS")
        print("9. 💾 Simpan CV")
        print("10. 📂 Load CV dari JSON")
        print("11. 📋 Load Sample CV")
        print("0. ❌ Exit")
        print("\n" + "-"*60)
    
    def add_personal_info(self):
        """Tambah personal info"""
        print("\n📝 Tambah Personal Information:")
        name = input("Nama lengkap: ").strip()
        email = input("Email: ").strip()
        phone = input("Nomor telepon: ").strip()
        location = input("Lokasi: ").strip()
        linkedin = input("LinkedIn URL (optional): ").strip()
        website = input("Website (optional): ").strip()
        
        self.current_cv.personal_info = {
            "full_name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "website": website
        }
        print("✓ Personal info berhasil ditambahkan")
    
    def add_experience(self):
        """Tambah experience"""
        print("\n💼 Tambah Experience:")
        job_title = input("Job title: ").strip()
        company = input("Nama perusahaan: ").strip()
        start_date = input("Start date (e.g., Jan 2022): ").strip()
        end_date = input("End date (e.g., Dec 2023) atau 'Present': ").strip()
        description = input("Deskripsi singkat: ").strip()
        
        self.current_cv.add_experience(job_title, company, start_date, end_date, description)
        print("✓ Experience berhasil ditambahkan")
    
    def add_education(self):
        """Tambah education"""
        print("\n🎓 Tambah Education:")
        degree = input("Degree (e.g., Bachelor, Master): ").strip()
        institution = input("Nama institusi: ").strip()
        field = input("Field of study: ").strip()
        year = input("Graduation year: ").strip()
        
        self.current_cv.add_education(degree, institution, field, year)
        print("✓ Education berhasil ditambahkan")
    
    def add_skills(self):
        """Tambah skills"""
        print("\n🛠️ Tambah Skills:")
        print("Masukkan skills (pisahkan dengan koma):")
        skills_input = input("Skills: ").strip()
        
        for skill in skills_input.split(","):
            self.current_cv.add_skill(skill.strip())
        
        print("✓ Skills berhasil ditambahkan")
    
    def add_certification(self):
        """Tambah certification"""
        print("\n🏆 Tambah Certification:")
        name = input("Nama sertifikasi: ").strip()
        issuer = input("Penerbit: ").strip()
        date = input("Tanggal: ").strip()
        
        self.current_cv.certifications.append({
            "name": name,
            "issuer": issuer,
            "issue_date": date
        })
        print("✓ Certification berhasil ditambahkan")
    
    def show_cv_preview(self):
        """Tampilkan preview CV"""
        print("\n" + "="*60)
        print("📄 CV PREVIEW")
        print("="*60)
        
        pi = self.current_cv.personal_info
        print(f"\nNAMA: {pi.get('full_name', 'N/A')}")
        print(f"Email: {pi.get('email', 'N/A')}")
        print(f"Phone: {pi.get('phone', 'N/A')}")
        print(f"Location: {pi.get('location', 'N/A')}")
        
        if self.current_cv.experience:
            print("\n💼 EXPERIENCE:")
            for i, exp in enumerate(self.current_cv.experience, 1):
                print(f"\n  {i}. {exp['job_title']} at {exp['company']}")
                print(f"     {exp['start_date']} - {exp['end_date']}")
                print(f"     {exp['description']}")
        
        if self.current_cv.education:
            print("\n🎓 EDUCATION:")
            for i, edu in enumerate(self.current_cv.education, 1):
                print(f"\n  {i}. {edu['degree']} in {edu['field']}")
                print(f"     {edu['institution']} ({edu['graduation_year']})")
        
        if self.current_cv.skills:
            print(f"\n🛠️ SKILLS: {', '.join(self.current_cv.skills)}")
    
    def summarize_experience(self):
        """Rangkum experience menggunakan Gemini"""
        if not self.current_cv.experience:
            print("❌ Tidak ada experience yang bisa dirangkum")
            return
        
        print("\n📝 Pilih experience yang akan dirangkum:")
        for i, exp in enumerate(self.current_cv.experience, 1):
            print(f"{i}. {exp['job_title']} at {exp['company']}")
        
        try:
            choice = int(input("\nPilih nomor: ")) - 1
            if 0 <= choice < len(self.current_cv.experience):
                exp = self.current_cv.experience[choice]
                print("\n🧠 Merangkum dengan Gemini API...")
                summary = self.cv_maker.summarize_experience(exp['description'])
                print(f"\nOriginal: {exp['description']}")
                print(f"Summary: {summary}")
                
                update = input("\nGunakan ringkasan ini? (y/n): ").strip().lower()
                if update == 'y':
                    exp['description'] = summary
                    print("✓ Experience berhasil diupdate")
            else:
                print("❌ Pilihan tidak valid")
        except ValueError:
            print("❌ Input tidak valid")
    
    def optimize_for_ats(self):
        """Optimize CV untuk ATS"""
        print("\n✨ Mengoptimalkan CV untuk ATS...")
        self.cv_maker.cv = self.current_cv
        self.cv_maker.optimize_cv_for_ats()
        self.current_cv = self.cv_maker.cv
        print("✓ CV berhasil dioptimalkan untuk ATS")
    
    def save_cv(self):
        """Simpan CV"""
        filename = input("\nMasukkan nama file (tanpa extension): ").strip()
        if filename:
            self.cv_maker.cv = self.current_cv
            self.cv_maker.save_cv(filename)
            print(f"✓ CV berhasil disimpan sebagai {filename}")
        else:
            print("❌ Nama file tidak valid")
    
    def load_cv_from_json(self):
        """Load CV dari JSON"""
        filepath = input("\nMasukkan path file JSON: ").strip()
        try:
            self.current_cv = CVData.from_json(filepath)
            print("✓ CV berhasil dimuat")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def load_sample_cv(self):
        """Load sample CV"""
        print("\n📋 Loading sample CV...")
        self.cv_maker.cv = self.cv_maker.create_sample_cv()
        self.current_cv = self.cv_maker.cv
        print("✓ Sample CV berhasil dimuat")
        self.show_cv_preview()
    
    def run(self):
        """Run CLI interface"""
        print("\n")
        print("╔" + "="*58 + "╗")
        print("║" + " "*58 + "║")
        print("║" + "  CV ATS Maker - Interactive CLI".center(58) + "║")
        print("║" + " "*58 + "║")
        print("╚" + "="*58 + "╝")
        
        while True:
            self.display_menu()
            choice = input("Pilih menu (0-11): ").strip()
            
            if choice == "0":
                print("\n👋 Terima kasih telah menggunakan CV ATS Maker!")
                break
            elif choice == "1":
                self.add_personal_info()
            elif choice == "2":
                self.add_experience()
            elif choice == "3":
                self.add_education()
            elif choice == "4":
                self.add_skills()
            elif choice == "5":
                self.add_certification()
            elif choice == "6":
                self.show_cv_preview()
            elif choice == "7":
                self.summarize_experience()
            elif choice == "8":
                self.optimize_for_ats()
            elif choice == "9":
                self.save_cv()
            elif choice == "10":
                self.load_cv_from_json()
            elif choice == "11":
                self.load_sample_cv()
            else:
                print("❌ Pilihan tidak valid")


def main():
    """Main entry point"""
    cli = CVMakerCLI()
    cli.run()


if __name__ == "__main__":
    main()
