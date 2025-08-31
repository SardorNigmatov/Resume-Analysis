import streamlit as st
import requests

# FastAPI server manzili
API_URL = "http://localhost:8080/screen_resume"

st.title("🧑‍💼 HR Screening Assistant")

# Form orqali ma’lumot kiritish
with st.form("hr_form"):
    resume_path = st.text_input("📄 Rezyume fayl manzili (PDF yoki TXT):", "data/resume.pdf")
    job_description = st.text_area("📝 Ish ta’rifi:", "Biz Data Scientist qidirmoqdamiz...")
    min_years = st.number_input("📆 Minimal tajriba (yil):", min_value=0.0, value=2.0, step=0.5)
    must_have_skills = st.text_area("⭐ Majburiy ko‘nikmalar (vergul bilan ajrating):", "python, machine learning, sql")
    nice_to_have_skills = st.text_area("✨ Afzallik beruvchi ko‘nikmalar (vergul bilan ajrating):", "aws, docker")
    threshold = st.slider("📊 PASS thresholddi (umumiy ball):", 50, 100, 70)

    submitted = st.form_submit_button("🔎 Rezyumeni baholash")

if submitted:
    if not resume_path.strip() or not job_description.strip():
        st.warning("❗ Iltimos, rezyume yo‘lini va ish ta’rifini kiriting.")
    else:
        with st.spinner("⏳ Rezyume tahlil qilinmoqda..."):
            payload = {
                "resume_path": resume_path,
                "job_description": job_description,
                "min_years": min_years,
                "must_have_skills": [s.strip() for s in must_have_skills.split(",") if s.strip()],
                "nice_to_have_skills": [s.strip() for s in nice_to_have_skills.split(",") if s.strip()],
                "threshold": threshold
            }
            response = requests.post(API_URL, json=payload)
            data = response.json()

        # Natijalar
        st.subheader("✅ Qaror:")
        decision = data.get("decision", "UNKNOWN")
        if decision == "PASS":
            st.success("Nomzod tanlovdan o‘tdi ✅")
        elif decision == "REJECT":
            st.error("Nomzod tanlovdan o‘tmadi ❌")
        else:
            st.warning("Qaror aniqlanmadi ⚠️")

        st.subheader("📊 Ballar tafsiloti:")
        score = data.get("score", {})
        if score:
            for k, v in score.items():
                st.write(f"  - **{k}**: {v}")
        else:
            st.info("Ballar mavjud emas.")

        st.subheader("📝 Qaror sabablari:")
        reasons = data.get("reasons", [])
        if reasons:
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.info("Sabablar ko‘rsatilmagan.")

        st.subheader("🔧 Yaxshilash bo‘yicha tavsiyalar:")
        improvements = data.get("improvements", [])
        if improvements:
            for i in improvements:
                st.write(f"- {i}")
        else:
            st.info("Tavsiyalar mavjud emas.")
