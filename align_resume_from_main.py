"""
Quick script to align resume with job URLs from main.py output
"""

from resume_aligner import ResumeAligner
from pathlib import Path
import sys


def main():
    """Align resume with job URLs from main.py"""
    
    # Job URLs from the latest main.py run
    job_urls = [
        "https://www.linkedin.com/jobs/view/staff-ai-engineer-at-intuit-4358332381",
        "https://www.linkedin.com/jobs/view/generative-ai-engineer-at-archer-4331977162",
        "https://www.linkedin.com/jobs/view/generative-ai-engineer-at-kronosai-4305165405",
    ]
    
    # Default resume path
    resume_path = "resume_template.txt"
    
    # Allow override via command line
    if len(sys.argv) > 1:
        resume_path = sys.argv[1]
    
    if not Path(resume_path).exists():
        print(f"❌ Resume file not found: {resume_path}")
        print("Please create a resume file or use resume_template.txt as a starting point.")
        sys.exit(1)
    
    print("🚀 Resume Alignment Tool")
    print(f"📄 Resume: {resume_path}")
    print(f"📋 Jobs to process: {len(job_urls)}\n")
    
    aligner = ResumeAligner()
    
    for i, url in enumerate(job_urls, 1):
        print(f"\n{'='*70}")
        print(f"Processing Job {i}/{len(job_urls)}")
        print(f"{'='*70}")
        
        try:
            # Create output filename
            resume_name = Path(resume_path).stem
            resume_ext = Path(resume_path).suffix
            
            # Extract company name from URL
            if "at-" in url:
                company_part = url.split("at-")[-1].split("-")[0]
                output_path = f"{resume_name}_aligned_{company_part}{resume_ext}"
            else:
                output_path = f"{resume_name}_aligned_job_{i}{resume_ext}"
            
            aligner.process(url, resume_path, output_path)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*70}")
    print("✅ All jobs processed!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
