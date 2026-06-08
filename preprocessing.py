# type: ignore
# pylint: skip-file
# flake8: noqa
# ============================================================
# preprocessing.py
# Modul Preprocessing Teks untuk Sistem Temu Kembali Informasi
# ============================================================
# Modul ini berisi fungsi-fungsi preprocessing teks yang
# digunakan untuk mempersiapkan dokumen dan query sebelum
# dilakukan indexing dan pencarian.
#
# Tahapan Preprocessing:
# 1. Case Folding   - mengubah teks menjadi huruf kecil
# 2. Tokenization   - memecah teks menjadi kata-kata (token)
# 3. Stopword Removal - menghapus kata-kata umum yang tidak bermakna
# 4. Stemming       - mengubah kata ke bentuk dasar (root word)
# ============================================================

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download data NLTK yang diperlukan (hanya perlu sekali)
# Dibungkus try-except agar tidak crash di server hosting yang membatasi akses internet (offline/restricted)
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except Exception as e:
    print(f"[WARNING] Gagal mengunduh NLTK resources: {e}")

# Inisialisasi stemmer dan stopwords
# PorterStemmer digunakan karena sederhana dan efektif untuk bahasa Inggris
stemmer = PorterStemmer()

# Stopwords adalah kata-kata umum seperti 'the', 'is', 'at', 'and'
# yang tidak memberikan informasi penting untuk pencarian
stop_words = set(stopwords.words('english'))


def case_folding(text):
    """
    Case Folding: Mengubah seluruh teks menjadi huruf kecil (lowercase).
    
    Tujuan:
    - Menyamakan representasi kata agar 'Football' dan 'football'
      dianggap sebagai kata yang sama.
    - Menghindari duplikasi term dalam vocabulary.
    
    Parameter:
        text (str): Teks input yang akan diproses
    
    Returns:
        str: Teks dalam huruf kecil
    
    Contoh:
        >>> case_folding("FOOTBALL World Cup")
        'football world cup'
    """
    return text.lower()


def tokenize(text):
    """
    Tokenization: Memecah teks menjadi daftar kata-kata (token).
    
    Tujuan:
    - Memisahkan teks menjadi unit-unit kata yang bisa diproses
    - Menghapus karakter non-alfanumerik (tanda baca, simbol, dll)
    - Menghasilkan daftar token yang bersih
    
    Menggunakan regex untuk mengambil hanya karakter alfanumerik.
    
    Parameter:
        text (str): Teks yang akan di-tokenize
    
    Returns:
        list: Daftar token (kata-kata)
    
    Contoh:
        >>> tokenize("football world cup 2024!")
        ['football', 'world', 'cup', '2024']
    """
    # \w+ mencocokkan satu atau lebih karakter alfanumerik
    tokens = re.findall(r'\w+', text)
    return tokens


def remove_stopwords(tokens):
    """
    Stopword Removal: Menghapus kata-kata umum yang tidak bermakna.
    
    Tujuan:
    - Mengurangi noise dalam dokumen
    - Menghapus kata-kata seperti 'the', 'is', 'and', 'in', dll
    - Meningkatkan akurasi pencarian karena hanya kata bermakna yang tersisa
    - Mengurangi ukuran vocabulary dan index
    
    Parameter:
        tokens (list): Daftar token yang akan difilter
    
    Returns:
        list: Daftar token tanpa stopwords
    
    Contoh:
        >>> remove_stopwords(['the', 'football', 'world', 'cup', 'is', 'great'])
        ['football', 'world', 'cup', 'great']
    """
    filtered = [token for token in tokens if token not in stop_words]
    return filtered


def stem(tokens):
    """
    Stemming: Mengubah kata ke bentuk dasar (root/stem).
    
    Tujuan:
    - Menyamakan variasi kata yang memiliki akar yang sama
    - Contoh: 'running', 'runs', 'ran' -> 'run'
    - Mengurangi ukuran vocabulary
    - Meningkatkan recall pencarian
    
    Menggunakan Porter Stemmer yang merupakan algoritma stemming
    paling populer untuk bahasa Inggris.
    
    Parameter:
        tokens (list): Daftar token yang akan di-stem
    
    Returns:
        list: Daftar token yang sudah di-stem
    
    Contoh:
        >>> stem(['running', 'football', 'played'])
        ['run', 'footbal', 'play']
    """
    stemmed = [stemmer.stem(token) for token in tokens]
    return stemmed


def preprocess_text(text):
    """
    Pipeline Preprocessing Lengkap.
    
    Menjalankan seluruh tahapan preprocessing secara berurutan:
    1. Case Folding   -> huruf kecil
    2. Tokenization   -> pecah jadi token
    3. Stopword Removal -> hapus kata umum
    4. Stemming       -> ubah ke bentuk dasar
    5. Join           -> gabung kembali jadi string
    
    Parameter:
        text (str): Teks mentah yang akan dipreprocess
    
    Returns:
        str: Teks yang sudah dipreprocess (string gabungan token)
    
    Contoh:
        >>> preprocess_text("The Football World Cup is Amazing!")
        'footbal world cup amaz'
    """
    # Langkah 1: Case Folding
    text = case_folding(text)
    
    # Langkah 2: Tokenization
    tokens = tokenize(text)
    
    # Langkah 3: Stopword Removal
    tokens = remove_stopwords(tokens)
    
    # Langkah 4: Stemming
    tokens = stem(tokens)
    
    # Langkah 5: Gabungkan kembali menjadi string
    # (diperlukan untuk input TfidfVectorizer)
    result = ' '.join(tokens)
    
    return result


def generate_extractive_title(text):
    """
    Ekstraksi Kalimat Utama: Memilih kalimat paling representatif 
    sebagai judul menggunakan frekuensi kata (extractive summary).
    """
    from nltk.tokenize import sent_tokenize
    import string
    
    # Pisahkan teks menjadi kalimat
    try:
        sentences = sent_tokenize(text)
    except Exception:
        # Fallback jika punk_tab tidak tersedia
        sentences = text.split('.')
        sentences = [s.strip() + '.' for s in sentences if s.strip()]

    if not sentences:
        return "Untitled Document"

    # Hitung frekuensi kata
    word_freq = {}
    tokens = tokenize(case_folding(text))
    tokens = remove_stopwords(tokens)
    
    for word in tokens:
        if word not in word_freq:
            word_freq[word] = 1
        else:
            word_freq[word] += 1

    # Normalisasi frekuensi (opsional tapi disarankan)
    max_freq = max(word_freq.values()) if word_freq else 1
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    # Skor setiap kalimat
    sentence_scores = {}
    for sentence in sentences:
        # Hanya pertimbangkan kalimat dengan panjang wajar
        word_count = len(sentence.split(' '))
        if word_count < 5 or word_count > 30:
            continue
            
        sentence_tokens = tokenize(case_folding(sentence))
        score = 0
        for word in sentence_tokens:
            if word in word_freq:
                score += word_freq[word]
        
        # Bagi dengan jumlah kata agar kalimat panjang tidak selalu menang
        if word_count > 0:
            sentence_scores[sentence] = score / word_count

    # Pilih kalimat dengan skor tertinggi
    if not sentence_scores:
        # Fallback: jika tidak ada yang masuk kriteria, ambil kalimat pertama yang cukup panjang
        for sentence in sentences:
            if len(sentence.split()) >= 3:
                best_sentence = sentence
                break
        else:
            best_sentence = sentences[0]
    else:
        best_sentence = max(sentence_scores, key=sentence_scores.get)

    # Bersihkan kalimat untuk judul
    title = best_sentence.strip()
    
    # Hapus karakter aneh di awal atau akhir
    title = title.lstrip(string.punctuation + " ")
    
    # Batasi panjang judul agar rapi (max ~100 karakter)
    if len(title) > 100:
        # Coba potong di spasi terdekat sebelum 100 karakter
        title = title[:97]
        last_space = title.rfind(' ')
        if last_space > 50:
            title = title[:last_space]
        title = title + "..."
        
    # Pastikan diawali huruf kapital
    if title:
        title = title[0].upper() + title[1:]
        
    return title


# ============================================================
# Jika file ini dijalankan langsung, tampilkan contoh penggunaan
# ============================================================
if __name__ == '__main__':
    # Contoh teks artikel berita
    sample_text = "The Football World Cup 2024 is being held in various countries. Many teams are competing for the championship title."
    
    print("=" * 60)
    print("DEMO PREPROCESSING TEKS")
    print("=" * 60)
    
    print(f"\nTeks Asli:\n{sample_text}")
    
    # Tunjukkan setiap langkah
    step1 = case_folding(sample_text)
    print(f"\n1. Case Folding:\n{step1}")
    
    step2 = tokenize(step1)
    print(f"\n2. Tokenization:\n{step2}")
    
    step3 = remove_stopwords(step2)
    print(f"\n3. Stopword Removal:\n{step3}")
    
    step4 = stem(step3)
    print(f"\n4. Stemming:\n{step4}")
    
    # Hasil akhir pipeline lengkap
    result = preprocess_text(sample_text)
    print(f"\n5. Hasil Akhir (preprocess_text):\n{result}")
    print("=" * 60)
