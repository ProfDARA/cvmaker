"""
Contoh penggunaan CV ATS Maker
"""

from CVmaker import CVMaker, CVData


def example_1_basic_usage():
    """Contoh 1: Penggunaan dasar"""
    print("\n" + "="*60)
    print("CONTOH 1: Penggunaan Dasar")
    print("="*60)
    
    try:
        # Initialize
        cv_maker = CVMaker()
        
        # Add personal info
        cv_maker.cv.personal_info = {
            "full_name": "Budi Santoso",
            "email": "budi@example.com",
            "phone": "+62-851-1234-5678",
            "location": "Bandung, Jawa Barat",
            "linkedin": "linkedin.com/in/budisantoso",
            "website": "budisantoso.com"
        }
        
        # Add professional summary
        cv_maker.cv.professional_summary = (
            "Web Developer berpengalaman 3 tahun di industri teknologi. "
            "Spesialisasi di full-stack development dengan fokus pada Python dan JavaScript. "
            "Passionate tentang clean code dan best practices."
        )
        
        # Add experience
        cv_maker.cv.add_experience(
            job_title="Full Stack Developer",
            company="PT Digital Inovasi",
            start_date="Mar 2021",
            end_date="Present",
            description="Develop dan maintain aplikasi web menggunakan Django dan React. Improved application performance by optimizing database queries. Collaborated dengan team untuk deliver features on time."
        )
        
        # Add education
        cv_maker.cv.add_education(
            degree="Bachelor of Science",
            institution="Universitas Telkom",
            field="Informatics",
            graduation_year="2021"
        )
        
        # Add skills
        skills = ["Python", "JavaScript", "React", "Django", "PostgreSQL", 
                  "Docker", "Git", "HTML/CSS", "RESTful API"]
        for skill in skills:
            cv_maker.cv.add_skill(skill)
        
        # Optimize dan save
        cv_maker.optimize_cv_for_ats()
        cv_maker.save_cv("contoh_1_basic_cv")
        
        print("✓ CV berhasil dibuat dan disimpan")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_2_text_summarization():
    """Contoh 2: Text Summarization"""
    print("\n" + "="*60)
    print("CONTOH 2: Text Summarization dengan Gemini")
    print("="*60)
    
    try:
        cv_maker = CVMaker()
        
        # Long description
        long_description = """
        Bertanggung jawab penuh atas pengembangan dan pemeliharaan aplikasi web enterprise.
        Merancang dan mengimplementasikan microservices architecture menggunakan Python FastAPI.
        Mengoptimalkan database queries yang meningkatkan performa aplikasi hingga 50%.
        Memimpin tim development sebanyak 5 orang engineers untuk deliver project tepat waktu.
        Mengimplementasikan CI/CD pipeline menggunakan GitHub Actions dan Docker.
        Berkolaborasi dengan product team, design team, dan stakeholders untuk menentukan requirements.
        Mentoring junior developers dan best practices dalam development.
        """
        
        print("\nDeskripsi Original:")
        print(long_description)
        
        # Summarize
        print("\nMerangkum dengan Gemini API...")
        summary = cv_maker.summarize_experience(long_description)
        
        print("\nDeskripsi yang Dirangkum:")
        print(summary)
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_3_load_and_modify():
    """Contoh 3: Load dan modify CV"""
    print("\n" + "="*60)
    print("CONTOH 3: Load dan Modifikasi CV dari JSON")
    print("="*60)
    
    try:
        # Load existing CV
        print("Loading CV dari JSON...")
        cv = CVData.from_json("cv_output/contoh_1_basic_cv.json")
        
        # Modify
        cv.add_skill("Kubernetes")
        cv.add_skill("AWS Lambda")
        
        # Add new experience
        cv.add_experience(
            job_title="Junior Developer",
            company="Startup XYZ",
            start_date="Jun 2020",
            end_date="Feb 2021",
            description="Developed web components using React. Fixed bugs dan implemented features."
        )
        
        # Save modified CV
        cv.to_json("cv_output/contoh_3_modified_cv.json")
        
        print("✓ CV berhasil dimodifikasi dan disimpan")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_4_ats_optimization():
    """Contoh 4: ATS Optimization"""
    print("\n" + "="*60)
    print("CONTOH 4: ATS Optimization Detail")
    print("="*60)
    
    from CVmaker import ATSOptimizer
    
    # Before optimization
    original = "worked on several projects and helped team members sometimes"
    
    print(f"Original: {original}")
    
    # Add keywords
    optimized = ATSOptimizer.add_ats_keywords(original)
    print(f"With Keywords: {optimized}")
    
    # Format optimization
    formatted = ATSOptimizer.optimize_formatting(optimized)
    print(f"Formatted: {formatted}")
    
    # Remove special chars
    special_text = "Web•Dev✓ Expert (Python★ & JS★)"
    cleaned = ATSOptimizer.remove_special_formatting(special_text)
    print(f"\nOriginal with special: {special_text}")
    print(f"Cleaned: {cleaned}")


def example_5_batch_processing():
    """Contoh 5: Batch Processing Multiple CVs"""
    print("\n" + "="*60)
    print("CONTOH 5: Batch Processing")
    print("="*60)
    
    try:
        # Create multiple CVs
        for i in range(1, 3):
            cv_maker = CVMaker()
            
            cv_maker.cv.personal_info = {
                "full_name": f"Person {i}",
                "email": f"person{i}@example.com",
                "phone": f"+62-800-{i}000-0000",
                "location": "Jakarta",
                "linkedin": f"linkedin.com/in/person{i}"
            }
            
            cv_maker.cv.professional_summary = f"Profesional berpengalaman bidang teknologi"
            
            cv_maker.cv.add_experience(
                f"Position {i}",
                f"Company {i}",
                "2020",
                "2023",
                f"Experience {i}: managed projects and delivered results"
            )
            
            cv_maker.cv.add_skill(f"Skill {i}")
            
            cv_maker.optimize_cv_for_ats()
            cv_maker.save_cv(f"batch_cv_{i}")
            
            print(f"✓ CV {i} berhasil dibuat")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  CV ATS Maker - Contoh Penggunaan".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Run examples
    example_1_basic_usage()
    example_2_text_summarization()
    example_3_load_and_modify()
    example_4_ats_optimization()
    example_5_batch_processing()
    
    print("\n" + "="*60)
    print("✓ Semua contoh selesai!")
    print("✓ Check folder 'cv_output' untuk output files")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
