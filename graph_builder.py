from typing_extensions import TypedDict
from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()  # .env fayldan atrof-muhit o'zgaruvchilarini yuklash

# Node funksiyalar
from nodes.loader import loader_node
from nodes.extractor import extractor_node
from nodes.scorer import scorer_node

# HR jarayonida ishlatiladigan umumiy State (holat)
class HRState(TypedDict):
    # Kirish (Input) ma’lumotlar
    resume_path: str                # Rezyume fayl manzili (PDF yoki TXT)
    job_description: str            # Ish ta’rifi
    min_years: float                # Minimal tajriba (yillarda)
    must_have_skills: List[str]     # Majburiy ko‘nikmalar
    nice_to_have_skills: List[str]  # Afzallik beruvchi ko‘nikmalar
    threshold: int                  # PASS uchun umumiy ball chegarasi

    # Jarayon davomida hosil bo‘ladigan (Produced) ma’lumotlar
    resume_text: str                # Rezyume matni (oddiy text)
    extracted: Any                  # Extractor’dan olingan strukturalangan ma’lumot
    decision: str                   # "PASS" yoki "REJECT"
    reasons: List[str]              # Qaror sabablari
    improvements: List[str]         # Yaxshilash bo‘yicha tavsiyalar
    score: Dict[str, int]           # Baho tafsilotlari (overall, skills, education, experience)

# HR pipeline graph builder
def graph_builder():
    g = StateGraph(HRState)

    # Node’larni qo‘shish
    g.add_node("loader", loader_node)        # Rezyumeni yuklaydi (PDF/TXT → text)
    g.add_node("extractor", extractor_node)  # Textdan strukturalangan info ajratadi
    g.add_node("scorer", scorer_node)        # Talablarga solishtirib baho beradi

    # Node’lar orasidagi oqim (edges)
    g.add_edge(START, "loader")        # START → loader
    g.add_edge("loader", "extractor")  # loader → extractor
    g.add_edge("extractor", "scorer")  # extractor → scorer
    g.add_edge("scorer", END)          # scorer → END

    return g.compile()
