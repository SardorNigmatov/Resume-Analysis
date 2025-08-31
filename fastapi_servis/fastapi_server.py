from fastapi import FastAPI
from pydantic import BaseModel
from graph_builder import graph_builder
from dotenv import load_dotenv

load_dotenv()  # .env fayldan atrof-muhit o'zgaruvchilarini yuklash

# ---------------------------
# FastAPI app
# ---------------------------
app = FastAPI(title="HR Screening API")

# Graphni yaratamiz
graph = graph_builder()

# ---------------------------
# Request body modeli
# ---------------------------
class HRRequest(BaseModel):
    resume_path: str
    job_description: str
    min_years: float
    must_have_skills: list[str]
    nice_to_have_skills: list[str]
    threshold: int = 70  # default qiymat

# ---------------------------
# Endpoint: rezyumeni baholash
# ---------------------------
@app.post("/screen_resume")
async def screen_resume(request: HRRequest):
    """
    Nomzodning rezyumesini yuklaydi, ma’lumotlarni ajratadi va
    ish talablariga solishtirib PASS/REJECT qaror chiqaradi.
    """
    # Boshlang‘ich state
    state = {
        "resume_path": request.resume_path,
        "job_description": request.job_description,
        "min_years": request.min_years,
        "must_have_skills": request.must_have_skills,
        "nice_to_have_skills": request.nice_to_have_skills,
        "threshold": request.threshold,
    }

    # Graph’ni async rejimda ishga tushiramiz
    result = await graph.ainvoke(state)

    # Natijani JSON qilib qaytaramiz
    return {
        "decision": result.get("decision", ""),
        "score": result.get("score", {}),
        "reasons": result.get("reasons", []),
        "improvements": result.get("improvements", []),
    }
