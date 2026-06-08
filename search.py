# ============================================================
# search.py
# Modul Pencarian untuk Sistem Temu Kembali Informasi
# ============================================================
# Modul ini berisi fungsi-fungsi untuk melakukan pencarian
# dokumen berdasarkan query pengguna.
#
# Konsep Pencarian (Retrieval):
# 1. Query pengguna dipreprocess (sama seperti dokumen)
# 2. Query ditransformasi menjadi vektor TF-IDF
# 3. Cosine Similarity dihitung antara query dan semua dokumen
# 4. Dokumen diurutkan berdasarkan similarity score (ranking)
# 5. Top-K dokumen paling relevan dikembalikan
#
# Cosine Similarity:
# - Mengukur kesamaan arah antara dua vektor
# - Nilai antara 0 (tidak mirip) sampai 1 (sangat mirip)
# - Rumus: cos(θ) = (A · B) / (||A|| × ||B||)
# - Dipilih karena tidak terpengaruh panjang dokumen
# ============================================================

import os
import re
import json
import time
import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import preprocess_text


def search_query(query, vectorizer, tfidf_matrix, df, top_k=5):
    """
    Melakukan pencarian dokumen berdasarkan query pengguna.
    
    Proses pencarian:
    1. Preprocess query (sama seperti preprocessing dokumen)
    2. Transform query menjadi vektor TF-IDF menggunakan vectorizer
    3. Hitung cosine similarity antara query dan semua dokumen
    4. Urutkan dokumen berdasarkan similarity score (descending)
    5. Ambil top-K dokumen paling relevan
    
    Parameter:
        query (str): Query pencarian dari pengguna
        vectorizer: objek TfidfVectorizer (sudah di-fit)
        tfidf_matrix: TF-IDF matrix dokumen (sparse matrix)
        df: DataFrame berisi data dokumen (category, title, content)
        top_k (int): Jumlah hasil teratas yang dikembalikan (default: 5)
    
    Returns:
        dict: Hasil pencarian berisi:
            - query: query asli
            - preprocessed_query: query setelah preprocessing
            - results: list of dict (ranking, category, title, content, score)
            - search_time: waktu pencarian dalam detik
            - total_documents: total dokumen yang dicari
    """
    # Catat waktu mulai pencarian
    start_time = time.time()
    
    # LANGKAH 1: Preprocessing query
    # Query harus dipreprocess dengan cara yang SAMA seperti dokumen
    # agar representasi vektornya konsisten
    preprocessed_query = preprocess_text(query)
    
    # LANGKAH 2: Transform query menjadi vektor TF-IDF
    # Menggunakan vectorizer yang SAMA (sudah di-fit dengan dokumen)
    # transform() hanya mengubah query ke vektor, tanpa mengubah vocabulary
    query_vector = vectorizer.transform([preprocessed_query])
    
    # LANGKAH 3: Hitung Cosine Similarity
    # Membandingkan vektor query dengan SEMUA vektor dokumen
    # Hasilnya: array 1D berisi similarity score untuk setiap dokumen
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # LANGKAH 4: Ranking - urutkan berdasarkan score tertinggi
    # argsort() mengurutkan index dari kecil ke besar
    # [::-1] membalik urutan menjadi besar ke kecil
    ranked_indices = similarity_scores.argsort()[::-1]
    
    # LANGKAH 5: Ambil top-K hasil
    top_indices = ranked_indices[:top_k]
    
    # Hitung waktu pencarian
    search_time = time.time() - start_time
    
    # Susun hasil pencarian
    results = []
    for rank, idx in enumerate(top_indices, 1):
        score = similarity_scores[idx]
        
        # Hanya tampilkan dokumen dengan score > 0
        # (dokumen yang memiliki kesamaan dengan query)
        if score > 0:
            content_text = df.iloc[idx]['content']
            # Preview: ambil 300 karakter pertama, tambah '...' jika terpotong
            if len(content_text) > 300:
                preview_text = content_text[:300] + '...'
            else:
                preview_text = content_text
            
            results.append({
                'rank': rank,
                'category': df.iloc[idx]['category'],
                'title': df.iloc[idx]['title'],
                'content': content_text,
                'preview': preview_text,
                'score': round(float(score), 4),
                'doc_index': int(idx)
            })
    
    return {
        'query': query,
        'preprocessed_query': preprocessed_query,
        'results': results,
        'search_time': round(search_time, 4),
        'total_documents': len(df)
    }


def save_search_history(query, results_count, search_time, history_dir='history'):
    """
    Menyimpan riwayat pencarian ke file JSON.
    
    Setiap pencarian yang dilakukan pengguna akan dicatat
    untuk ditampilkan di halaman Search History.
    
    Parameter:
        query (str): Query yang dicari
        results_count (int): Jumlah hasil yang ditemukan
        search_time (float): Waktu pencarian (detik)
        history_dir (str): Direktori penyimpanan history
    """
    # Buat folder history jika belum ada
    os.makedirs(history_dir, exist_ok=True)
    
    history_file = os.path.join(history_dir, 'search_history.json')
    
    # Load history yang sudah ada
    history = load_search_history(history_dir)
    
    # Server PythonAnywhere menggunakan waktu UTC, jadi kita konversi ke WIB (+7 jam)
    wib_time = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    
    # Tambahkan entry baru
    entry = {
        'query': query,
        'results_count': results_count,
        'search_time': search_time,
        'timestamp': wib_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    history.append(entry)
    
    # Simpan kembali ke file JSON
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def load_search_history(history_dir='history'):
    """
    Memuat riwayat pencarian dari file JSON.
    
    Parameter:
        history_dir (str): Direktori penyimpanan history
    
    Returns:
        list: Daftar riwayat pencarian
    """
    history_file = os.path.join(history_dir, 'search_history.json')
    
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return []


def highlight_keywords(text, query):
    """
    Menandai kata kunci query dalam teks hasil pencarian.
    
    Berguna untuk menunjukkan kepada pengguna mengapa suatu
    dokumen dianggap relevan.
    
    Parameter:
        text (str): Teks dokumen
        query (str): Query pencarian
    
    Returns:
        str: Teks dengan kata kunci yang di-highlight menggunakan tag <mark>
    """
    # Ambil kata-kata dari query (sebelum preprocessing)
    keywords = query.lower().split()
    
    highlighted = text
    for keyword in keywords:
        if len(keyword) < 2:  # Skip kata terlalu pendek
            continue
        # \b = word boundary agar hanya kata utuh yang di-highlight
        try:
            pattern = re.compile(r'\b(' + re.escape(keyword) + r')\b', re.IGNORECASE)
            highlighted = pattern.sub(r'<mark>\1</mark>', highlighted)
        except re.error:
            continue
    
    return highlighted


# ============================================================
# Jika file ini dijalankan langsung, tampilkan contoh penggunaan
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("DEMO SEARCH ENGINE")
    print("=" * 60)
    print("\nModul ini memerlukan vectorizer dan matrix dari indexing.py")
    print("Jalankan app.py untuk menggunakan fitur pencarian lengkap.")
    print("=" * 60)
