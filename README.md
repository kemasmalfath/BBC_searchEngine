# The BBC Chronicle - Sistem Temu Kembali Informasi (STKI)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Proyek ini merupakan implementasi **Sistem Temu Kembali Informasi (STKI)** berbasis web untuk mencari artikel berita dari dataset BBC News. Proyek ini dibangun untuk memenuhi syarat **Ujian Akhir Semester (UAS) mata kuliah Temu Kembali Informasi (COM620321) di Universitas Lampung**.

*   **Demo Aplikasi (Live Deployment):** [https://kemas.pythonanywhere.com/](https://kemas.pythonanywhere.com/)

---

## 👥 Anggota Kelompok (Tim Pengembang)

Proyek ini dikembangkan oleh kelompok mahasiswa **Universitas Lampung**:

| Nama Anggota | NPM | Kelas |
| :--- | :--- | :---: |
| **Muhammad Fa'jri Ramadhani** | 2357051004 | A |
| **Nabila Cahaya Putri** | 2357051010 | B |
| **Kemas Muhammad A.I** | 2317051072 | B |
| **S Agung Setiawan** | 2317051011 | B |
| **Khomarul Hidayat** | 2317051029 | A |

---

## 📖 Deskripsi Proyek

**The BBC Chronicle** adalah mesin pencari (*search engine*) artikel berita BBC yang mencakup 5 kategori utama: *Business*, *Entertainment*, *Politics*, *Sport*, dan *Tech*. Sistem ini dibangun menggunakan konsep **Vector Space Model (VSM)** dengan pembobotan **TF-IDF** dan pengukuran kemiripan dokumen menggunakan **Cosine Similarity**.

Sistem ini bersifat dinamis, responsif, dan menyediakan statistik data secara langsung, visualisasi hasil evaluasi performa, serta riwayat pencarian pengguna.

---

## 🛠️ Keselarasan dengan Ketentuan UAS STKI

Sistem ini memenuhi seluruh kriteria wajib dan tambahan yang ditetapkan dalam ketentuan UAS STKI:

| Ketentuan UAS | Implementasi pada Proyek | Berkas Terkait |
| :--- | :--- | :--- |
| **1. Menerima Query** | Form input pencarian dinamis yang menerima kata kunci dari pengguna. | [app.py](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/app.py) |
| **2. Preprocessing Teks** | Meliputi *Case Folding*, *Tokenization*, *Stopword Removal* (NLTK stopwords Inggris), dan *Stemming* (Porter Stemmer). | [preprocessing.py](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/preprocessing.py) |
| **3. Indexing Dokumen** | Ekstraksi fitur dan pembobotan menggunakan TF-IDF. Representasi disimpan dalam format `.pkl` (Pickle) agar server tidak perlu memproses ulang setiap startup. | [indexing.py](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/indexing.py) |
| **4. Menghitung Relevansi** | Menggunakan rumus *Cosine Similarity* untuk membandingkan vektor kueri dengan seluruh dokumen. | [search.py](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/search.py) |
| **5. Ranking & Skor Relevansi** | Hasil pencarian diurutkan dari nilai similarity tertinggi ke terendah (skor > 0) dengan batas pencarian teratas (*Top-K*). | [search.py](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/search.py) |
| **6. Evaluasi Performa** | Pengujian otomatis menggunakan **10 Ground Truth queries** untuk menghitung **Precision@5**, **Recall**, **NDCG@5**, **Average Precision (AP)**, **Mean Average Precision (MAP)**, dan **Global Confusion Matrix** (TP, FP, FN, TN, Akurasi, F1-Score). | [evaluation.py](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/evaluation.py) |
| **7. Dataset Real & Relevan** | Menggunakan dataset BBC News yang terdiri dari 2.225 dokumen berita teks nyata yang dikelompokkan secara terstruktur. | Folder `dataset/` |

---

## ✨ Fitur Unggulan Tambahan

Selain fitur wajib di atas, sistem ini juga dilengkapi dengan:

*   **Fitur Penerjemahan Artikel (*Translation Feature*):** Menerjemahkan judul dan konten berita secara langsung dari bahasa Inggris ke bahasa Indonesia menggunakan API Google Translate (melalui request POST untuk performa stabil).
*   **Riwayat Pencarian (*Search History*):** Riwayat kata kunci pencarian yang dimasukkan pengguna disimpan secara lokal dalam file JSON beserta catatan waktu (WIB) dan jumlah hasil pencarian.
*   **Ekstraksi Judul Otomatis (*Extractive Title Summarization*):** Jika dokumen tidak memiliki judul eksplisit, sistem mengekstrak kalimat paling representatif menggunakan metode frekuensi kata (*extractive summarization*).
*   **Highlight Keyword Pencarian:** Menyorot (*highlight*) kata kunci pencarian pada cuplikan teks hasil pencarian agar pengguna mudah memahami relevansi dokumen.

---

## 📂 Struktur Berkas Proyek

Berikut adalah struktur berkas utama di dalam repositori:

*   [**`app.py`**](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/app.py): Entry point utama aplikasi web berbasis Flask. Menghubungkan logika pemrosesan ke antarmuka pengguna.
*   [**`preprocessing.py`**](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/preprocessing.py): Implementasi pipeline pembersihan teks (case folding, tokenisasi, stopword, stemming) dan ekstraksi judul artikel.
*   [**`indexing.py`**](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/indexing.py): Modul untuk membangun matriks TF-IDF, serta menyimpan/memuat model biner `.pkl`.
*   [**`search.py`**](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/search.py): Modul pencarian dengan Cosine Similarity, perankingan, highlighter kata kunci, dan pencatatan riwayat.
*   [**`evaluation.py`**](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/evaluation.py): Logika pengujian sistem menggunakan 10 query pengujian dan perhitungan metrik performa (Precision, Recall, MAP, NDCG, Confusion Matrix).
*   [**`requirements.txt`**](file:///c:/Users/alfat/Documents/GitHub/BBC_searchEngine/requirements.txt): Daftar dependensi Python yang dibutuhkan untuk menjalankan sistem.
*   **`templates/` & `static/`**: Berkas HTML (antarmuka template) dan stylesheet CSS (desain modern dengan tema *glassmorphism*).

---

## 📊 Detail Query Evaluasi (Ground Truth)

Sistem diuji menggunakan 10 query pengujian berikut yang mewakili masing-masing topik kategori:

1.  `"football world cup"` (Kategori Relevan: **Sport**)
2.  `"government election"` (Kategori Relevan: **Politics**)
3.  `"stock market crash"` (Kategori Relevan: **Business**)
4.  `"smartphone technology"` (Kategori Relevan: **Tech**)
5.  `"movie awards ceremony"` (Kategori Relevan: **Entertainment**)
6.  `"internet security threat"` (Kategori Relevan: **Tech**)
7.  `"oil price economy"` (Kategori Relevan: **Business**)
8.  `"music album release"` (Kategori Relevan: **Entertainment**)
9.  `"climate change policy"` (Kategori Relevan: **Politics**)
10. `"artificial intelligence computer"` (Kategori Relevan: **Tech**)

Evaluasi dapat diakses secara langsung di route `/evaluation` pada web browser Anda untuk melihat visualisasi tabel performa dan matriks evaluasi global.


