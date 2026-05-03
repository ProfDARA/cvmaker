"""
Quick Test - Job Fit Analyzer

File ini untuk quick testing fitur Job Fit Analyzer
Cukup jalankan: python quick_test_jobfit.py
"""

from CVmaker import CVMaker, JobFitAnalyzer


def quick_test():
    """Quick test job fit analyzer feature"""
    
    print("\n" + "=" * 70)
    print("JOB FIT ANALYZER - QUICK TEST")
    print("=" * 70)
    
    try:
        # Initialize
        print("\n[1] Initializing CV Maker...")
        cv_maker = CVMaker()
        print("✓ CV Maker initialized")
        
        # Create sample CV
        print("\n[2] Loading sample CV...")
        cv_maker.cv = cv_maker.create_sample_cv()
        print("✓ Sample CV loaded")
        print(f"   Name: {cv_maker.cv.personal_info['full_name']}")
        print(f"   Skills: {', '.join(cv_maker.cv.skills[:5])}...")
        
        # Test 1: Direct job description analysis
        print("\n[3] Analyzing job fit (Direct job description)...")
        job_desc = """
        SENIOR FULL STACK DEVELOPER
        
        Requirements:
        - 5+ years experience in full stack development
        - Python and JavaScript expertise
        - React, Django, FastAPI experience
        - PostgreSQL and MongoDB
        - Docker and AWS
        - REST API design
        - CI/CD pipelines
        - Team leadership
        
        Nice to have:
        - Machine Learning basics
        - Microservices architecture
        - Kubernetes
        """
        
        analysis_1 = cv_maker.check_job_fit(job_desc)
        print("✓ Analysis completed")
        
        # Display results
        JobFitAnalyzer.display_fit_analysis(analysis_1)
        
        # Save results
        print("\n[4] Saving results...")
        cv_maker.save_job_fit_analysis(analysis_1, "quick_test_analysis")
        print("✓ Results saved to cv_output/quick_test_analysis.json")
        
        # Test 2: File-based analysis
        print("\n[5] Testing file-based analysis...")
        try:
            analysis_2 = cv_maker.check_job_fit_from_file("example_job_description.txt")
            print("✓ File-based analysis completed")
            
            fit_score = analysis_2.get("fit_score", 0)
            fit_level = analysis_2.get("fit_level", "UNKNOWN")
            print(f"   Fit Score: {fit_score}/100")
            print(f"   Fit Level: {fit_level}")
            
            # Save
            cv_maker.save_job_fit_analysis(analysis_2, "example_job_fit")
            
        except FileNotFoundError:
            print("⚠ File not found: example_job_description.txt")
            print("  (This is optional for testing)")
        
        # Summary
        print("\n" + "=" * 70)
        print("TEST COMPLETED SUCCESSFULLY! ✅")
        print("=" * 70)
        print("\nOutput files created in cv_output/:")
        print("  - quick_test_analysis.json")
        print("  - example_job_fit.json (if file exists)")
        print("\nNext steps:")
        print("  1. Check the JSON output files")
        print("  2. Run: python example_job_fit_analysis.py")
        print("  3. Read: JOBFIT_GUIDE.md for more examples")
        print("=" * 70 + "\n")
        
        return True
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nSetup GEMINI_API_KEY:")
        print("  Windows: set GEMINI_API_KEY=your_api_key")
        print("  Or create .env file with: GEMINI_API_KEY=your_api_key")
        print("\nGet API key from: https://aistudio.google.com")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = quick_test()
    exit(0 if success else 1)
