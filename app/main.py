import os, json, re, io, base64, requests
from io import BytesIO

import streamlit as st
import pandas as pd
import pdfplumber
import matplotlib.pyplot as plt
import seaborn as sns

# === OpenRouter Config ===
API_KEY = os.getenv("KEY1")
if not API_KEY:
    st.error("OPENROUTER_API_KEY belum disetel di environment.")
    st.stop()

OR_URL   = "https://openrouter.ai/api/v1/chat/completions"
MODEL    = "deepseek/deepseek-chat-v3-0324:free"          # 1 model saja
HEADERS  = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://localhost"             # disarankan OpenRouter
}

def call_llm(prompt: str) -> str:
    """Kirim prompt ke OpenRouter & ambil text jawaban."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    r = requests.post(OR_URL, headers=HEADERS, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def strip_markdown_fence(txt: str) -> str:
    """Hilangkan blok ```json ... ``` jika ada."""
    return re.sub(r"```json|```", "", txt, flags=re.I).strip()

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="Data2Insight", layout="centered")
st.title("📊 PDF Table Automation Analyzer")

pdf_file = st.file_uploader("Upload PDF berisi tabel", type=["pdf"])
if not pdf_file:
    st.stop()

# ---- Ekstrak tabel ----
tables = []
with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        for tbl in page.extract_tables():
            if tbl:
                df = pd.DataFrame(tbl[1:], columns=tbl[0])
                tables.append(df)

if not tables:
    st.warning("Tidak ada tabel terdeteksi di PDF.")
    st.stop()

idx = st.selectbox("Pilih Tabel", range(len(tables)), format_func=lambda i:f"Tabel {i+1}")
df  = tables[idx]
st.dataframe(df, use_container_width=True)

user_prompt = st.text_area("Instruksi / pertanyaan Anda:")

if st.button("Proses via LLM"):
    # ------- Prompt LLM ------------
    prompt = f"""
Kamu adalah analis data. Berikan output JSON dengan struktur PERSIS seperti ini:

{{
  "Jawaban": "Jawaban naratif ...",
  "tabel": {{
    "NamaKolom1": [...],
    "NamaKolom2": [...]
  }},
  "kode": "### hanya kode Python (matplotlib / seaborn) ###"
}}

• "tabel" harus berbentuk kolom → list, panjang list sama tiap kolom.  
• "kode" harus bisa langsung dieksekusi tanpa perubahan dan menghasilkan plot.  
• Hindari blok markdown ```json atau ```python, cukup raw JSON saja.
Dataset: {df.to_dict(orient='list')}
Pertanyaan: {user_prompt}
"""
    with st.spinner("Meminta jawaban LLM ..."):
        raw_text = call_llm(prompt)

    st.subheader("Raw Response")
    st.code(raw_text[:500] + ("..." if len(raw_text) > 500 else ""), language="json")

    # -------- Bersihkan & parse JSON ----------
    try:
        clean = strip_markdown_fence(raw_text)
        data  = json.loads(clean)
    except json.JSONDecodeError as e:
        st.error(f"Gagal parse JSON: {e}")
        st.stop()

    # -------- Tampilkan Jawaban & Tabel --------
    st.markdown("### 📝 Jawaban")
    st.write(data.get("Jawaban", "-"))

    vis_df = pd.DataFrame(data.get("tabel", {}))
    if vis_df.empty:
        st.warning("Bagian 'tabel' kosong / format salah.")
        st.stop()

    st.markdown("### 📑 Tabel")
    st.dataframe(vis_df)

    # -------- Jalankan kode visual ----------
    st.markdown("### 📊 Visualisasi Otomatis")
    code_str = data.get("kode", "")
    if not code_str.strip():
        st.warning("Tidak ada 'kode' visualisasi.")
        st.stop()

    st.expander("Lihat Kode").code(code_str, language="python")

    try:
        # Eksekusi kode di scope terisolasi dan tangkap output
        scope = {"plt": plt, "pd": pd}    
        exec(code_str, scope)

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        st.image(buf)
        plt.clf()
    except Exception as e:
        st.error(f"Error saat menjalankan kode visual: {e}")

