# PANDUAN AWAM: Sistem Pencarian Berita (News Search Engine)

Panduan ini dibuat agar sistem ini sangat mudah dipahami oleh siapa saja, bahkan oleh orang awam yang tidak mengerti programming atau matematika rumit.

---

## 1. Apa Sih Sebenarnya Sistem Ini?
Sistem ini pada dasarnya sama seperti **Google Search**, tapi dalam skala yang jauh lebih kecil dan khusus mencari **Artikel Berita (BBC News)**. 

Jika kamu mengetikkan sesuatu (contoh: *"pertandingan sepak bola piala dunia"*), sistem ini tidak akan sekadar mencocokkan kata per kata persis, tapi akan menghitung **seberapa relevan (nyambung)** suatu berita dengan apa yang kamu cari.

## 2. Bagaimana Cara Kerjanya? (Penjelasan Sangat Sederhana)

Bayangkan kamu adalah seorang penjaga perpustakaan yang punya ribuan buku, dan seseorang minta tolong dicarikan buku tentang "Sepak Bola". Proses yang dilakukan sistem mirip dengan apa yang akan kamu lakukan:

### Tahap 1: Bersih-bersih Teks (Preprocessing)
Sebelum sistem mulai mencari, sistem akan membersihkan teksnya dulu biar gak bingung.
1. **Huruf Kecil Semua (Case Folding):** Kata `Sepak`, `sePak`, dan `SEPAK` diubah jadi `sepak`. Biar komputer gak anggap itu kata yang berbeda.
2. **Potong per Kata (Tokenization):** Kalimat panjang dipotong jadi kata satuan.
3. **Buang Kata Tidak Penting (Stopword):** Kata-kata seperti `yang`, `di`, `ke`, `adalah` dibuang karena tidak ada artinya untuk pencarian.
4. **Cari Kata Dasar (Stemming):** Kata seperti `bermain` atau `dimainkan` diubah ke bentuk dasarnya yaitu `main`.

### Tahap 2: Menentukan Bobot Kata (TF-IDF)
Tidak semua kata itu sama pentingnya. Sistem menggunakan metode **TF-IDF** untuk memberi nilai (bobot) pada setiap kata:
- Jika suatu kata sering muncul di satu berita, tapi **JARANG** ada di berita-berita lain, maka kata itu **SANGAT PENTING**.
- *Contoh:* Kata "Ronaldo" mungkin muncul 10 kali di satu berita, tapi jarang di berita lain. Maka bobot kata "Ronaldo" sangat tinggi. Kalau ada user mencari kata "Ronaldo", berita ini pasti muncul paling atas.

### Tahap 3: Menghitung Kemiripan (Cosine Similarity)
Setelah query (kata kunci pencarian) dan dokumen (berita) sudah punya bobot kata, komputer mengukur kemiripannya dengan **Cosine Similarity**. 
- Anggap saja sistem mengukur "arah" dari dua buah garis. Kalau arahnya persis sama (sudutnya 0), berarti kemiripannya 100% (skor 1.0). Kalau beda jauh, kemiripannya 0%.
- Semakin tinggi skornya (semakin mendekati 1), berarti beritanya semakin cocok dengan apa yang kamu cari!

---

## 3. Penjelasan Fitur-Fitur Website

Saat kamu membuka websitenya, ini adalah fitur-fitur yang bisa langsung kamu gunakan:

1. **Kotak Pencarian (Search Bar):** Tempat kamu mengetikkan kata kunci berita yang ingin dicari (harus pakai bahasa Inggris karena beritanya bahasa Inggris, contoh: *football world cup*).
2. **Kategori Berita (Badges):** Saat hasil pencarian keluar, kamu akan melihat label warna-warni (contoh: label biru bertuliskan *sport*). Ini adalah kategori dari berita tersebut.
3. **Similarity Score (Skor Persentase):** Di setiap hasil, ada angka persentase (misal: 89%). Ini adalah hasil hitungan *Cosine Similarity*. Semakin tinggi persentasenya, sistem semakin yakin bahwa ini berita yang tepat buat kamu.
4. **Highlight Kuning:** Kata-kata di dalam preview teks berita yang cocok dengan kata kuncimu akan ditandai dengan stabilo warna kuning biar mata kita gampang mencarinya.
5. **History (Riwayat):** Kalau kamu klik menu History di atas, kamu bisa melihat kata kunci apa saja yang pernah dicari sebelumnya, lengkap dengan jam dan berapa banyak hasilnya.
6. **Evaluasi (Rapor Sistem):** Di menu Evaluasi, sistem melakukan "Ujian" pada dirinya sendiri. Sistem akan mencari 10 kata kunci yang sudah disiapkan, lalu menilai dirinya sendiri pakai nilai IPK (dalam bentuk metrik P@5 dan MAP). Semakin tinggi MAP-nya, berarti mesin pencari ini semakin pintar.

Itu saja! Intinya, ini adalah mini-Google yang menggunakan matematika pintar untuk mencocokkan kata kunci kamu dengan ribuan teks artikel secara cepat!
