"""
Batch Resume Alignment Tool
Processes multiple LinkedIn job URLs and creates aligned resume versions for each.
"""

from pathlib import Path
from resume_aligner import ResumeAligner
import sys


def process_multiple_jobs(job_urls: list[str], resume_path: str, output_dir: Optional[str] = None):
    """
    Process multiple job URLs and create aligned resumes for each
    
    Args:
        job_urls: List of LinkedIn job posting URLs
        resume_path: Path to the original resume file
        output_dir: Directory to save aligned resumes (default: same as resume directory)
    """
    if output_dir is None:
        output_dir = Path(resume_path).parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    aligner = ResumeAligner()
    resume_name = Path(resume_path).stem
    resume_ext = Path(resume_path).suffix
    
    results = []
    
    for i, url in enumerate(job_urls, 1):
        print(f"\n{'='*60}")
        print(f"Processing Job {i}/{len(job_urls)}")
        print(f"{'='*60}")
        
        try:
            # Extract company name from URL or use index
            company_name = f"job_{i}"
            if "linkedin.com/jobs/view" in url:
                # Try to extract company from URL
                parts = url.split("/")
                if len(parts) > 4:
                    company_name = parts[-2].replace("-", "_")
            
            output_path = output_dir / f"{resume_name}_aligned_{company_name}{resume_ext}"
            
            aligned_resume = aligner.process(url, resume_path, str(output_path))
            results.append({
                "url": url,
                "output_path": str(output_path),
                "status": "success"
            })
            
        except Exception as e:
            print(f"❌ Error processing {url}: {str(e)}")
            results.append({
                "url": url,
                "status": "error",
                "error": str(e)
            })
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total jobs processed: {len(job_urls)}")
    print(f"Successful: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"Failed: {sum(1 for r in results if r['status'] == 'error')}")
    print(f"\nAligned resumes saved to: {output_dir}")
    
    return results


def main():
    """Example usage with job URLs from the project"""
    import sys
    
    # Job URLs from the terminal output
    default_job_urls = [
        "https://www.linkedin.com/jobs/view/staff-ai-engineer-at-intuit-4358332381",
        "https://www.linkedin.com/jobs/view/generative-ai-engineer-at-archer-4331977162",
        "https://www.linkedin.com/jobs/view/generative-ai-engineer-at-kronosai-4305165405",
    ]
    
    if len(sys.argv) < 2:
        print("Usage: python batch_resume_aligner.py <resume_file_path> [output_directory]")
        print("\nExample:")
        print("  python batch_resume_aligner.py resume_template.txt")
        print("  python batch_resume_aligner.py resume_template.txt ./aligned_resumes")
        print("\nUsing default job URLs from the project...")
        resume_path = "resume_template.txt"
    else:
        resume_path = sys.argv[1]
        default_job_urls = []  # User will provide URLs
    
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    else:
        output_dir = None
    
    # If URLs provided via command line or file
    if len(sys.argv) > 3:
        # Assume remaining args are URLs
        job_urls = sys.argv[3:]
    else:
        job_urls = default_job_urls
    
    if not job_urls:
        print("No job URLs provided. Please provide URLs as arguments or update the script.")
        sys.exit(1)
    
    if not Path(resume_path).exists():
        print(f"Resume file not found: {resume_path}")
        print("Please create a resume file first or use resume_template.txt")
        sys.exit(1)
    
    process_multiple_jobs(job_urls, resume_path, output_dir)


if __name__ == "__main__":
    main()
