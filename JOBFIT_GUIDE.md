# Job Fit Analyzer Guide

## Overview

**Job Fit Analyzer** adalah fitur AI-powered yang menganalisis tingkat kecocokan CV Anda dengan job description. Menggunakan Gemini API, sistem ini memberikan detailed analysis tentang:

- 📊 **Fit Score** (0-100): Skor kecocokan overall
- ✅ **Matched Skills**: Skills yang sudah ada di CV
- ❌ **Missing Skills**: Skills yang perlu dikembangkan
- 💪 **Strengths**: Kekuatan CV untuk posisi ini
- ⚠️ **Weaknesses**: Kelemahan yang perlu diperbaiki
- 💡 **Recommendations**: Saran improvement spesifik

---

## Quick Start

### 1. Basic Usage (Direct Job Description)

```python
from CVmaker import CVMaker

# Initialize
cv_maker = CVMaker()
cv_maker.cv = cv_maker.create_sample_cv()

# Job description
job_desc = """
SENIOR DEVELOPER
Requirements:
- 5+ years experience
- Python & JavaScript
- React & Django
- PostgreSQL
- Docker & AWS
"""

# Analyze
analysis = cv_maker.check_job_fit(job_desc)

# Display results
from CVmaker import JobFitAnalyzer
JobFitAnalyzer.display_fit_analysis(analysis)

# Save results
cv_maker.save_job_fit_analysis(analysis, "job_fit_result")
```

### 2. Load Job Description from File

```python
cv_maker = CVMaker()
cv_maker.cv = cv_maker.create_sample_cv()

# Analyze from file
analysis = cv_maker.check_job_fit_from_file("example_job_description.txt")

# Display & save
JobFitAnalyzer.display_fit_analysis(analysis)
cv_maker.save_job_fit_analysis(analysis, "my_analysis")
```

### 3. Compare Multiple Jobs

```python
cv_maker = CVMaker()
cv_maker.cv = cv_maker.create_sample_cv()

jobs = {
    "Frontend Dev": "...",
    "Backend Dev": "...",
    "Full Stack Dev": "..."
}

results = {}
for title, desc in jobs.items():
    analysis = cv_maker.check_job_fit(desc)
    results[title] = analysis.get("fit_score", 0)

# Sort by score
for title, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{title}: {score}/100")
```

---

## API Reference

### CVMaker Methods

#### `check_job_fit(job_description: str) -> Dict`
Analisis kecocokan CV dengan job description.

```python
analysis = cv_maker.check_job_fit("Job description text here...")
```

**Returns:**
```python
{
    "fit_score": 75,
    "fit_level": "GOOD",
    "matched_skills": ["Python", "Django", "PostgreSQL"],
    "missing_skills": ["Machine Learning", "AWS"],
    "matched_experience": ["Backend development"],
    "strengths": ["5+ years experience", "Strong technical skills"],
    "weaknesses": ["Limited ML experience"],
    "recommendations": ["Learn ML basics", "Get AWS certification"],
    "summary": "Good fit for backend role..."
}
```

#### `check_job_fit_from_file(job_file_path: str) -> Dict`
Analisis kecocokan dengan job description dari file.

```python
analysis = cv_maker.check_job_fit_from_file("job_description.txt")
```

#### `save_job_fit_analysis(analysis: Dict, filename: str = "job_fit_analysis")`
Simpan hasil analisis ke JSON file.

```python
cv_maker.save_job_fit_analysis(analysis, "my_analysis")
# Output: cv_output/my_analysis.json
```

### JobFitAnalyzer Methods

#### `display_fit_analysis(analysis: Dict)`
Tampilkan hasil analisis dengan format yang rapi.

```python
JobFitAnalyzer.display_fit_analysis(analysis)
```

**Output:**
```
======================================================================
JOB FIT ANALYSIS RESULT
======================================================================

📊 FIT SCORE: 75/100 [████████████████████████░░░░░░░░░░░░░░░░░░░░]
📈 FIT LEVEL: GOOD

📝 Summary:
Good match for the Senior Developer position...

✅ Matched Skills (8):
   • Python
   • JavaScript
   • Django
   • React
   • PostgreSQL
   • Docker
   • REST API
   • Git

❌ Missing Skills (3):
   • Machine Learning
   • AWS
   • Kubernetes

💪 Strengths:
   • 5+ years experience in full stack development
   • Strong technical foundation across multiple technologies
   • Experience with modern frameworks

⚠️ Weaknesses:
   • Limited cloud platform experience
   • No machine learning background
   • Limited DevOps experience

💡 Recommendations:
   • Pursue AWS certification or hands-on cloud projects
   • Learn ML basics through online courses or projects
   • Gain more DevOps/Kubernetes experience

======================================================================
```

---

## Understanding Fit Levels

| Fit Level | Score | Meaning |
|-----------|-------|---------|
| **EXCELLENT** | 80-100 | CV sangat cocok untuk posisi |
| **GOOD** | 60-79 | CV cocok dengan beberapa gap |
| **MODERATE** | 40-59 | CV cukup cocok, banyak gap |
| **POOR** | 0-39 | CV kurang cocok untuk posisi |

---

## Output Files

Hasil analisis disimpan dalam folder `cv_output/`:

```
cv_output/
  ├── job_fit_analysis.json          # JSON dengan detailed analysis
  ├── my_cv_ats_optimized.json       # CV dalam format JSON
  ├── my_cv_ats_optimized.txt        # CV dalam format plain text
  └── my_cv_ats_optimized.pdf        # CV dalam format PDF
```

---

## JSON Output Structure

```json
{
  "fit_score": 75,
  "fit_level": "GOOD",
  "matched_skills": [
    "Python",
    "Django",
    "PostgreSQL",
    "REST API",
    "Docker"
  ],
  "missing_skills": [
    "Machine Learning",
    "AWS",
    "Kubernetes"
  ],
  "matched_experience": [
    "5+ years full stack development",
    "Backend architecture design"
  ],
  "strengths": [
    "Strong Python expertise",
    "Experience with Django framework",
    "Proven ability to design REST APIs"
  ],
  "weaknesses": [
    "Limited cloud platform experience",
    "No machine learning background"
  ],
  "recommendations": [
    "Pursue AWS Certified Solutions Architect certification",
    "Complete machine learning fundamentals course",
    "Work on a cloud-native project"
  ],
  "summary": "Your CV shows good match for this Senior Developer position. You have most of the required technical skills, particularly in Python and backend development. To increase your fit, focus on gaining cloud experience (AWS) and learning ML basics."
}
```

---

## Advanced Usage

### Load Custom CV Data

```python
from CVmaker import CVData

# Load CV dari JSON
cv = CVData.from_json("my_cv.json")

# Atau buat CV baru
cv = CVData()
cv.personal_info["full_name"] = "John Doe"
cv.add_skill("Python")
cv.add_experience("Senior Dev", "Company", "2020", "Present", "...")

# Use with CV Maker
cv_maker = CVMaker()
cv_maker.cv = cv

# Analyze
analysis = cv_maker.check_job_fit(job_description)
```

### Batch Analysis

```python
import json

cv_maker = CVMaker()
cv_maker.cv = cv_maker.create_sample_cv()

# Analisis multiple jobs
jobs_file = "job_postings.json"
with open(jobs_file, 'r') as f:
    jobs = json.load(f)

results = {}
for job in jobs:
    title = job['title']
    description = job['description']
    analysis = cv_maker.check_job_fit(description)
    results[title] = analysis

# Save batch results
with open("batch_analysis.json", 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
```

### Integration with CLI

```python
# cli.py
import argparse
from CVmaker import CVMaker

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cv', default='my_cv.json')
    parser.add_argument('--job', required=True)
    parser.add_argument('--output', default='analysis.json')
    
    args = parser.parse_args()
    
    cv_maker = CVMaker()
    cv_maker.cv = CVData.from_json(args.cv)
    
    analysis = cv_maker.check_job_fit_from_file(args.job)
    cv_maker.save_job_fit_analysis(analysis, args.output)

if __name__ == "__main__":
    main()
```

Usage:
```bash
python cli.py --job job_description.txt --output my_analysis
```

---

## Tips & Best Practices

### 1. Format Job Description
Semakin detail dan clear job description, semakin akurat analysis:
- ✅ Include requirements section
- ✅ List specific skills needed
- ✅ Describe responsibilities
- ✅ Mention nice-to-have skills

### 2. Keep CV Updated
- Update CV dengan latest skills
- Add recent projects
- Include certifications
- Quantify achievements

### 3. Interpret Results
- **High fit score** = Strong candidate
- **Missing skills** = Learning opportunities
- **Recommendations** = Action items to improve fit

### 4. Use for Career Planning
- Identify skill gaps
- Plan professional development
- Target right roles
- Prepare for interviews

---

## Troubleshooting

### Error: GEMINI_API_KEY tidak ditemukan
```bash
# Set environment variable
# Windows:
set GEMINI_API_KEY=your_key_here

# Or create .env file:
GEMINI_API_KEY=your_key_here
```

### File not found error
```python
# Pastikan path file benar
import os
if os.path.exists("job_description.txt"):
    analysis = cv_maker.check_job_fit_from_file("job_description.txt")
```

### Empty or invalid JSON response
```python
# Check analysis structure
if "error" in analysis:
    print(f"Error: {analysis['error']}")
else:
    JobFitAnalyzer.display_fit_analysis(analysis)
```

---

## Examples

See `example_job_fit_analysis.py` untuk:
- Direct analysis contoh
- File-based analysis
- Multiple jobs comparison
- Improvement suggestions
- Batch processing

---

## Next Steps

1. ✅ Setup GEMINI_API_KEY
2. ✅ Run `python CVmaker.py` untuk testing
3. ✅ Check `cv_output/` folder untuk results
4. ✅ Modify CV data sesuai kebutuhan
5. ✅ Analyze multiple job descriptions
6. ✅ Use recommendations untuk improvement

---

## Support

Untuk issues atau pertanyaan, check:
- `README.md` - Project overview
- `QUICK_START.py` - Quick examples
- `example_job_fit_analysis.py` - Detailed examples
- Gemini API docs: https://ai.google.dev/

---

*Happy Job Hunting! 🚀*
