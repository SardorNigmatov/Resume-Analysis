from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class ResumeExtracted(BaseModel):
    name: Optional[str] = Field(None, description="Candidate full name if present")
    skills: List[str] = Field(default_factory=list, description="Normalized skills list (list)")
    education: Optional[str] = Field(None, description="Highest education level if present")
    years_experience: Optional[int] = Field(None, description="Estimated total years of experience.")
    summary: Optional[str] = Field(None, description="Short summary of the candidate's profile")
    recent_companies: List[str] = Field(default_factory=list, description="Recent employers")
    projects: List[str] = Field(default_factory=list, description="Short list or key projects")


class ScoreBreakdown(BaseModel):
    skill_match: int = Field(description="0-100 skill match score")
    education_match: int = Field(description="0-100 education match score")
    experience_match: int = Field(description="0-100 experience match score")
    overall: int = Field(description="0-100 overall match score")
    
class HRDecision(BaseModel):
    decision: str = Field(description="PASS or REJECT")
    reasons: List[str] = Field(description="Concise reasons supporting the decision")
    improvements: List[str] = Field(description="Suggested improvements for the candidate")
    score: ScoreBreakdown