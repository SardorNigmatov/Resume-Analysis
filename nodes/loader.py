from typing import Dict
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def loader_node(state: Dict) -> Dict:
    """
    Kirish (Input):
        state['resume_path'] -> PDF yoki TXT faylning yo‘li (path)
    
    Chiqish (Output):
        {'resume_text': '...'} -> Rezyume matni oddiy text shaklida
    """
    path = state['resume_path']
    ext = os.path.splitext(path)[1].lower()   # fayl kengaytmasini aniqlash

    # PDF fayl uchun yuklovchi
    if ext == '.pdf':
        loader = PyPDFLoader(path)   # ✅ faqat bitta PDF faylni o‘qiydi
    # TXT fayl uchun yuklovchi
    elif ext == '.txt':
        loader = TextLoader(path, encoding='utf8')
    # Boshqa formatlar qo‘llab-quvvatlanmaydi
    else:
        raise ValueError(f"Qo‘llab-quvvatlanmaydigan fayl turi: {ext}")

    # Hujjatni yuklash
    docs = loader.load()
    # Har bir sahifadan matnni olib, bitta stringga qo‘shib chiqish
    text = "\n\n".join(doc.page_content.strip() for doc in docs if doc.page_content)

    return {"resume_text": text}
