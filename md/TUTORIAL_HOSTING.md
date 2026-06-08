# Panduan Hosting Gratis Flask App untuk Proyek STKI

Karena proyek ini menggunakan Python (Flask) dan perlu menyimpan file model (`.pkl`) serta dataset secara permanen, tidak semua layanan hosting gratis cocok. Beberapa layanan seperti Heroku (sudah tidak gratis) atau Render (file akan hilang saat server *sleep*) kurang disarankan.

Pilihan **TERBAIK, GRATIS, dan PALING MUDAH** untuk proyek mahasiswa adalah **PythonAnywhere**.

Keunggulan PythonAnywhere:
- 100% Gratis selamanya (untuk 1 website).
- Penyimpanan persisten (file dataset dan model tidak akan terhapus).
- Tidak perlu kartu kredit.
- Domain gratis: `nama-kamu.pythonanywhere.com`.

Berikut adalah tutorial langkah demi langkah cara meng-hosting web STKI ini ke PythonAnywhere.

---

## TAHAP 1: Persiapan File
1. Buka folder proyek `TKI` di komputermu.
2. Hapus folder `dataset`, `models`, dan `history` (kita akan meng-upload versi bersihnya agar ringan, nanti dataset di-upload ulang dari website).
3. Block semua file yang tersisa (`app.py`, `preprocessing.py`, `indexing.py`, `search.py`, `evaluation.py`, `requirements.txt`, folder `templates`, folder `static`).
4. **Jadikan satu file ZIP** (misal: `stki_project.zip`).

---

## TAHAP 2: Buat Akun & Upload
1. Buka website [PythonAnywhere.com](https://www.pythonanywhere.com/) dan buat akun (Pilih **Create a Beginner account** yang gratis).
2. Setelah login, kamu akan masuk ke halaman *Dashboard*.
3. Klik tab **Files** di menu atas.
4. Di bagian *Directories*, ketik `stki_app` lalu klik tombol **New directory**.
5. Masuk ke dalam folder `stki_app` yang baru dibuat.
6. Klik tombol **Upload a file** warna kuning, lalu pilih file `stki_project.zip` yang kamu buat di Tahap 1.

---

## TAHAP 3: Ekstrak File & Install Library
1. Buka menu **Consoles** (di pojok kanan atas), lalu klik **Bash**.
2. Akan terbuka layar terminal hitam. Ketikkan perintah berikut satu per satu (tekan Enter setiap baris):
   ```bash
   cd stki_app
   unzip stki_project.zip
   rm stki_project.zip
   ```
3. Sekarang kita install library Python yang dibutuhkan. Ketik:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
   *(Tunggu proses install sampai selesai. Butuh waktu sekitar 1-2 menit).*
4. Terakhir, kita download data NLTK secara manual di konsol. Ketik perintah ini:
   ```bash
   python3.10 -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
   ```

---

## TAHAP 4: Setup Website (Web Tab)
1. Keluar dari layar hitam (klik logo PythonAnywhere di pojok kiri atas).
2. Pergi ke tab **Web**.
3. Klik tombol **Add a new web app**.
4. Klik **Next**.
5. Pilih **Flask**, lalu pilih versi **Python 3.10** (atau yang terbaru yang tersedia).
6. Di bagian *Path*, ubah tulisannya menjadi:
   `/home/NAMA_USERNAME_KAMU/stki_app/app.py` 
   *(Ganti NAMA_USERNAME_KAMU dengan username akun PythonAnywhere kamu!)*
7. Klik **Next**, dan website akan dibuat.

---

## TAHAP 5: Konfigurasi WSGI File
Masih di halaman Web tab:
1. Scroll ke bawah sampai menemukan bagian **Code**.
2. Klik link file yang ada di kolom **WSGI configuration file** (biasanya bernama `/var/www/username_pythonanywhere_com_wsgi.py`).
3. Akan terbuka halaman editor kode. **Hapus semua isinya**, lalu ganti dengan kode berikut:

```python
import sys
import os

# 1. Tentukan lokasi folder proyekmu
path = '/home/NAMA_USERNAME_KAMU/stki_app'
if path not in sys.path:
    sys.path.insert(0, path)

# 2. Ubah working directory
os.chdir(path)

# 3. Import aplikasi Flask-mu
from app import app as application
```
*(Ingat: Ganti `NAMA_USERNAME_KAMU` dengan username aslimu).*
4. Klik tombol hijau **Save** di pojok kanan atas.

---

## TAHAP 6: Launching!
1. Kembali ke tab **Web**.
2. Klik tombol hijau besar bertuliskan **Reload NAMA_USERNAME_KAMU.pythonanywhere.com**.
3. Selesai! Sekarang klik link domain kamu (ada di bagian paling atas halaman).

Website kamu sudah online dan bisa diakses dari mana saja.

**Langkah Terakhir:**
Saat website sudah terbuka di HP atau laptop temanmu, buka websitenya, lalu **Upload file ZIP dataset BBC News (`archive (7).zip`)** melalui tampilan website tersebut seperti biasa. Sistem akan memprosesnya, dan setelah selesai, website pencarian beritamu siap didemokan ke dosen!
