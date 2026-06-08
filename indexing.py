# ============================================================
# indexing.py
# Modul Indexing Dokumen untuk Sistem Temu Kembali Informasi
# ============================================================
# Modul ini berisi fungsi-fungsi untuk membangun index dokumen
# menggunakan TF-IDF (Term Frequency - Inverse Document Frequency).
#
# Konsep TF-IDF:
# - TF (Term Frequency): Seberapa sering suatu kata muncul dalam
#   satu dokumen. Semakin sering = semakin penting untuk dokumen itu.
#
# - IDF (Inverse Document Frequency): Seberapa jarang suatu kata
#   muncul di seluruh koleksi dokumen. Kata yang jarang = lebih unik
#   dan lebih penting.
#
# - TF-IDF = TF × IDF
#   Memberikan bobot tinggi pada kata yang sering muncul di satu
#   dokumen tapi jarang di dokumen lain.
#
# Proses Indexing:
# 1. Preprocessing seluruh dokumen
# 2. Membangun vocabulary (kumpulan semua kata unik)
# 3. Menghitung TF-IDF matrix (dokumen × term)
# 4. Menyimpan model ke file pickle
# ============================================================

import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing import preprocess_text


def build_tfidf_index(documents):
    """
    Membangun TF-IDF Index dari kumpulan dokumen.
    
    Proses:
    1. Menerima list dokumen (sudah dipreprocess)
    2. Membuat TfidfVectorizer (alat untuk menghitung TF-IDF)
    3. Fit & Transform dokumen menjadi TF-IDF matrix
    
    TF-IDF Matrix:
    - Baris = dokumen
    - Kolom = term (kata unik)
    - Nilai = bobot TF-IDF
    
    Parameter:
        documents (list): Daftar teks dokumen yang sudah dipreprocess
    
    Returns:
        tuple: (vectorizer, tfidf_matrix)
            - vectorizer: objek TfidfVectorizer (untuk transform query)
            - tfidf_matrix: sparse matrix TF-IDF
    
    Contoh:
        >>> docs = ["football world cup", "stock market economy"]
        >>> vectorizer, matrix = build_tfidf_index(docs)
        >>> print(matrix.shape)  # (2, jumlah_kata_unik)
    """
    # Inisialisasi TfidfVectorizer
    # - max_features: batasi jumlah kata unik (opsional, untuk efisiensi)
    # - ngram_range: gunakan unigram (kata tunggal)
    vectorizer = TfidfVectorizer(
        max_features=10000,    # Maksimal 10.000 kata unik
        ngram_range=(1, 1),    # Hanya unigram (kata tunggal)
        norm='l2'              # Normalisasi L2 (untuk cosine similarity)
    )
    
    # Fit dan Transform: pelajari vocabulary + hitung TF-IDF
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Informasi index yang dibangun
    print(f"[INDEXING] Jumlah dokumen  : {tfidf_matrix.shape[0]}")
    print(f"[INDEXING] Jumlah vocabulary: {tfidf_matrix.shape[1]}")
    print(f"[INDEXING] Ukuran matrix   : {tfidf_matrix.shape}")
    
    return vectorizer, tfidf_matrix


def save_model(vectorizer, tfidf_matrix, model_dir='models'):
    """
    Menyimpan model TF-IDF ke file pickle.
    
    Tujuan:
    - Agar tidak perlu membangun ulang index setiap kali server dijalankan
    - Menghemat waktu startup aplikasi
    - Model disimpan sebagai file binary (.pkl)
    
    File yang disimpan:
    - tfidf_vectorizer.pkl: objek TfidfVectorizer
    - tfidf_matrix.pkl: TF-IDF matrix (sparse matrix)
    
    Parameter:
        vectorizer: objek TfidfVectorizer
        tfidf_matrix: sparse matrix TF-IDF
        model_dir (str): direktori penyimpanan model
    """
    # Buat folder models jika belum ada
    os.makedirs(model_dir, exist_ok=True)
    
    # Simpan vectorizer
    vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"[SAVE] Vectorizer disimpan ke: {vectorizer_path}")
    
    # Simpan TF-IDF matrix
    matrix_path = os.path.join(model_dir, 'tfidf_matrix.pkl')
    with open(matrix_path, 'wb') as f:
        pickle.dump(tfidf_matrix, f)
    print(f"[SAVE] TF-IDF Matrix disimpan ke: {matrix_path}")


def load_model(model_dir='models'):
    """
    Memuat model TF-IDF dari file pickle.
    
    Membaca kembali vectorizer dan TF-IDF matrix yang sudah
    disimpan sebelumnya agar tidak perlu rebuilding.
    
    Parameter:
        model_dir (str): direktori tempat model disimpan
    
    Returns:
        tuple: (vectorizer, tfidf_matrix) atau (None, None) jika file tidak ada
    """
    vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
    matrix_path = os.path.join(model_dir, 'tfidf_matrix.pkl')
    
    # Cek apakah file model ada
    if not os.path.exists(vectorizer_path) or not os.path.exists(matrix_path):
        print("[LOAD] File model tidak ditemukan. Perlu build ulang.")
        return None, None
    
    # Load vectorizer
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    print(f"[LOAD] Vectorizer dimuat dari: {vectorizer_path}")
    
    # Load TF-IDF matrix
    with open(matrix_path, 'rb') as f:
        tfidf_matrix = pickle.load(f)
    print(f"[LOAD] TF-IDF Matrix dimuat dari: {matrix_path}")
    print(f"[LOAD] Ukuran matrix: {tfidf_matrix.shape}")
    
    return vectorizer, tfidf_matrix


def get_vocabulary_info(vectorizer):
    """
    Mendapatkan informasi tentang vocabulary yang dibangun.
    
    Berguna untuk menampilkan statistik index di website.
    
    Parameter:
        vectorizer: objek TfidfVectorizer
    
    Returns:
        dict: informasi vocabulary
    """
    vocab = vectorizer.vocabulary_
    return {
        'total_terms': len(vocab),
        'sample_terms': list(vocab.keys())[:20],  # 20 contoh kata
    }


# ============================================================
# Jika file ini dijalankan langsung, tampilkan contoh penggunaan
# ============================================================
if __name__ == '__main__':
    # Contoh dokumen sederhana
    sample_docs = [
        "football world cup championship england team",
        "stock market economy financial crisis bank",
        "technology smartphone apple samsung release",
        "government election politics prime minister",
        "movie film awards oscar ceremony hollywood"
    ]
    
    print("=" * 60)
    print("DEMO INDEXING TF-IDF")
    print("=" * 60)
    
    # Preprocess dokumen
    print("\nPreprocessing dokumen...")
    preprocessed = [preprocess_text(doc) for doc in sample_docs]
    for i, doc in enumerate(preprocessed):
        print(f"  Doc {i+1}: {doc}")
    
    # Build index
    print("\nMembangun TF-IDF index...")
    vectorizer, matrix = build_tfidf_index(preprocessed)
    
    # Tampilkan informasi
    vocab_info = get_vocabulary_info(vectorizer)
    print(f"\nTotal kata unik: {vocab_info['total_terms']}")
    print(f"Contoh kata: {vocab_info['sample_terms']}")
    
    # Save model
    print("\nMenyimpan model...")
    save_model(vectorizer, matrix)
    
    # Load model
    print("\nMemuat model...")
    v2, m2 = load_model()
    print(f"Matrix shape setelah load: {m2.shape}")
    
    print("\n" + "=" * 60)
