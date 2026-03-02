# Resume Alignment Tool

This tool extracts job descriptions from LinkedIn job postings and aligns your resume to match the requirements.

## Files

- **`resume_aligner.py`** - Main module with `ResumeAligner` class
- **`align_resume_from_main.py`** - Quick script using job URLs from main.py output
- **`batch_resume_aligner.py`** - Process multiple job URLs at once
- **`resume_template.txt`** - Sample resume template

## Setup

1. Make sure you have your OpenAI API key in `.env`:
   ```
   OPENAI_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here  # For job description extraction
   ```

2. Install dependencies (should already be in pyproject.toml):
   ```bash
   pip install langchain langchain-openai langchain-tavily python-dotenv
   ```

## Usage

### Option 1: Quick Start (Using job URLs from main.py)

```bash
python align_resume_from_main.py resume_template.txt
```

This will process the 3 job URLs found by main.py and create aligned resume versions.

### Option 2: Single Job URL

```bash
python resume_aligner.py <linkedin_url> <resume_file> [output_file]
```

Example:
```bash
python resume_aligner.py \
  https://www.linkedin.com/jobs/view/staff-ai-engineer-at-intuit-4358332381 \
  resume_template.txt \
  aligned_resume_intuit.txt
```

### Option 3: Batch Processing

```bash
python batch_resume_aligner.py <resume_file> [output_directory] [url1] [url2] ...
```

Example:
```bash
python batch_resume_aligner.py resume_template.txt ./aligned_resumes \
  https://www.linkedin.com/jobs/view/staff-ai-engineer-at-intuit-4358332381 \
  https://www.linkedin.com/jobs/view/generative-ai-engineer-at-archer-4331977162
```

### Option 4: Use as Python Module

```python
from resume_aligner import ResumeAligner

aligner = ResumeAligner()

# Extract job description
job_desc = aligner.extract_job_description("https://linkedin.com/jobs/view/...")

# Read your resume
resume = aligner.read_resume("resume.txt")

# Align resume
aligned = aligner.align_resume(resume, job_desc)

# Or use the complete workflow
aligned = aligner.process(
    "https://linkedin.com/jobs/view/...",
    "resume.txt",
    "aligned_resume.txt"
)
```

## How It Works

1. **Job Description Extraction**: Uses TavilySearch to fetch the LinkedIn job posting content
2. **Structured Extraction**: Uses GPT-4 to extract structured information (title, company, requirements, etc.)
3. **Resume Alignment**: Uses GPT-4 to intelligently align your resume with the job requirements
   - Highlights relevant skills and experiences
   - Reorders sections to emphasize relevant qualifications
   - Uses keywords from the job description naturally
   - Maintains original format and structure

## Resume Format

Currently supports:
- `.txt` files (plain text)
- `.md` files (Markdown)

Future support (requires additional libraries):
- `.pdf` files (needs PyPDF2 or pdfplumber)
- `.docx` files (needs python-docx)

## Notes

- **LinkedIn Access**: LinkedIn may require authentication to view full job descriptions. The tool uses web search to extract content, which may have limitations.
- **Cost**: Each alignment uses 2-3 LLM API calls (extraction + alignment). Monitor your usage.
- **Accuracy**: The tool emphasizes existing content - it won't fabricate experiences or skills.

## Output

For each job, the tool creates an aligned resume file with naming pattern:
- `{original_name}_aligned_{company_name}.txt`

Example: `resume_template_aligned_intuit.txt`

## Troubleshooting

**Issue**: "Limited content extracted"
- **Solution**: LinkedIn may require login. Try manually copying the job description and creating a text file, then modify the script to read from that file.

**Issue**: "Resume file not found"
- **Solution**: Create a resume file first. Use `resume_template.txt` as a starting point.

**Issue**: "ModuleNotFoundError"
- **Solution**: Install missing dependencies: `pip install -e .` or install individually.
