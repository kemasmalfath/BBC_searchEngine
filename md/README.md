# 📰 The BBC Chronicle

## Sistem Temu Kembali Informasi Artikel Berita BBC News
### UAS Mata Kuliah Temu Kembali Informasi (STKI) — COM620321
### Universitas Lampung | Periode 2025–2026 Genap

---

## 📋 Daftar Isi

1. [Deskripsi Proyek](#-deskripsi-proyek)
2. [Konsep Sistem Temu Kembali Informasi](#-konsep-sistem-temu-kembali-informasi)
3. [Arsitektur Sistem](#-arsitektur-sistem)
4. [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
5. [Struktur Folder](#-struktur-folder)
6. [Cara Install & Menjalankan](#-cara-install--menjalankan)
7. [Cara Menjalankan di Google Colab](#-cara-menjalankan-di-google-colab)
8. [Penjelasan Modul](#-penjelasan-modul)
9. [Preprocessing Teks](#-preprocessing-teks)
10. [Indexing & TF-IDF](#-indexing--tf-idf)
11. [Cosine Similarity](#-cosine-similarity)
12. [Evaluasi Sistem IR](#-evaluasi-sistem-ir)
13. [Contoh Query Pengujian](#-contoh-query-pengujian)
14. [Pembagian Tugas Kelompok](#-pembagian-tugas-kelompok)
15. [Materi Presentasi](#-materi-presentasi)
16. [Pertanyaan Dosen & Jawaban](#-pertanyaan-dosen--jawaban)

---

## 📝 Deskripsi Proyek

Proyek ini membangun **Sistem Temu Kembali Informasi (Information Retrieval System)** berbasis web menggunakan Flask. Sistem ini mampu mencari artikel berita BBC News yang paling relevan berdasarkan query pengguna.

**Tema:**
> "Sistem Temu Kembali Informasi Artikel Berita Menggunakan TF-IDF dan Cosine Similarity"

**Dataset:** BBC News Dataset (~2.225 artikel berita dari 5 kategori)

**Metode:** Vector Space Model dengan TF-IDF dan Cosine Similarity

---

## 🎓 Konsep Sistem Temu Kembali Informasi

### Apa itu Information Retrieval (IR)?

**Information Retrieval (Temu Kembali Informasi)** adalah bidang ilmu yang mempelajari bagaimana menemukan informasi (dokumen, teks, gambar) yang relevan dari koleksi besar berdasarkan kebutuhan informasi pengguna (query).

### Komponen Utama Sistem IR:

1. **Query Processing** — Memproses input pengguna menjadi representasi yang dapat dibandingkan
2. **Document Processing** — Memproses koleksi dokumen (preprocessing, indexing)
3. **Matching/Retrieval** — Mencocokkan query dengan dokumen untuk menemukan yang relevan
4. **Ranking** — Mengurutkan dokumen berdasarkan tingkat relevansi
5. **Evaluation** — Mengevaluasi performa sistem menggunakan metrik standar

### Alur Kerja Sistem:

```
User Query → Preprocessing → TF-IDF Transform → Cosine Similarity → Ranking → Hasil
                                                        ↑
Dataset → Preprocessing → TF-IDF Indexing ─────────────┘
```

### Mengapa TF-IDF + Cosine Similarity?

- **TF-IDF**: Memberikan bobot kata berdasarkan frekuensi di dokumen (TF) dan keunikan di koleksi (IDF). Kata yang sering di satu dokumen tapi jarang di dokumen lain mendapat bobot tinggi.
- **Cosine Similarity**: Mengukur kesamaan arah antara vektor query dan dokumen. Tidak terpengaruh panjang dokumen. Nilai 0-1 (0 = tidak mirip, 1 = identik).

---

## 🏗 Arsitektur Sistem

```
┌──────────────────────────────────────────────────┐
│                    USER INTERFACE                 │
│         (HTML + CSS + Bootstrap + Flask)          │
│   ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│   │ Search   │  │ History  │  │  Evaluation  │  │
│   │ Page     │  │ Page     │  │  Page        │  │
│   └────┬─────┘  └──────────┘  └──────────────┘  │
│        │                                          │
├────────┼──────────────────────────────────────────┤
│        ▼          FLASK BACKEND (app.py)          │
│   ┌──────────────────────────────────────────┐   │
│   │  Route: /search (POST)                    │   │
│   │  Route: /history (GET)                    │   │
│   │  Route: /evaluation (GET)                 │   │
│   │  Route: /upload (POST)                    │   │
│   │  Route: /article/<id> (GET)               │   │
│   └────┬─────────┬────────────┬──────────────┘   │
│        │         │            │                    │
├────────┼─────────┼────────────┼────────────────────┤
│        ▼         ▼            ▼     CORE MODULES   │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │preproc.py│ │indexing. │ │  evaluation.py   │  │
│  │          │ │py        │ │                  │  │
│  │-casefold │ │-tfidf    │ │ -precision@k     │  │
│  │-tokenize │ │-save/load│ │ -recall          │  │
│  │-stopword │ │          │ │ -MAP             │  │
│  │-stemming │ │          │ │ -ground truth    │  │
│  └──────────┘ └──────────┘ └──────────────────┘  │
│        ▲              ▲                            │
│        │              │                            │
│  ┌─────┴──────┐ ┌─────┴──────┐                    │
│  │ search.py  │ │   models/  │                    │
│  │            │ │            │                    │
│  │-cosine sim │ │ *.pkl      │                    │
│  │-ranking    │ │ (pickle)   │                    │
│  │-highlight  │ │            │                    │
│  └────────────┘ └────────────┘                    │
└──────────────────────────────────────────────────┘
```

---

## 💻 Teknologi yang Digunakan

| Komponen | Teknologi | Fungsi |
|----------|-----------|--------|
| Backend | Python 3.x + Flask | Web server & logic |
| Frontend | HTML5 + CSS3 + Bootstrap 5 | Antarmuka pengguna |
| IR Model | TF-IDF (sklearn) | Pembobotan term |
| Similarity | Cosine Similarity (sklearn) | Pengukuran kesamaan |
| NLP | NLTK | Stopwords, Stemming |
| Data | Pandas | Pengolahan DataFrame |
| Persistence | Pickle | Penyimpanan model |
| History | JSON | Riwayat pencarian |

---

## 📁 Struktur Folder

```
STKI_Berita_Web/  (TKI/)
│
├── dataset/                    ← Dataset BBC News (di-extract dari ZIP)
│   └── News Articles/
│       ├── business/           ← Artikel berita bisnis
│       ├── entertainment/      ← Artikel berita hiburan
│       ├── politics/           ← Artikel berita politik
│       ├── sport/              ← Artikel berita olahraga
│       └── tech/               ← Artikel berita teknologi
│
├── templates/
│   └── index.html              ← Template HTML (search, results, history, eval)
│
├── static/
│   └── style.css               ← Styling CSS (modern, responsive)
│
├── models/                     ← Model TF-IDF tersimpan (auto-generated)
│   ├── tfidf_vectorizer.pkl    ← TfidfVectorizer object
│   ├── tfidf_matrix.pkl        ← TF-IDF sparse matrix
│   └── dataframe.pkl           ← DataFrame dokumen
│
├── history/                    ← Riwayat pencarian (auto-generated)
│   └── search_history.json     ← File JSON riwayat
│
├── preprocessing.py            ← Modul preprocessing teks
├── indexing.py                 ← Modul indexing TF-IDF
├── search.py                   ← Modul pencarian & ranking
├── evaluation.py               ← Modul evaluasi (P@K, Recall, MAP)
├── app.py                      ← Aplikasi utama Flask
├── requirements.txt            ← Daftar library Python
└── README.md                   ← Dokumentasi proyek (file ini)
```

---

## 🚀 Cara Install & Menjalankan

### Prasyarat
- Python 3.8 atau lebih baru
- pip (Python package manager)

### Langkah-langkah:

#### 1. Clone / Download Proyek
```bash
cd TKI
```

#### 2. Install Library
```bash
pip install -r requirements.txt
```

#### 3. Download NLTK Data (otomatis, tapi bisa manual)
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

#### 4. Jalankan Aplikasi
```bash
python app.py
```

#### 5. Buka Browser
```
http://localhost:5000
```

#### 6. Upload Dataset
- Klik tombol upload di halaman utama
- Pilih file ZIP dataset BBC News (`archive (7).zip`)
- Tunggu proses extract & indexing selesai
- Sistem siap digunakan!

---

## ☁ Cara Menjalankan di Google Colab

### Langkah 1: Upload semua file proyek ke Colab

```python
# Di Google Colab, upload file ZIP proyek
from google.colab import files
uploaded = files.upload()  # Upload archive (7).zip
```

### Langkah 2: Install library

```python
!pip install flask pandas numpy scikit-learn nltk tabulate
```

### Langkah 3: Extract dataset

```python
import zipfile
with zipfile.ZipFile('archive (7).zip', 'r') as zip_ref:
    zip_ref.extractall('dataset')
```

### Langkah 4: Upload file proyek

```python
# Upload semua file .py, templates/, static/
# Atau clone dari repository
```

### Langkah 5: Jalankan Flask dengan ngrok

```python
# Install pyngrok untuk tunnel
!pip install pyngrok

from pyngrok import ngrok

# Set auth token (daftar gratis di ngrok.com)
ngrok.set_auth_token("YOUR_NGROK_TOKEN")

# Jalankan Flask di background
import subprocess
proc = subprocess.Popen(['python', 'app.py'])

# Buat tunnel
public_url = ngrok.connect(5000)
print(f"Website bisa diakses di: {public_url}")
```

### Alternatif: Jalankan tanpa ngrok (flask-ngrok)

```python
!pip install flask-ngrok

# Tambahkan di app.py sebelum app.run():
from flask_ngrok import run_with_ngrok
run_with_ngrok(app)
app.run()
```

---

## 📦 Penjelasan Modul

### 1. `preprocessing.py` — Preprocessing Teks

Modul ini memproses teks mentah agar siap untuk indexing dan pencarian.

**Fungsi-fungsi:**
| Fungsi | Input | Output | Keterangan |
|--------|-------|--------|------------|
| `case_folding(text)` | String | String lowercase | Mengubah ke huruf kecil |
| `tokenize(text)` | String | List of tokens | Memecah jadi kata-kata |
| `remove_stopwords(tokens)` | List | List (filtered) | Hapus kata umum |
| `stem(tokens)` | List | List (stemmed) | Ubah ke bentuk dasar |
| `preprocess_text(text)` | String | String (clean) | Pipeline lengkap |

### 2. `indexing.py` — Indexing TF-IDF

Modul ini membangun index dokumen menggunakan TF-IDF.

**Fungsi-fungsi:**
| Fungsi | Keterangan |
|--------|------------|
| `build_tfidf_index(docs)` | Buat TF-IDF matrix dari list dokumen |
| `save_model(vec, matrix)` | Simpan model ke file pickle |
| `load_model()` | Load model dari pickle |

### 3. `search.py` — Pencarian & Ranking

Modul ini melakukan pencarian dokumen berdasarkan query.

**Fungsi-fungsi:**
| Fungsi | Keterangan |
|--------|------------|
| `search_query(query, ...)` | Cari dokumen relevan, return top-K |
| `save_search_history(...)` | Simpan riwayat ke JSON |
| `load_search_history()` | Baca riwayat dari JSON |
| `highlight_keywords(text, query)` | Tandai kata kunci di hasil |

### 4. `evaluation.py` — Evaluasi Sistem

Modul ini mengevaluasi performa sistem IR.

**Fungsi-fungsi:**
| Fungsi | Keterangan |
|--------|------------|
| `precision_at_k(...)` | Hitung Precision@K |
| `recall(...)` | Hitung Recall |
| `average_precision(...)` | Hitung Average Precision |
| `mean_average_precision(...)` | Hitung MAP |
| `run_evaluation(...)` | Jalankan evaluasi lengkap |

### 5. `app.py` — Aplikasi Flask

File utama yang menghubungkan semua modul.

**Routes:**
| Route | Method | Keterangan |
|-------|--------|------------|
| `/` | GET | Halaman utama (search bar) |
| `/search` | POST | Proses pencarian |
| `/history` | GET | Riwayat pencarian |
| `/evaluation` | GET | Evaluasi sistem |
| `/article/<id>` | GET | Detail artikel |
| `/upload` | POST | Upload dataset ZIP |

---

## 🔧 Preprocessing Teks

### Mengapa Preprocessing Penting?

Preprocessing membersihkan teks agar sistem bisa fokus pada kata-kata yang bermakna. Tanpa preprocessing, kata seperti "The" dan "the" dianggap berbeda, dan kata-kata umum akan mendominasi hasil.

### Tahapan Preprocessing:

```
Input: "The Football World Cup 2024 is AMAZING!"
  │
  ▼ 1. Case Folding
  "the football world cup 2024 is amazing!"
  │
  ▼ 2. Tokenization
  ["the", "football", "world", "cup", "2024", "is", "amazing"]
  │
  ▼ 3. Stopword Removal
  ["football", "world", "cup", "2024", "amazing"]
  │
  ▼ 4. Stemming (Porter)
  ["footbal", "world", "cup", "2024", "amaz"]
  │
  ▼ 5. Join
Output: "footbal world cup 2024 amaz"
```

### Pengaruh Preprocessing terhadap IR:

| Tahap | Pengaruh |
|-------|----------|
| Case Folding | Menyamakan representasi → vocabulary lebih kecil |
| Tokenization | Memecah teks → unit yang dapat diproses |
| Stopword Removal | Menghapus noise → fokus pada kata bermakna |
| Stemming | Menyamakan variasi kata → meningkatkan recall |

---

## 📊 Indexing & TF-IDF

### Apa itu TF-IDF?

**TF-IDF (Term Frequency – Inverse Document Frequency)** adalah metode pembobotan kata yang menunjukkan seberapa penting suatu kata dalam suatu dokumen relatif terhadap seluruh koleksi.

### Rumus:

```
TF(t,d) = Frekuensi term t dalam dokumen d / Total term dalam dokumen d

IDF(t) = log(N / df(t))
  dimana N = total dokumen, df(t) = jumlah dokumen yang mengandung term t

TF-IDF(t,d) = TF(t,d) × IDF(t)
```

### Contoh:

Misalkan ada 3 dokumen:
- D1: "football world cup" 
- D2: "stock market economy"
- D3: "football championship league"

Kata "football" muncul di D1 dan D3 (2 dari 3 dokumen):
- IDF("football") = log(3/2) = 0.176
- TF-IDF di D1 = (1/3) × 0.176 = 0.059

Kata "cup" hanya muncul di D1 (1 dari 3 dokumen):
- IDF("cup") = log(3/1) = 0.477
- TF-IDF di D1 = (1/3) × 0.477 = 0.159

→ "cup" memiliki bobot lebih tinggi karena lebih unik.

### TF-IDF Matrix:

```
         football  world  cup  stock  market  economy  championship  league
D1:      0.059    0.159  0.159  0      0       0       0             0
D2:      0        0      0      0.159  0.159   0.159   0             0
D3:      0.059    0      0      0      0       0       0.159         0.159
```

---

## 📐 Cosine Similarity

### Apa itu Cosine Similarity?

Cosine Similarity mengukur kesamaan antara dua vektor berdasarkan sudut antara mereka. Semakin kecil sudutnya, semakin mirip.

### Rumus:

```
cos(θ) = (A · B) / (||A|| × ||B||)

dimana:
A · B     = dot product (perkalian elemen-per-elemen lalu dijumlahkan)
||A||     = norm/panjang vektor A
||B||     = norm/panjang vektor B
```

### Kelebihan Cosine Similarity:

- Nilai antara **0** (tidak mirip) dan **1** (identik)
- **Tidak terpengaruh panjang dokumen** (dokumen panjang vs pendek fair)
- Efisien untuk sparse vectors (TF-IDF biasanya sparse)
- Standard dalam Information Retrieval

### Contoh:

```
Query:  "football cup"  → vektor: [0.5, 0, 0.5, 0, 0, 0, 0, 0]
D1:     "football world cup" → vektor: [0.3, 0.3, 0.3, 0, 0, 0, 0, 0]
D2:     "stock market" → vektor: [0, 0, 0, 0.5, 0.5, 0, 0, 0]

cos(Query, D1) = (0.5×0.3 + 0×0.3 + 0.5×0.3) / (0.707 × 0.52) = 0.82
cos(Query, D2) = (0.5×0 + 0×0.5 + 0.5×0) / (0.707 × 0.707) = 0.00

→ D1 lebih relevan (score 0.82 vs 0.00)
```

---

## 📈 Evaluasi Sistem IR

### Mengapa Evaluasi Penting?

Evaluasi diperlukan untuk mengukur seberapa baik sistem dalam menemukan dokumen yang relevan. Tanpa evaluasi, kita tidak tahu apakah sistem berfungsi dengan benar.

### Komponen Evaluasi:

1. **Query Pengujian** — 10 query yang akan diuji
2. **Ground Truth** — Jawaban yang "benar" (kategori relevan) untuk setiap query
3. **Metrik** — Precision@5, Recall, MAP

### 10 Query Pengujian:

| # | Query | Kategori Relevan |
|---|-------|-----------------|
| 1 | football world cup | sport |
| 2 | government election | politics |
| 3 | stock market crash | business |
| 4 | smartphone technology | tech |
| 5 | movie awards ceremony | entertainment |
| 6 | internet security threat | tech |
| 7 | oil price economy | business |
| 8 | music album release | entertainment |
| 9 | climate change policy | politics |
| 10 | artificial intelligence computer | tech |

### Cara Menghitung:

**Precision@5:**
```
Dari 5 hasil teratas, berapa yang relevan?
Contoh: Dari 5 hasil query "football world cup":
  1. sport ✓
  2. sport ✓  
  3. sport ✓
  4. business ✗
  5. sport ✓

Precision@5 = 4/5 = 0.80
```

**Recall:**
```
Berapa persen dokumen relevan yang berhasil ditemukan?
Contoh: Ada 100 artikel sport di dataset, ditemukan 4 di top-5:

Recall = 4/100 = 0.04
(Recall rendah karena hanya mengambil 5 dari ratusan dokumen relevan)
```

**Average Precision:**
```
Precision dihitung di setiap posisi dokumen relevan:
  Posisi 1: sport ✓ → P@1 = 1/1 = 1.0
  Posisi 2: sport ✓ → P@2 = 2/2 = 1.0
  Posisi 3: sport ✓ → P@3 = 3/3 = 1.0
  Posisi 4: business ✗ → skip
  Posisi 5: sport ✓ → P@5 = 4/5 = 0.8

AP = (1.0 + 1.0 + 1.0 + 0.8) / 4 = 0.95
```

**MAP:**
```
MAP = Rata-rata AP dari seluruh 10 query
MAP = (AP1 + AP2 + ... + AP10) / 10
```

---

## 🧪 Contoh Query Pengujian

### Contoh Hasil Pencarian

**Query: "football world cup"**

```
Rank  Kategori       Score    Judul
1     sport          0.8912   001.txt
2     sport          0.7234   045.txt  
3     sport          0.6891   120.txt
4     sport          0.5432   078.txt
5     business       0.3211   015.txt
```

**Query: "stock market crash"**

```
Rank  Kategori       Score    Judul
1     business       0.7654   023.txt
2     business       0.7123   089.txt
3     business       0.6543   012.txt
4     business       0.5678   056.txt
5     business       0.4321   034.txt
```

---

## 👥 Pembagian Tugas Kelompok

### Saran Pembagian yang Adil (Balanced) untuk 5 Anggota:

| Anggota | Peran / Fokus | Berkas Utama | Tanggung Jawab & Deskripsi Tugas |
|:---:|---|---|---|
| **Anggota 1** | **NLP Preprocessing & Dataset Manager** | `preprocessing.py`, folder `dataset/` | - Mengimplementasikan pembersihan teks (case folding, tokenization, stopword removal, stemming).<br>- Mengelola dataset mentah dan proses pembacaan file.<br>- Menyusun materi teori preprocessing untuk presentasi. |
| **Anggota 2** | **Indexing & Storage Engineer** | `indexing.py`, folder `models/` | - Membangun representasi matriks TF-IDF dari dokumen.<br>- Mengoptimasi penyimpanan & pembacaan model menggunakan library `pickle`.<br>- Menyusun dokumentasi teknis indexing untuk presentasi. |
| **Anggota 3** | **Search Engine & Evaluation Analyst** | `search.py`, `evaluation.py` | - Menghitung kemiripan query dengan Cosine Similarity.<br>- Mengimplementasikan sorting relevansi dan pencocokan keyword.<br>- Menghitung metrik performa sistem (Precision@5, Recall, MAP) menggunakan query pengujian. |
| **Anggota 4** | **Backend Integrator & Git Manager (Lead)** | `app.py`, setup repository GitHub | - Menghubungkan seluruh modul python ke server Flask.<br>- Mengurus routing web Flask (`/search`, `/history`, `/evaluation`, dll).<br>- Bertindak sebagai Git Master (setup repo, handle merge conflicts, deployment). |
| **Anggota 5** | **Frontend Designer & Responsive UI/UX** | `templates/index.html`, `static/style.css` | - Merancang tampilan visual bertema koran editorial "The BBC Chronicle".<br>- Membuat layout responsif agar nyaman dibuka di mobile/tablet.<br>- Mengatur CSS animations, styling card, interaktivitas, dan visual pendukung. |


### Semua Anggota Wajib Memahami:
- Konsep dasar Information Retrieval
- Cara kerja TF-IDF dan Cosine Similarity
- Alur kerja sistem secara keseluruhan
- Cara menjalankan aplikasi

---

## 🎤 Materi Presentasi

### Struktur Presentasi (15-20 menit):

1. **Pendahuluan** (2 menit)
   - Latar belakang Information Retrieval
   - Tujuan proyek

2. **Konsep & Metode** (5 menit)
   - Vector Space Model
   - TF-IDF
   - Cosine Similarity
   - Preprocessing

3. **Arsitektur Sistem** (3 menit)
   - Flowchart
   - Struktur modul
   - Teknologi yang digunakan

4. **Demo** (5 menit)
   - Tampilan website
   - Contoh pencarian
   - Hasil dengan similarity score
   - Search history

5. **Evaluasi** (3 menit)
   - Metrik (P@K, Recall, MAP)
   - Hasil evaluasi
   - Analisis

6. **Kesimpulan** (2 menit)
   - Ringkasan
   - Kelebihan & kekurangan
   - Pengembangan ke depan

---

## ❓ Pertanyaan Dosen & Jawaban

### Q1: Apa itu TF-IDF dan bagaimana cara kerjanya?

**A:** TF-IDF (Term Frequency - Inverse Document Frequency) adalah metode pembobotan kata. TF mengukur seberapa sering kata muncul dalam satu dokumen. IDF mengukur seberapa unik kata tersebut di seluruh koleksi. TF-IDF = TF × IDF. Kata yang sering di satu dokumen tapi jarang di koleksi mendapat bobot tinggi, artinya kata tersebut sangat representatif untuk dokumen itu.

### Q2: Mengapa menggunakan Cosine Similarity, bukan Euclidean Distance?

**A:** Cosine Similarity mengukur kesamaan arah vektor, bukan jarak. Keuntungannya: (1) Tidak terpengaruh panjang dokumen — dokumen panjang dan pendek bisa dibandingkan secara fair. (2) Nilainya selalu 0-1 sehingga mudah diinterpretasi. (3) Efisien untuk sparse vectors seperti TF-IDF.

### Q3: Apa fungsi preprocessing dan apa yang terjadi jika tidak dilakukan?

**A:** Preprocessing membersihkan teks agar fokus pada kata bermakna. Tanpa case folding, "Football" dan "football" dianggap berbeda. Tanpa stopword removal, kata seperti "the", "is" mendominasi. Tanpa stemming, "running" dan "run" dianggap kata berbeda. Akibatnya, akurasi pencarian menurun drastis.

### Q4: Bagaimana cara menghitung MAP?

**A:** MAP = Mean Average Precision. Langkah: (1) Untuk setiap query, hitung AP (Average Precision) = rata-rata precision di setiap posisi relevan. (2) MAP = rata-rata AP dari seluruh query pengujian. MAP adalah metrik paling komprehensif karena mempertimbangkan urutan (posisi) dokumen relevan.

### Q5: Apa perbedaan Precision dan Recall?

**A:** Precision mengukur "dari yang dikembalikan, berapa yang relevan?" (kualitas). Recall mengukur "dari yang relevan, berapa yang berhasil ditemukan?" (cakupan). Biasanya ada trade-off: meningkatkan satu akan menurunkan yang lain.

### Q6: Mengapa Recall rendah pada sistem ini?

**A:** Recall rendah karena kita hanya mengambil top-5 hasil, sementara ada ratusan dokumen relevan per kategori. Ini adalah trade-off yang disengaja — pengguna biasanya hanya melihat beberapa hasil teratas (seperti Google). Yang penting adalah Precision tinggi (hasil teratas harus relevan).

### Q7: Apa itu Ground Truth dan mengapa diperlukan?

**A:** Ground Truth adalah "jawaban benar" yang sudah ditentukan sebelumnya. Dalam proyek ini, ground truth mendefinisikan kategori yang seharusnya relevan untuk setiap query. Tanpa ground truth, kita tidak bisa menghitung metrik evaluasi karena tidak ada acuan "relevan" atau "tidak relevan".

### Q8: Apa kelebihan dan kekurangan sistem ini?

**A:** Kelebihan: (1) Sederhana dan mudah dipahami. (2) Tidak butuh training data. (3) Cepat untuk dataset kecil-menengah. (4) Interpretable — bisa dijelaskan mengapa dokumen relevan. Kekurangan: (1) Tidak memahami semantik (sinonim tidak terdeteksi). (2) Bag-of-words — tidak memperhatikan urutan kata. (3) Bergantung pada exact keyword matching.

### Q9: Apa perbedaan TF-IDF dengan Bag of Words (BoW)?

**A:** BoW hanya menghitung frekuensi kata (TF saja). TF-IDF menambahkan faktor IDF yang memberikan bobot rendah pada kata umum dan bobot tinggi pada kata unik. Hasilnya, TF-IDF lebih akurat untuk pencarian karena tidak didominasi kata-kata umum.

### Q10: Bagaimana jika dataset lebih besar (misalnya jutaan dokumen)?

**A:** Untuk dataset sangat besar: (1) Gunakan inverted index untuk efisiensi. (2) Gunakan approximate nearest neighbor (ANN) untuk pencarian cepat. (3) Gunakan distributed computing (Elasticsearch, Solr). (4) Pertimbangkan model neural (BERT, dll) untuk pemahaman semantik. Namun, untuk skala ribuan dokumen, TF-IDF + Cosine Similarity sudah cukup efisien.

---

## 📝 Lisensi

Proyek ini dibuat untuk keperluan akademis (UAS STKI COM620321 Universitas Lampung).

Dataset BBC News berasal dari sumber publik untuk keperluan riset dan pendidikan.
