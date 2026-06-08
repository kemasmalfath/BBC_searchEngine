# 📋 Checklist Kesiapan Presentasi UAS STKI

Dokumen ini memetakan **Ketentuan Resmi Proyek UAS STKI (COM620321)** dengan **Fitur Aplikasi yang Telah Dibuat**. Anda dapat menggunakan dokumen ini sebagai panduan saat presentasi atau sebagai lampiran laporan.

---

## 1. Fitur Wajib Sistem (100% TERPENUHI)
| Ketentuan PDF | Implementasi di Proyek | Status |
|---------------|------------------------|:---:|
| Menerima query dari pengguna | Ada kotak pencarian (*search bar*) di halaman utama. | ✅ |
| Melakukan preprocessing teks | Modul `preprocessing.py` melakukan: Case Folding, Tokenization, Stopword Removal (NLTK), dan Stemming (Porter). | ✅ |
| Melakukan indexing dokumen | Modul `indexing.py` membangun *vocabulary* (10.000 term) dan TF-IDF matrix, lalu disave ke `.pkl`. | ✅ |
| Menghitung relevansi dokumen | Menggunakan perhitungan **Cosine Similarity** di modul `search.py` untuk mengukur jarak query dan dokumen. | ✅ |
| Menampilkan ranking hasil | Hasil pencarian diurutkan dari skor tertinggi ke terendah, dan sistem mengambil Top-5. | ✅ |
| Menampilkan skor relevansi | Setiap *result card* menampilkan skor *Similarity* dalam bentuk angka desimal dan visual persentase (bar). | ✅ |
| Melakukan evaluasi performa | Fitur evaluasi tersedia di menu "Evaluasi" (halaman khusus `/evaluation`). | ✅ |

---

## 2. Ketentuan Evaluasi (100% TERPENUHI)
| Ketentuan PDF | Implementasi di Proyek | Status |
|---------------|------------------------|:---:|
| Menggunakan Ground Truth | Didefinisikan di `evaluation.py` (Kategori relevan untuk setiap query sudah di-mapping manual). | ✅ |
| Minimal 10 query pengujian | Ada tepat 10 query berbeda (contoh: *football world cup*, *stock market crash*, dll). | ✅ |
| Menggunakan metrik IR | Metrik yang dihitung: **Precision@5** (0.88), **Recall** (0.01), dan **MAP** (0.915). | ✅ |

---

## 3. Ketentuan Dataset & Tema (100% TERPENUHI)
| Ketentuan PDF | Implementasi di Proyek | Status |
|---------------|------------------------|:---:|
| Teks memadai (>100 kata) | Dataset BBC News berisi artikel berita teks utuh yang panjang. | ✅ |
| Relevan dengan tema proyek | Tema: "Pencarian Artikel Berita" sangat relevan dengan dataset. | ✅ |
| Diperoleh dari sumber publik | BBC News Dataset adalah dataset publik yang sangat populer di Kaggle untuk riset NLP/IR. | ✅ |

---

## 4. Ketentuan Lainnya & Output
| Ketentuan PDF | Implementasi di Proyek | Status |
|---------------|------------------------|:---:|
| Sistem Keseluruhan (Web/GUI) | Dibangun menggunakan **Flask Python** dengan tampilan HTML/CSS Bootstrap yang bersih. | ✅ |
| Mudah dipahami kelompok | Kode dipisah per modul (`preprocessing.py`, `indexing.py`, dll) dan penuh dengan komentar bahasa Indonesia. | ✅ |
| File Presentasi | Panduan alur presentasi sudah disediakan di file `README.md`. | ✅ |
| Source code di GitHub | *Anda tinggal membuat repository di GitHub dan melakukan push folder proyek ini.* | ⏳ |

---

## 🎯 Kesimpulan: **SIAP PRESENTASI!**

Proyek ini telah memenuhi dan bahkan melampaui standar minimal dari rubrik penilaian dosen (terdapat fitur ekstra seperti: Fitur *Upload ZIP otomatis*, *Highlight keyword*, dan *Search History*).

**Langkah Terakhir Anda Sebelum Presentasi:**
1. Upload folder proyek ini ke GitHub kelompok Anda.
2. Pelajari file `PANDUAN_AWAM.md` agar lancar saat menjelaskan logika pencariannya.
3. Pelajari daftar "Pertanyaan Dosen & Jawaban" di file `README.md`.
4. (Opsional) Hosting aplikasi ini ke PythonAnywhere mengikuti tutorial di `TUTORIAL_HOSTING.md` agar terlihat lebih keren saat demo.
