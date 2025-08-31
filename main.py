from constants import (
    JOB_DESCRIPTION,
    MIN_YEARS,
    MUST_HAVE_SKILLS,
    NICE_TO_HAVE_SKILLS,
    THRESHOLD
)
import os
from dotenv import load_dotenv

# .env fayldagi kalitlarni yuklash (API_KEY va boshqalar)
load_dotenv()

def main():
    from graph_builder import graph_builder
    
    # HR pipeline graphini chaqiramiz
    graph = graph_builder()

    # Foydalanuvchidan rezyume fayl manzilini olish
    resume_path = input("Rezyume fayl yo‘lini kiriting: ").strip()

    # Boshlang‘ich state
    initial_state = {
        "resume_path": resume_path,
        "job_description": JOB_DESCRIPTION,
        "min_years": MIN_YEARS,
        "must_have_skills": MUST_HAVE_SKILLS,
        "nice_to_have_skills": NICE_TO_HAVE_SKILLS,
        "threshold": THRESHOLD
    }

    # Graph orqali pipeline’ni ishga tushirish
    final_state = graph.invoke(initial_state)

    # Natijalarni chiqarish
    print("============== HR Skrining Natijasi =============")
    print(f"✅ Qaror: {final_state.get('decision')}")

    print("\n📊 Ballar tafsiloti:")
    for k, v in final_state.get('score', {}).items():
        print(f"  - {k}: {v}")

    print("\n📝 Qaror sabablari:")
    for r in final_state.get('reasons', []):
        print(f"  - {r}")

    print("\n🔧 Yaxshilash bo‘yicha tavsiyalar:")
    for i in final_state.get('improvements', []):
        print(f"  - {i}")

if __name__ == "__main__":
    main()
