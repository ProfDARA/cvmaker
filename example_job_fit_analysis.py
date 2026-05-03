"""
Example usage of Job Fit Analyzer feature

Mendemonstrasikan cara menggunakan fitur Job Fit Analyzer untuk mendeteksi
kecocokan CV dengan job description
"""

from CVmaker import CVMaker, JobFitAnalyzer


def example_1_direct_analysis():
    """Example 1: Analisis job fit dengan job description langsung"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Direct Job Description Analysis")
    print("=" * 70)
    
    try:
        # Initialize CV Maker
        cv_maker = CVMaker()
        
        # Create sample CV
        cv_maker.cv = cv_maker.create_sample_cv()
        print("✓ Sample CV loaded")
        
        # Job description
        job_desc = """
        BACKEND DEVELOPER - PYTHON & DJANGO
        
        Requirements:
        - 3+ years Python experience
        - Django framework expertise
        - PostgreSQL and database design
        - REST API development
        - Docker containerization
        - Git version control
        
        Nice to have:
        - FastAPI experience
        - Microservices architecture
        - Cloud deployment (AWS/GCP)
        """
        
        # Analyze fit
        print("\nAnalyzing job fit...")
        analysis = cv_maker.check_job_fit(job_desc)
        
        # Display results
        JobFitAnalyzer.display_fit_analysis(analysis)
        
        # Save results
        cv_maker.save_job_fit_analysis(analysis, "backend_developer_fit")
        
    except Exception as e:
        print(f"Error: {e}")


def example_2_file_based_analysis():
    """Example 2: Analisis job fit dari file job description"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: File-Based Job Description Analysis")
    print("=" * 70)
    
    try:
        # Initialize CV Maker
        cv_maker = CVMaker()
        
        # Create sample CV
        cv_maker.cv = cv_maker.create_sample_cv()
        print("✓ Sample CV loaded")
        
        # Load job description from file
        job_file = "example_job_description.txt"
        print(f"\nAnalyzing from file: {job_file}")
        analysis = cv_maker.check_job_fit_from_file(job_file)
        
        # Display results
        JobFitAnalyzer.display_fit_analysis(analysis)
        
        # Save results
        cv_maker.save_job_fit_analysis(analysis, "senior_developer_fit")
        
    except FileNotFoundError:
        print(f"❌ File not found: example_job_description.txt")
        print("Pastikan file example_job_description.txt ada di folder project")
    except Exception as e:
        print(f"Error: {e}")


def example_3_multiple_jobs_comparison():
    """Example 3: Analisis dan bandingkan multiple job descriptions"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Multiple Jobs Comparison")
    print("=" * 70)
    
    try:
        cv_maker = CVMaker()
        cv_maker.cv = cv_maker.create_sample_cv()
        
        jobs = {
            "frontend_developer": """
            FRONTEND DEVELOPER - REACT
            Requirements:
            - React expertise
            - JavaScript/TypeScript
            - CSS & HTML5
            - REST API integration
            - Git version control
            """,
            
            "backend_developer": """
            BACKEND DEVELOPER - PYTHON
            Requirements:
            - Python 3+ years
            - Django/FastAPI
            - PostgreSQL
            - REST API design
            - Docker
            """,
            
            "fullstack_developer": """
            FULL STACK DEVELOPER
            Requirements:
            - 5+ years full stack
            - Python & JavaScript
            - React & Django
            - PostgreSQL
            - Docker & AWS
            - Machine Learning basics
            """
        }
        
        results = {}
        
        print("\nAnalyzing multiple positions...")
        for job_title, job_desc in jobs.items():
            print(f"  - Analyzing: {job_title}")
            analysis = cv_maker.check_job_fit(job_desc)
            results[job_title] = analysis.get("fit_score", 0)
        
        # Display comparison
        print("\n" + "-" * 70)
        print("COMPARISON RESULTS:")
        print("-" * 70)
        
        sorted_jobs = sorted(results.items(), key=lambda x: x[1], reverse=True)
        
        for rank, (job_title, score) in enumerate(sorted_jobs, 1):
            bar_length = 40
            filled = int(bar_length * score / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"{rank}. {job_title:20} {score:3d}/100 [{bar}]")
        
        print("\nBest fit: " + sorted_jobs[0][0])
        
    except Exception as e:
        print(f"Error: {e}")


def example_4_improvement_suggestions():
    """Example 4: Dapatkan saran improvement dari analysis"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Improvement Suggestions")
    print("=" * 70)
    
    try:
        cv_maker = CVMaker()
        cv_maker.cv = cv_maker.create_sample_cv()
        
        job_desc = """
        DATA SCIENTIST - PYTHON & ML
        Requirements:
        - 5+ years Python
        - Machine Learning (scikit-learn, TensorFlow)
        - Statistical analysis
        - SQL and Big Data tools
        - Visualization (matplotlib, seaborn)
        - Model deployment
        - Docker & cloud platforms
        
        Responsibilities:
        - Build and deploy ML models
        - Analyze complex datasets
        - Create data visualizations
        - Mentor data engineering team
        """
        
        print("\nAnalyzing CV fit for Data Scientist role...")
        analysis = cv_maker.check_job_fit(job_desc)
        
        # Extract and display recommendations
        print("\n" + "-" * 70)
        print("RECOMMENDATIONS TO IMPROVE FIT:")
        print("-" * 70)
        
        recommendations = analysis.get("recommendations", [])
        missing_skills = analysis.get("missing_skills", [])
        
        if recommendations:
            print("\n💡 AI Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        
        if missing_skills:
            print(f"\n📚 Skills to Develop:")
            for i, skill in enumerate(missing_skills[:5], 1):
                print(f"   {i}. {skill}")
        
        # Save detailed analysis
        cv_maker.save_job_fit_analysis(analysis, "data_scientist_fit")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("JOB FIT ANALYZER - USAGE EXAMPLES")
    print("=" * 70)
    
    try:
        # Run examples
        example_1_direct_analysis()
        # example_2_file_based_analysis()
        # example_3_multiple_jobs_comparison()
        # example_4_improvement_suggestions()
        
        print("\n" + "=" * 70)
        print("Examples completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPastikan GEMINI_API_KEY sudah di set dengan benar!")
