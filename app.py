# ============================================================
# app.py
# Aplikasi Utama Flask - Sistem Temu Kembali Informasi
# ============================================================
# File ini adalah entry point aplikasi web.
# Menghubungkan semua modul (preprocessing, indexing, search,
# evaluation) dan menyediakan antarmuka web melalui Flask.
#
# Routes:
# /           - Halaman utama (search + results)
# /search     - Proses pencarian (POST)
# /history    - Riwayat pencarian
# /evaluation - Evaluasi sistem IR
# /article    - Detail artikel
# /upload     - Upload dataset ZIP
# ============================================================

import os
import zipfile
import pandas as pd
import time
import urllib.parse
import urllib.request
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for


# Import modul-modul STKI yang sudah dibuat
from preprocessing import preprocess_text, generate_extractive_title
from indexing import build_tfidf_index, save_model, load_model
from search import search_query, save_search_history, load_search_history, highlight_keywords
from evaluation import run_evaluation, GROUND_TRUTH

# ============================================================
# INISIALISASI FLASK APP
# ============================================================
app = Flask(__name__)

# Konfigurasi folder upload
UPLOAD_FOLDER = 'dataset'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # Max 200MB

# ============================================================
# VARIABEL GLOBAL
# ============================================================
# Variabel global untuk menyimpan data yang sudah diproses
# agar tidak perlu memproses ulang setiap kali ada request
df = None                   # DataFrame berisi data artikel
vectorizer = None           # TfidfVectorizer (sudah di-fit)
tfidf_matrix = None         # TF-IDF matrix (sparse matrix)
dataset_loaded = False      # Status apakah dataset sudah dimuat
category_stats = {}         # Statistik jumlah per kategori


# ============================================================
# FUNGSI MEMBACA DATASET
# ============================================================

def read_dataset_from_folder(base_path):
    """
    Membaca seluruh file .txt dari folder dataset BBC News.
    
    Struktur folder yang diharapkan:
    base_path/
    ├── business/
    │   ├── 001.txt
    │   ├── 002.txt
    │   └── ...
    ├── entertainment/
    ├── politics/
    ├── sport/
    └── tech/
    
    Parameter:
        base_path (str): Path ke folder News Articles
    
    Returns:
        pd.DataFrame: DataFrame berisi kolom [category, title, content]
    """
    data = []
    
    # Iterasi setiap folder kategori
    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)
        
        # Pastikan ini adalah folder (bukan file)
        if not os.path.isdir(category_path):
            continue
        
        # Iterasi setiap file .txt dalam folder kategori
        for filename in os.listdir(category_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(category_path, filename)
                
                try:
                    # Baca isi file dengan encoding latin-1
                    # (beberapa file BBC News menggunakan encoding ini)
                    with open(filepath, 'r', encoding='latin-1', errors='ignore') as f:
                        content = f.read().strip()
                    
                    if content:  # Hanya tambahkan jika tidak kosong
                        # Ambil kalimat utama sebagai title (extractive summary)
                        title = generate_extractive_title(content)
                        
                        data.append({
                            'category': category,
                            'title': title,
                            'content': content
                        })
                except Exception as e:
                    print(f"[WARNING] Gagal membaca {filepath}: {e}")
                    continue
    
    # Buat DataFrame
    dataframe = pd.DataFrame(data)
    print(f"[DATASET] Total dokumen dibaca: {len(dataframe)}")
    print(f"[DATASET] Kategori: {dataframe['category'].unique().tolist()}")
    print(f"[DATASET] Distribusi:")
    print(dataframe['category'].value_counts().to_string())
    
    return dataframe


def extract_zip_dataset(zip_path, extract_to='dataset'):
    """
    Extract file ZIP dataset.
    
    Parameter:
        zip_path (str): Path ke file ZIP
        extract_to (str): Folder tujuan extract
    
    Returns:
        str: Path ke folder News Articles
    """
    os.makedirs(extract_to, exist_ok=True)
    
    print(f"[ZIP] Extracting {zip_path} ke {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"[ZIP] Selesai extract.")
    
    # Cari folder News Articles
    # Struktur dalam ZIP bisa berbeda, cari secara rekursif
    for root, dirs, files in os.walk(extract_to):
        if 'News Articles' in dirs:
            return os.path.join(root, 'News Articles')
        # Cek juga apakah folder kategori langsung ada
        expected_cats = {'business', 'entertainment', 'politics', 'sport', 'tech'}
        if expected_cats.issubset(set(dirs)):
            return root
    
    # Fallback: cari folder yang punya subfolder kategori
    for root, dirs, files in os.walk(extract_to):
        if any(d in ['business', 'sport', 'tech', 'politics', 'entertainment'] for d in dirs):
            return root
    
    return extract_to


def initialize_system(articles_path):
    """
    Inisialisasi seluruh sistem IR.
    
    Proses:
    1. Membaca dataset dari folder
    2. Preprocessing semua dokumen
    3. Membangun TF-IDF index
    4. Menyimpan model ke pickle
    
    Parameter:
        articles_path (str): Path ke folder News Articles
    """
    global df, vectorizer, tfidf_matrix, dataset_loaded, category_stats
    
    print("\n" + "=" * 60)
    print("INISIALISASI SISTEM TEMU KEMBALI INFORMASI")
    print("=" * 60)
    
    # LANGKAH 1: Baca dataset
    print("\n[1/4] Membaca dataset...")
    df = read_dataset_from_folder(articles_path)
    
    if len(df) == 0:
        print("[ERROR] Tidak ada dokumen yang dibaca!")
        return False
    
    # Statistik kategori
    category_stats = df['category'].value_counts().to_dict()
    
    # LANGKAH 2: Preprocessing semua dokumen
    print("\n[2/4] Preprocessing dokumen...")
    start_time = time.time()
    df['preprocessed'] = df['content'].apply(preprocess_text)
    prep_time = time.time() - start_time
    print(f"       Selesai dalam {prep_time:.2f} detik")
    
    # LANGKAH 3: Membangun TF-IDF index
    print("\n[3/4] Membangun TF-IDF index...")
    vectorizer, tfidf_matrix = build_tfidf_index(df['preprocessed'].tolist())
    
    # LANGKAH 4: Simpan model
    print("\n[4/4] Menyimpan model...")
    save_model(vectorizer, tfidf_matrix)
    
    # Simpan juga DataFrame
    df.to_pickle('models/dataframe.pkl')
    print("[SAVE] DataFrame disimpan ke: models/dataframe.pkl")
    
    dataset_loaded = True
    
    print("\n" + "=" * 60)
    print("SISTEM SIAP DIGUNAKAN!")
    print(f"Total dokumen: {len(df)}")
    print(f"Vocabulary size: {tfidf_matrix.shape[1]}")
    print("=" * 60 + "\n")
    
    return True


def try_load_existing_model():
    """
    Mencoba memuat model yang sudah ada dari file pickle.
    
    Jika model sudah pernah disimpan, load langsung agar
    tidak perlu memproses ulang dataset.
    
    Returns:
        bool: True jika berhasil load, False jika tidak
    """
    global df, vectorizer, tfidf_matrix, dataset_loaded, category_stats
    
    # Cek apakah file model ada
    if not os.path.exists('models/tfidf_vectorizer.pkl') or \
       not os.path.exists('models/tfidf_matrix.pkl') or \
       not os.path.exists('models/dataframe.pkl'):
        return False
    
    try:
        # Load model
        vectorizer, tfidf_matrix = load_model()
        
        # Load DataFrame
        df = pd.read_pickle('models/dataframe.pkl')
        category_stats = df['category'].value_counts().to_dict()
        
        dataset_loaded = True
        print(f"[STARTUP] Model berhasil dimuat! ({len(df)} dokumen)")
        return True
    except Exception as e:
        print(f"[STARTUP] Gagal memuat model: {e}")
        return False


# Coba muat model secara otomatis saat startup server (sangat penting untuk WSGI/hosting)
try_load_existing_model()


# ============================================================
# ROUTES FLASK
# ============================================================

@app.route('/')
def index():
    """
    Halaman utama - menampilkan search bar dan statistik.
    """
    return render_template(
        'index.html',
        dataset_loaded=dataset_loaded,
        category_stats=category_stats,
        total_documents=len(df) if df is not None else 0
    )


@app.route('/upload', methods=['POST'])
def upload_dataset():
    """
    Route untuk upload file ZIP dataset.
    
    Proses:
    1. Menerima file ZIP dari form upload
    2. Simpan file ZIP ke folder dataset
    3. Extract ZIP
    4. Baca seluruh file .txt
    5. Build TF-IDF index
    """
    if 'dataset_zip' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diupload'}), 400
    
    file = request.files['dataset_zip']
    
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
    
    if not file.filename.endswith('.zip'):
        return jsonify({'error': 'File harus berformat .zip'}), 400
    
    try:
        # Simpan file ZIP
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(zip_path)
        print(f"[UPLOAD] File disimpan ke: {zip_path}")
        
        # Extract ZIP
        articles_path = extract_zip_dataset(zip_path)
        print(f"[UPLOAD] News Articles path: {articles_path}")
        
        # Inisialisasi sistem
        success = initialize_system(articles_path)
        
        if success:
            return redirect(url_for('index'))
        else:
            return jsonify({'error': 'Gagal memproses dataset'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/search', methods=['POST'])
def search():
    """
    Route untuk melakukan pencarian.
    
    Proses:
    1. Ambil query dari form
    2. Lakukan pencarian menggunakan search_query()
    3. Simpan ke search history
    4. Tampilkan hasil
    """
    if not dataset_loaded:
        return redirect(url_for('index'))
    
    query = request.form.get('query', '').strip()
    
    if not query:
        return redirect(url_for('index'))
    
    # Lakukan pencarian
    result = search_query(query, vectorizer, tfidf_matrix, df, top_k=5)
    
    # Highlight keywords di preview
    for r in result['results']:
        r['preview_highlighted'] = highlight_keywords(r['preview'], query)
    
    # Simpan ke history
    save_search_history(
        query=query,
        results_count=len(result['results']),
        search_time=result['search_time']
    )
    
    return render_template(
        'index.html',
        dataset_loaded=dataset_loaded,
        category_stats=category_stats,
        total_documents=len(df),
        search_result=result,
        query=query
    )


@app.route('/history')
def history():
    """
    Route untuk menampilkan riwayat pencarian.
    """
    search_history = load_search_history()
    # Balik urutan agar yang terbaru di atas
    search_history.reverse()
    
    return render_template(
        'index.html',
        dataset_loaded=dataset_loaded,
        category_stats=category_stats,
        total_documents=len(df) if df is not None else 0,
        search_history=search_history,
        show_history=True
    )


@app.route('/evaluation')
def evaluation():
    """
    Route untuk menjalankan dan menampilkan evaluasi sistem IR.
    """
    if not dataset_loaded:
        return redirect(url_for('index'))
    
    # Jalankan evaluasi
    eval_results = run_evaluation(search_query, vectorizer, tfidf_matrix, df)
    
    return render_template(
        'index.html',
        dataset_loaded=dataset_loaded,
        category_stats=category_stats,
        total_documents=len(df),
        eval_results=eval_results,
        show_evaluation=True
    )


@app.route('/article/<int:doc_index>')
def article_detail(doc_index):
    """
    Route untuk menampilkan detail artikel lengkap.
    """
    if not dataset_loaded or doc_index >= len(df):
        return redirect(url_for('index'))
    
    article = {
        'category': df.iloc[doc_index]['category'],
        'title': df.iloc[doc_index]['title'],
        'content': df.iloc[doc_index]['content'],
        'index': doc_index
    }
    
    return render_template(
        'index.html',
        dataset_loaded=dataset_loaded,
        category_stats=category_stats,
        total_documents=len(df),
        article=article,
        show_article=True
    )


# Cache untuk menyimpan hasil terjemahan agar tidak membebani API Google Translate
translation_cache = {}

def translate_text_post(text, sl='en', tl='id'):
    """
    Menerjemahkan teks menggunakan API bebas Google Translate melalui request POST
    untuk menghindari batasan panjang URL (HTTP 414).
    """
    if not text:
        return ""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={sl}&tl={tl}&dt=t"
        data = urllib.parse.urlencode({'q': text}).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            translated_sentences = []
            for item in result[0]:
                if item[0]:
                    translated_sentences.append(item[0])
            return "".join(translated_sentences)
    except Exception as e:
        print(f"[TRANSLATION_API_ERROR] Gagal menerjemahkan teks: {e}")
        return text  # Fallback ke teks asli jika gagal


@app.route('/translate/<int:doc_index>')
def translate_article(doc_index):
    """
    API Route untuk menerjemahkan judul dan konten artikel berdasarkan indeks dokumen.
    Menerima parameter query 'lang' (contoh: /translate/123?lang=id).
    """
    if not dataset_loaded or df is None or doc_index >= len(df):
        return jsonify({'error': 'Artikel tidak ditemukan atau sistem belum dimuat'}), 404
        
    target_lang = request.args.get('lang', 'id').lower()
    
    # Jika meminta bahasa Inggris (asli), langsung kembalikan data dari DataFrame
    if target_lang == 'en':
        return jsonify({
            'title': df.iloc[doc_index]['title'],
            'content': df.iloc[doc_index]['content']
        })
        
    # Cek cache terlebih dahulu
    cache_key = (doc_index, target_lang)
    if cache_key in translation_cache:
        print(f"[CACHE_HIT] Menyajikan terjemahan dari cache untuk indeks {doc_index}")
        return jsonify(translation_cache[cache_key])
        
    # Ambil teks asli
    original_title = df.iloc[doc_index]['title']
    original_content = df.iloc[doc_index]['content']
    
    print(f"[API_TRANSLATE] Menerjemahkan artikel indeks {doc_index} ke '{target_lang}'...")
    translated_title = translate_text_post(original_title, sl='en', tl=target_lang)
    translated_content = translate_text_post(original_content, sl='en', tl=target_lang)
    
    response_data = {
        'title': translated_title,
        'content': translated_content
    }
    
    # Simpan ke cache jika terjemahan berhasil
    if translated_title != original_title or translated_content != original_content:
        translation_cache[cache_key] = response_data
        
    return jsonify(response_data)



# ============================================================
# MAIN - Jalankan Aplikasi
# ============================================================
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  THE BBC CHRONICLE")
    print("  Sistem Temu Kembali Informasi Artikel Berita")
    print("  UAS Mata Kuliah STKI - COM620321")
    print("=" * 60)
    
    # Coba load model yang sudah ada
    print("\n[STARTUP] Memeriksa model yang tersimpan...")
    if try_load_existing_model():
        print("[STARTUP] Model ditemukan dan dimuat!")
    else:
        print("[STARTUP] Model belum ada.")
        
        # Cek apakah ada folder dataset yang sudah di-extract
        possible_paths = [
            os.path.join('dataset', 'News Articles'),
            os.path.join('dataset', 'BBC News Summary', 'News Articles'),
            os.path.join('dataset', 'bbc', 'News Articles'),
        ]
        
        found = False
        for path in possible_paths:
            if os.path.exists(path) and os.path.isdir(path):
                subdirs = os.listdir(path)
                if any(d in subdirs for d in ['business', 'sport', 'tech']):
                    print(f"[STARTUP] Dataset ditemukan di: {path}")
                    initialize_system(path)
                    found = True
                    break
        
        if not found:
            print("[STARTUP] Dataset belum ada. Upload melalui web interface.")
    
    print("\n[SERVER] Menjalankan Flask server...")
    print("[SERVER] Buka browser ke: http://localhost:5000")
    print("[SERVER] Tekan Ctrl+C untuk menghentikan server\n")
    
    # Jalankan Flask
    # debug=False agar tidak double-load saat startup
    app.run(debug=False, host='0.0.0.0', port=5000)

