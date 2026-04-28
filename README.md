# CV ATS Maker dengan Text Summarizer (Gemini API)

Aplikasi modern untuk membuat CV yang dioptimalkan untuk Applicant Tracking System (ATS) dengan fitur text summarizer menggunakan Gemini API dari Google.

## ✨ Fitur Utama

- **CV Data Management**: Manajemen data CV terstruktur dengan informasi lengkap
- **ATS Optimization**: Otomatis mengoptimalkan CV untuk sistem ATS
- **Text Summarizer**: Merangkum deskripsi pekerjaan menggunakan Gemini API
- **Multi-Format Export**: Export ke Plain Text (ATS-friendly) dan JSON
- **Professional Keywords**: Menambahkan action verbs dan keywords industri
- **Format Cleaning**: Menghapus formatting kompleks yang tidak ATS-friendly

## 🚀 Quick Start

### 1. Setup Environment

**Windows:**
```bash
# Clone atau download repository
cd "CV maker"

# Install dependencies
pip install -r requirements.txt

# Set Gemini API Key (Windows PowerShell)
$env:GEMINI_API_KEY = "your_api_key_here"

# Atau set permanent (Windows CMD)
setx GEMINI_API_KEY "your_api_key_here"
```

**Linux/Mac:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set Gemini API Key
export GEMINI_API_KEY="your_api_key_here"

# Untuk permanent, tambah ke ~/.bashrc atau ~/.zshrc
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
```

### 2. Dapatkan Gemini API Key

1. Kunjungi https://aistudio.google.com
2. Click "Get API Key" atau "Create new API key"
3. Copy API key Anda
4. Set sebagai environment variable

### 3. Run Aplikasi

```bash
python CVmaker.py
```

## 📖 Penggunaan

### Basic Usage

```python
from CVmaker import CVMaker

# Initialize CV Maker
cv_maker = CVMaker(api_key="your_api_key")

# Create CV object
cv = cv_maker.cv

# Add personal info
cv.personal_info = {
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+62-812-1234-5678",
    "location": "Jakarta, Indonesia",
    "linkedin": "linkedin.com/in/johndoe"
}

# Add experience
cv.add_experience(
    job_title="Senior Developer",
    company="Tech Company",
    start_date="Jan 2022",
    end_date="Present",
    description="Managed development team and delivered projects on time"
)

# Add education
cv.add_education(
    degree="Bachelor",
    institution="University",
    field="Computer Science",
    graduation_year="2020"
)

# Add skills
cv.add_skill("Python")
cv.add_skill("JavaScript")
cv.add_skill("Docker")

# Optimize for ATS
cv_maker.optimize_cv_for_ats()

# Save CV
cv_maker.save_cv("my_cv")
```

### Summarize Experience

```python
# Summarize experience description
summary = cv_maker.summarize_experience(
    "Bertanggung jawab atas pengembangan dan maintenance aplikasi web, "
    "implementasi CI/CD pipeline, dan kolaborasi dengan tim design"
)
print(summary)
```

## 📁 Struktur File

```
CV maker/
├── CVmaker.py          # Main application
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── README.md          # Documentation (this file)
├── .env               # Environment variables (create manually)
└── cv_output/         # Output folder (auto-created)
    ├── my_cv_ats_optimized.txt
    └── my_cv_ats_optimized.json
```

## 🏗️ Arsitektur Aplikasi

### Classes

1. **GeminiConfig**
   - Konfigurasi dan komunikasi dengan Gemini API
   - Summarize text
   - Optimize CV content

2. **CVData**
   - Model untuk data CV
   - Methods untuk add experience, education, skills, dll
   - Export ke dict, JSON

3. **ATSOptimizer**
   - Optimasi formatting untuk ATS
   - Remove special characters
   - Add action keywords

4. **CVExporter**
   - Export CV ke berbagai format
   - Plain text format (ATS-friendly)
   - JSON format

5. **CVMaker**
   - Main application class
   - Koordinasi semua components
   - Workflow management

## 🎯 ATS Optimization Features

### Formatting Optimization
- Hapus simbol khusus yang tidak standard
- Ubah bullet points ke format sederhana
- Remove excessive spaces

### Content Optimization
- Tambah action verbs (achieved, led, managed, dll)
- Professional language
- Structured information

### Keyword Enhancement
- Industry-specific keywords
- Measurable achievements
- Clear role descriptions

## 📊 Output Format

### Plain Text (TXT)
```
JOHN DOE
Email: john@example.com
Phone: +62-812-1234-5678
---

PROFESSIONAL SUMMARY
Experienced developer...

EXPERIENCE

Senior Developer at Tech Company
Jan 2022 - Present
Led development team...

EDUCATION

Bachelor in Computer Science
University (2020)

SKILLS
Python, JavaScript, Docker, AWS
```

### JSON Format
```json
{
  "personal_info": {
    "full_name": "John Doe",
    "email": "john@example.com",
    ...
  },
  "professional_summary": "...",
  "experience": [...],
  "education": [...],
  "skills": [...]
}
```

## 🔧 Advanced Usage

### Custom CV Processing

```python
from CVmaker import CVMaker, CVExporter, ATSOptimizer

cv_maker = CVMaker()

# Load existing CV from JSON
cv = CVMaker.from_json("existing_cv.json")
cv_maker.cv = cv

# Optimize specific experience
for exp in cv_maker.cv.experience:
    optimized_desc = ATSOptimizer.add_ats_keywords(exp['description'])
    exp['description'] = optimized_desc

# Save
cv_maker.save_cv("optimized_cv")
```

### Batch Processing

```python
import glob

# Process multiple CVs
cv_files = glob.glob("input_cvs/*.json")
for cv_file in cv_files:
    cv_maker = CVMaker()
    cv_maker.cv = CVData.from_json(cv_file)
    cv_maker.optimize_cv_for_ats()
    filename = cv_file.split('/')[-1].replace('.json', '')
    cv_maker.save_cv(f"optimized_{filename}")
```

## 🐛 Troubleshooting

### "GEMINI_API_KEY tidak ditemukan"
- Setup environment variable sesuai OS Anda
- Pastikan API key valid dari https://aistudio.google.com
- Restart terminal/IDE setelah set environment variable

### "Error menggunakan Gemini API"
- Check internet connection
- Verify API key masih valid
- Check quota di Google AI Studio
- Fallback mechanism sudah ada (use original text)

### File not found
- Pastikan working directory sudah benar
- Gunakan absolute path jika perlu
- Create cv_output folder manually jika needed

## 📝 Environment Variables

Buat file `.env` di root folder:

```
GEMINI_API_KEY=your_api_key_here
```

## 🔐 Security Tips

- ⚠️ Jangan commit `.env` file dengan API key
- Gunakan `.gitignore` untuk `.env`
- Rotate API key secara berkala
- Jangan share API key di public repository

## 📚 Dependencies

- **google-generativeai**: Gemini API client
- **python-dotenv**: Environment variable management
- **reportlab**: PDF generation (optional)
- **python-docx**: DOCX generation (optional)

## 🎓 Learning Resources

- [Gemini API Documentation](https://ai.google.dev/)
- [ATS Best Practices](https://www.indeed.com/career-advice/cvs-cover-letters/applicant-tracking-system-ats)
- [Google AI Studio](https://aistudio.google.com)

## 📄 License

MIT License - Feel free to use and modify

## 👨‍💻 Author

Created with ❤️ for better CV optimization

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:
1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Create Pull Request

## 📞 Support

Untuk pertanyaan atau issues, silakan create issue di repository.

---

**Happy CV Making! 🚀**
