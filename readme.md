# 📊 PDF Table Automation Analyzer

**👤 Nama**: Zainal Fattah\
**🆔 NIM**: 32602300013\
**📚 Proyek ini dibuat untuk memenuhi tugas mata kuliah Cloud Computing**

---

## 🦰 Deskripsi Proyek

**Data2Insight** adalah aplikasi berbasis **Streamlit** yang memungkinkan pengguna mengunggah file PDF berisi tabel, kemudian menganalisis tabel tersebut secara otomatis menggunakan **Large Language Model (LLM)** dari [OpenRouter](https://openrouter.ai). Output yang diberikan berupa:

- Narasi analisis dalam bahasa alami (`"Jawaban"`),
- Hasil transformasi tabel (`"tabel"` dalam format JSON),
- dan **kode Python otomatis** (`"kode"`) untuk visualisasi menggunakan `matplotlib` atau `seaborn`.

Semua proses dilakukan secara otomatis dengan bantuan **model **`` dari OpenRouter.

---

## 🔧 Fitur Utama

- 📄 **Ekstraksi tabel PDF** menggunakan `pdfplumber`.
- 🤖 **Prompt otomatis ke LLM** berdasarkan isi tabel & pertanyaan pengguna.
- 📊 **Visualisasi otomatis** berdasarkan instruksi dan output model.
- ✅ Kompatibel dengan Docker dan dapat dijalankan di mana saja tanpa setup manual.
- 🔐 **API Key OpenRouter** diatur melalui environment variable (`KEY1`).

---

## 🏁 Cara Menjalankan Secara Lokal

### 1. Clone repositori ini:

```bash
git clone https://github.com/zainalfattah/data2insight.git
cd data2insight
```

### 2. Buat virtual environment & aktifkan

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/MacOS
```

### 3. Install dependensi Python

```bash
pip install -r requirements.txt
```

### 4. Setel API KEY dari OpenRouter

```bash
set KEY1=sk-xxxxx...  # Windows
# export KEY1=sk-xxxxx...  # Linux/MacOS
```

### 5. Jalankan aplikasi

```bash
streamlit run app/main.py
```

---

## 🐳 Menjalankan dengan Docker

### 1. Build image Docker

```bash
docker build -t data2insight .
```

### 2. Jalankan container

```bash
docker run -p 8501:8501 -e KEY1=sk-xxxxx... data2insight
```

> Buka aplikasi di browser: [http://localhost:8501](http://localhost:8501)

---

## 🚀 Cara Deploy ke Docker Hub

### 1. Tag image dengan nama Docker Hub kamu

```bash
docker tag [nama_image_lokal] [username_dockerhub]/[nama_image]:[tag]
```

### 2. Login dan push ke Docker Hub

```bash
docker login
docker push [username_dockerhub]/[nama_image]:[tag]
```

## Pengguna lain cukup menjalankan:

```bash
docker pull zainalfattah/data2insight:v1
docker run -p 8501:8501 -e KEY1=sk-xxxxx... zainalfattah/data2insight:v1
```

---

## 📁 Struktur Direktori

```
data2insight/
├── app/
│   └── main.py              # Aplikasi Streamlit utama
├── requirements.txt         # Daftar dependensi Python
├── Dockerfile               # Konfigurasi image Docker
├── .dockerignore
└── README.md                # Dokumentasi proyek ini
```

---

## 🌐 Konfigurasi Environment Variable

| Nama Var | Deskripsi                  | Wajib? |
| -------- | -------------------------- | ------ |
| `KEY1`   | API Key dari OpenRouter.ai | ✅ Ya   |

Untuk mendapatkan API key, kunjungi [https://openrouter.ai/](https://openrouter.ai/).

---

## 🧪 Contoh Alur Penggunaan

1. **Upload PDF** berisi tabel.
2. Aplikasi akan otomatis menampilkan tabel yang terdeteksi.
3. Masukkan instruksi atau pertanyaan ke LLM.
4. Klik "Proses via LLM", lalu sistem akan:
   - Mengirim data tabel & pertanyaan ke model LLM,
   - Menampilkan narasi jawaban (`"Jawaban"`),
   - Menampilkan transformasi tabel baru (`"tabel"`),
   - Mengeksekusi kode visualisasi (`"kode"`) dan menampilkan grafik.

---

## 🧛️ Format Prompt ke LLM

```text
Kamu adalah analis data. Berikan output JSON dengan struktur PERSIS seperti ini:
{
  "Jawaban": "Ringkasan insight...",
  "tabel": { "NamaKolom": [..] },
  "kode": "import matplotlib.pyplot as plt ..."
}
```

- Hindari markdown (seperti `json atau `python).
- Kode harus bisa langsung dijalankan tanpa modifikasi.
- Kolom tabel harus seimbang panjangnya.

---

## ⚠️ Keamanan

- Kode Python dari model LLM dijalankan dengan `exec()` secara terisolasi menggunakan `scope` terbatas (`plt`, `pd`).
- Disarankan menambahkan validasi keamanan lebih ketat untuk pemakaian di produksi.

---

## 📄 Lisensi

Proyek ini menggunakan lisensi **MIT License** — bebas digunakan untuk pembelajaran dan pengembangan pribadi.

---

> 🙏 Terima kasih telah membaca.\
> Proyek ini dikerjakan sebagai bagian dari penilaian tugas *Cloud Computing* oleh Zainal Fattah, NIM 32602300013.

