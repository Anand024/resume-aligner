"""
Resume Alignment Tool
Takes a LinkedIn job posting URL, extracts the job description,
and updates a resume to align with the job requirements.
"""

from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

load_dotenv()


class JobDescription(BaseModel):
    """Schema for extracted job description"""
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    location: str = Field(description="Job location")
    description: str = Field(description="Full job description")
    requirements: str = Field(description="Key requirements and qualifications")
    responsibilities: str = Field(description="Key responsibilities")


class ResumeAligner:
    """Class to handle resume alignment with job descriptions"""
    
    def __init__(self, model: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.search_tool = TavilySearch()
        self.llm_structured = self.llm.with_structured_output(JobDescription)
    
    def extract_job_description(self, linkedin_url: str) -> JobDescription:
        """
        Extract job description from LinkedIn URL using web search
        """
        print(f"🔍 Extracting job description from: {linkedin_url}")
        
        # Extract job ID and company from URL for better search
        job_id = linkedin_url.split("/")[-1] if "/" in linkedin_url else ""
        page_content = ""
        
        # Try multiple search strategies
        search_queries = [
            f"LinkedIn job posting {linkedin_url} full description",
            f"site:linkedin.com/jobs {job_id}",
            f"{linkedin_url} job description requirements",
        ]
        
        for query in search_queries:
            try:
                result = self.search_tool.invoke({"query": query, "search_depth": "advanced"})
                
                # Handle different result formats from TavilySearch
                if isinstance(result, list):
                    for item in result:
                        if isinstance(item, dict):
                            content = item.get("content", "") or item.get("raw_content", "")
                            if content:
                                page_content += f"\n\n{content}"
                        else:
                            page_content += f"\n\n{str(item)}"
                elif isinstance(result, dict):
                    content = result.get("content", "") or result.get("raw_content", "")
                    if content:
                        page_content += f"\n\n{content}"
                else:
                    page_content += f"\n\n{str(result)}"
                
                # If we got substantial content, break
                if len(page_content) > 500:
                    break
            except Exception as e:
                print(f"⚠️  Search query failed: {query} - {str(e)}")
                continue
        
        if not page_content or len(page_content.strip()) < 100:
            print("⚠️  Warning: Limited content extracted. The job description may be incomplete.")
            print("   LinkedIn may require authentication. Consider manually copying the job description.")
        
        # Use LLM to extract structured job description
        extraction_prompt = f"""Extract the job description information from the following LinkedIn job posting content.

URL: {linkedin_url}

Content:
{page_content[:10000]}  # Limit content to avoid token limits

Please extract:
1. Job title
2. Company name
3. Location
4. Full job description
5. Key requirements and qualifications (skills, experience, education)
6. Key responsibilities

If any information is missing, indicate "Not specified"."""

        job_desc = self.llm_structured.invoke([HumanMessage(content=extraction_prompt)])
        return job_desc
    
    def read_resume(self, resume_path: str) -> str:
        """Read resume from file (supports .txt, .md, and can be extended for PDF/DOCX)"""
        path = Path(resume_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {resume_path}")
        
        if path.suffix.lower() == '.txt' or path.suffix.lower() == '.md':
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        elif path.suffix.lower() == '.pdf':
            # For PDF, you would need PyPDF2 or pdfplumber
            # This is a placeholder - you can extend this
            raise NotImplementedError("PDF parsing not yet implemented. Please convert to .txt or .md first.")
        elif path.suffix.lower() in ['.docx', '.doc']:
            # For DOCX, you would need python-docx
            # This is a placeholder
            raise NotImplementedError("DOCX parsing not yet implemented. Please convert to .txt or .md first.")
        else:
            # Try to read as text anyway
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    
    def align_resume(self, resume_content: str, job_description: JobDescription) -> str:
        """
        Use LLM to align resume content with job description
        """
        print("📝 Aligning resume with job description...")
        
        alignment_prompt = f"""You are a professional resume writer. Your task is to update and align a resume to match a specific job description.

JOB DESCRIPTION:
Title: {job_description.title}
Company: {job_description.company}
Location: {job_description.location}

Requirements:
{job_description.requirements}

Responsibilities:
{job_description.responsibilities}

Full Description:
{job_description.description}

CURRENT RESUME:
{resume_content}

INSTRUCTIONS:
1. Analyze the job description and identify key skills, technologies, and experiences required
2. Review the current resume and identify relevant experiences that match the job requirements
3. Update the resume to:
   - Highlight relevant skills and experiences that match the job requirements
   - Reorder sections if needed to emphasize most relevant qualifications
   - Add or modify bullet points to align with job responsibilities
   - Use keywords from the job description naturally throughout the resume
   - Ensure all sections (Summary, Experience, Skills, Education) are optimized
4. Maintain the original format and structure as much as possible
5. Do NOT fabricate experiences or skills - only emphasize and reframe existing content
6. Keep the resume professional and ATS-friendly

Return the updated resume in the same format as the original."""

        response = self.llm.invoke([HumanMessage(content=alignment_prompt)])
        return response.content
    
    def process(self, linkedin_url: str, resume_path: str, output_path: Optional[str] = None) -> str:
        """
        Complete workflow: extract job description, read resume, align, and save
        """
        # Extract job description
        job_desc = self.extract_job_description(linkedin_url)
        print(f"\n✅ Extracted Job Description:")
        print(f"   Title: {job_desc.title}")
        print(f"   Company: {job_desc.company}")
        print(f"   Location: {job_desc.location}")
        
        # Read resume
        print(f"\n📄 Reading resume from: {resume_path}")
        resume_content = self.read_resume(resume_path)
        
        # Align resume
        aligned_resume = self.align_resume(resume_content, job_desc)
        
        # Save aligned resume
        if output_path is None:
            # Create output filename based on input
            input_path = Path(resume_path)
            output_path = str(input_path.parent / f"{input_path.stem}_aligned{input_path.suffix}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(aligned_resume)
        
        print(f"\n✅ Aligned resume saved to: {output_path}")
        return aligned_resume


def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python resume_aligner.py <linkedin_job_url> <resume_file_path> [output_file_path]")
        print("\nExample:")
        print("  python resume_aligner.py https://www.linkedin.com/jobs/view/123456 resume.txt")
        print("  python resume_aligner.py https://www.linkedin.com/jobs/view/123456 resume.txt aligned_resume.txt")
        sys.exit(1)
    
    linkedin_url = sys.argv[1]
    resume_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    aligner = ResumeAligner()
    aligner.process(linkedin_url, resume_path, output_path)


if __name__ == "__main__":
    main()
