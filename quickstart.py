"""
CV Maker Pro - Quick Start & Testing

Run this untuk quick start dan test aplikasi
"""

import subprocess
import time
import os
import sys
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70 + "\n")

def check_requirements():
    """Check jika semua requirements sudah installed"""
    print_header("📦 Checking Requirements")
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'google': 'Google Generative AI',
        'dotenv': 'python-dotenv',
        'reportlab': 'ReportLab'
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print("  pip install -r requirements.txt")
        return False
    
    print("\n✅ All requirements installed!")
    return True

def check_api_key():
    """Check jika GEMINI_API_KEY sudah set"""
    print_header("🔑 Checking GEMINI_API_KEY")
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        print(f"✓ GEMINI_API_KEY is set")
        print(f"  Value: {api_key[:10]}...{api_key[-10:]}")
        return True
    else:
        print("✗ GEMINI_API_KEY is NOT set")
        print("\nSet it with:")
        print("  Windows (PowerShell): $env:GEMINI_API_KEY = 'your_key'")
        print("  Windows (CMD): setx GEMINI_API_KEY 'your_key'")
        print("  Linux/Mac: export GEMINI_API_KEY='your_key'")
        print("\nOr create .env file:")
        print("  GEMINI_API_KEY=your_api_key_here")
        print("\nGet API key from: https://aistudio.google.com")
        return False

def create_folders():
    """Create required folders"""
    print_header("📁 Creating Folders")
    
    folders = ['cv_data', 'cv_output', 'templates']
    
    for folder in folders:
        path = Path(folder)
        if not path.exists():
            path.mkdir(exist_ok=True)
            print(f"✓ Created {folder}/")
        else:
            print(f"✓ {folder}/ already exists")

def check_html_frontend():
    """Check jika index.html exists"""
    print_header("🌐 Checking Frontend")
    
    if Path('index.html').exists():
        print("✓ index.html found")
        print(f"  Location: {Path('index.html').absolute()}")
        return True
    else:
        print("✗ index.html NOT found")
        return False

def display_instructions():
    """Display startup instructions"""
    print_header("🚀 Quick Start Instructions")
    
    print("1️⃣  START BACKEND SERVER")
    print("   Terminal: python server.py")
    print("   Expected: 'Starting server on http://localhost:5000'")
    
    print("\n2️⃣  OPEN FRONTEND")
    print("   Option A: Double-click index.html")
    print("   Option B: Right-click index.html > Open with browser")
    print("   Option C: Browser: file:///path/to/index.html")
    
    print("\n3️⃣  CREATE & OPTIMIZE CV")
    print("   - Fill in your information")
    print("   - Click '⚡ Check ATS Score'")
    print("   - View suggestions and optimize")
    
    print("\n4️⃣  ANALYZE JOB FIT")
    print("   - Paste job description")
    print("   - Click '🎯 Analyze Fit'")
    print("   - See how well you match")
    
    print("\n5️⃣  SAVE & LOAD CV")
    print("   - Go to Storage tab")
    print("   - Click Save to store CV")
    print("   - Load CV anytime from saved list")

def display_features():
    """Display available features"""
    print_header("✨ Available Features")
    
    features = [
        ("CV Editor", "Edit personal info, experience, education, skills"),
        ("ATS Optimizer", "Get real-time ATS score with improvement suggestions"),
        ("Job Fit Analyzer", "Check how well your CV matches a job posting"),
        ("Save/Load CV", "Save CV to JSON and reload anytime"),
        ("Responsive UI", "Works on desktop, tablet, and mobile"),
        ("Local Storage", "All data stored locally on your computer"),
        ("Zero Sign-up", "No account or login required"),
        ("Offline Ready", "Works completely offline (after loading HTML)")
    ]
    
    for i, (name, desc) in enumerate(features, 1):
        print(f"{i}. {name}")
        print(f"   {desc}\n")

def display_troubleshooting():
    """Display troubleshooting tips"""
    print_header("🐛 Troubleshooting")
    
    print("❓ Server not starting?")
    print("  → Make sure port 5000 is not in use")
    print("  → Run: python server.py")
    print("  → Should see 'Starting server on http://localhost:5000'")
    
    print("\n❓ Frontend not connecting to backend?")
    print("  → Check server is running first")
    print("  → Browser should show API responses")
    print("  → Check browser console (F12) for errors")
    
    print("\n❓ Gemini API errors?")
    print("  → Check GEMINI_API_KEY is set correctly")
    print("  → Visit https://aistudio.google.com for new key")
    print("  → Restart server after setting new key")
    
    print("\n❓ CV not saving?")
    print("  → Check cv_data/ folder exists")
    print("  → Check file permissions")
    print("  → Try different filename")

def display_api_endpoints():
    """Display API endpoints"""
    print_header("📡 Available API Endpoints")
    
    endpoints = [
        ("GET", "/api/health", "Check if API is running"),
        ("POST", "/api/cv/analyze-ats", "Analyze ATS score"),
        ("POST", "/api/job/analyze-fit", "Analyze job fit"),
        ("POST", "/api/cv/save", "Save CV to file"),
        ("GET", "/api/cv/load/{filename}", "Load saved CV"),
        ("GET", "/api/cv/list", "List all saved CVs"),
        ("DELETE", "/api/cv/delete/{filename}", "Delete saved CV"),
        ("GET", "/api/docs", "API documentation")
    ]
    
    print(f"{'Method':<10} {'Endpoint':<30} {'Description':<35}")
    print("-" * 75)
    
    for method, endpoint, desc in endpoints:
        print(f"{method:<10} {endpoint:<30} {desc:<35}")

def main():
    """Main quick start function"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           CV MAKER PRO - QUICK START & SETUP                  ║")
    print("║           ATS Optimizer + Job Fit Analyzer                    ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    # Checks
    checks = [
        ("Requirements", check_requirements),
        ("API Key", check_api_key),
        ("Folders", create_folders),
        ("Frontend", check_html_frontend),
    ]
    
    passed = 0
    failed = 0
    
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            failed += 1
    
    # Display info
    display_features()
    display_api_endpoints()
    display_instructions()
    display_troubleshooting()
    
    # Summary
    print_header("📊 Startup Summary")
    
    if failed == 0 and passed == len(checks):
        print("✅ All checks passed! You're ready to go!")
        print("\n🚀 Next steps:")
        print("   1. Start server: python server.py")
        print("   2. Open browser: file:///path/to/index.html")
        print("   3. Create your CV and analyze!")
    else:
        print(f"⚠️  {failed} check(s) failed, {passed} passed")
        print("\nPlease fix the issues above before starting the application")
    
    print("\n" + "=" * 70)
    print("Documentation: See SETUP_FULLSTACK.md for detailed guide")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
