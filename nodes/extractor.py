from typing import Dict
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from schemas import ResumeExtracted

# Rezyumeni tahlil qilish uchun prompt
extract_prompt = ChatPromptTemplate.from_messages([
    ("system", "Siz tajribali HR (kadrlar bo‘yicha) mutaxassissiz. Rezyumedan strukturalangan ma’lumotlarni ajratib oling."),
    ("human", 
     "Rezyume matni:\n ```{resume_text}```\n\n"
     "Iltimos, quyidagi kalitlar bilan to‘liq JSON qaytaring: "
     "{{name: string, summary: string, years_of_experience: float, "
     "skills: list (kichik harflarda yozilgan stringlar), education: string, "
     "recent_companies: list, projects: list}}."
    )
])

# LLM model (OpenAI)
_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Rezyumeni strukturalangan holda qaytaruvchi chain
extract_chain = extract_prompt | _llm.with_structured_output(ResumeExtracted)

def extractor_node(state: Dict) -> Dict:
    """
    Kirish:
        state['resume_text']  -> Rezyume matni
    Chiqish:
        {'extracted': ResumeExtracted} -> Strukturalangan natija
    """
    extracted: ResumeExtracted = extract_chain.invoke(
        {"resume_text": state['resume_text']}
    )
    return {'extracted': extracted}
