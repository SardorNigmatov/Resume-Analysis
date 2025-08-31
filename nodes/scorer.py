from typing import Dict, Optional
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from schemas import ResumeExtracted

# HR qarorini ifodalovchi model
class HRDecision(BaseModel):
    overall_score: int         # Umumiy baho (0-100)
    skills_score: int          # Ko‘nikmalar bahosi (0-100)
    education_score: int       # Ta’lim bahosi (0-100)
    experience_score: int      # Tajriba bahosi (0-100)
    decision: str              # "PASS" yoki "REJECT"
    rationale: str             # Qaror sababi
    improvements: Optional[str] = None   # Yaxshilash bo‘yicha tavsiyalar (ixtiyoriy)

# AI ga beriladigan system prompt
scorer_system = (
    "Siz HR skrining (dastlabki tekshiruv) yordamchisiz. "
    "Nomzodning rezyumesidan chiqarilgan ma’lumotlarni ish talablariga solishtiring. "
    "Adolatli bo‘ling, lekin qat’iy baholang. "
    "Har bir sohani (ko‘nikmalar/ta’lim/tajriba) 0-100 oralig‘ida baholang. "
    "Solishtirishdan oldin barcha ko‘nikmalarni kichik harflarga aylantiring. "
    "Umumiy ball threshold (chegaradan) yuqori bo‘lsa va kamida 70% muhim ko‘nikmalar mavjud bo‘lsa "
    "gina qarorni PASS qiling. Aks holda REJECT."
)

# Prompt shabloni
scorer_prompt = ChatPromptTemplate.from_messages([
    ("system", scorer_system),
    ("human", 
     "Ish ta’rifi:\n```\n{job_description}\n```\n\n"
     "Minimal tajriba yillari: {min_years}\n"
     "Majburiy ko‘nikmalar: {must_have_skills}\n"
     "Afzallik beruvchi ko‘nikmalar: {nice_to_have_skills}\n"
     "PASS thresholddi (umumiy ball): {threshold}\n\n"
     "Rezyumedan chiqarilgan ma’lumot (JSON): {extracted_json}\n\n"
     "HRDecision sxemasiga mos keladigan JSON qaytaring (decision = 'PASS' yoki 'REJECT').")
])

# LLM modeli
_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Chain (prompt + model + HRDecision)
score_chain = scorer_prompt | _llm.with_structured_output(HRDecision)

def scorer_node(state: Dict) -> Dict:
    """
    Kirish:
        state['extracted'] -> ResumeExtracted obyekt
        state['job_description'] -> Ish ta’rifi
        state['min_years'] -> Minimal tajriba
        state['must_have_skills'] -> Majburiy ko‘nikmalar
        state['nice_to_have_skills'] -> Afzallik beruvchi ko‘nikmalar
        state['threshold'] -> Chegara ball

    Chiqish:
        {
            'decision': 'PASS' yoki 'REJECT',
            'reasons': [...],
            'improvements': [...],
            'score': {
                'overall_score': int,
                'skills_score': int,
                'education_score': int,
                'experience_score': int
            }
        }
    """
    extracted: ResumeExtracted = state.get("extracted")
    threshold: int = state.get("threshold", 70)

    # Modeldan natija olish
    result: HRDecision = score_chain.invoke(
        {
            "job_description": state.get("job_description"),
            "min_years": state.get("min_years"),
            "must_have_skills": [s.lower() for s in state.get("must_have_skills", [])],
            "nice_to_have_skills": [s.lower() for s in state.get("nice_to_have_skills", [])],
            "threshold": threshold,
            "extracted_json": extracted.model_dump_json(indent=2)
        }
    )

    # Yakuniy natija
    return {
        "decision": result.decision,
        "reasons": [result.rationale] if result.rationale else [],
        "improvements": [result.improvements] if result.improvements else [],
        "score": {
            "overall_score": result.overall_score,
            "skills_score": result.skills_score,
            "education_score": result.education_score,
            "experience_score": result.experience_score
        }
    }
