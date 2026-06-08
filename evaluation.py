# ============================================================
# evaluation.py
# Modul Evaluasi Sistem Temu Kembali Informasi
# ============================================================
# Modul ini berisi fungsi-fungsi untuk mengevaluasi performa
# sistem temu kembali informasi menggunakan metrik standar IR.
#
# Metrik Evaluasi yang Digunakan:
#
# 1. Precision@K
#    - Proporsi dokumen relevan di antara K dokumen teratas
#    - Rumus: Precision@K = |Relevant ∩ Retrieved@K| / K
#    - Contoh: Dari 5 hasil, 3 relevan → Precision@5 = 3/5 = 0.6
#
# 2. Recall
#    - Proporsi dokumen relevan yang berhasil ditemukan
#    - Rumus: Recall = |Relevant ∩ Retrieved| / |Relevant|
#    - Contoh: Ada 4 dokumen relevan, ditemukan 3 → Recall = 3/4 = 0.75
#
# 3. MAP (Mean Average Precision)
#    - Rata-rata Average Precision untuk semua query
#    - AP menghitung precision di setiap posisi dokumen relevan
#    - MAP = rata-rata AP dari seluruh query pengujian
#    - Merupakan metrik evaluasi IR yang paling komprehensif
#
# 4. NDCG@K (Normalized Discounted Cumulative Gain)
#    - Mengukur performa peringkat hasil pencarian dengan memberikan
#      bobot penalti diskon berdasarkan posisi dokumen relevan.
#    - Rumus: NDCG@K = DCG@K / IDCG@K
#
# 5. Confusion Matrix (TP, FP, FN, TN)
#    - Matriks evaluasi klasifikasi biner untuk memetakan dokumen
#      relevan (Positive) vs tidak relevan (Negative) yang terpanggil (Retrieved)
#      vs tidak terpanggil (Non-Retrieved).
# ============================================================

import json
import math
from tabulate import tabulate


# ============================================================
# GROUND TRUTH
# ============================================================
# Ground truth mendefinisikan kategori yang SEHARUSNYA relevan
# untuk setiap query pengujian.
#
# Contoh: Query "football world cup" seharusnya menghasilkan
# dokumen dari kategori "sport"
# ============================================================

GROUND_TRUTH = {
    "football world cup": {
        "relevant_categories": ["sport"],
        "description": "Berita tentang sepak bola dan piala dunia"
    },
    "government election": {
        "relevant_categories": ["politics"],
        "description": "Berita tentang pemerintahan dan pemilihan umum"
    },
    "stock market crash": {
        "relevant_categories": ["business"],
        "description": "Berita tentang pasar saham dan krisis keuangan"
    },
    "smartphone technology": {
        "relevant_categories": ["tech"],
        "description": "Berita tentang smartphone dan teknologi"
    },
    "movie awards ceremony": {
        "relevant_categories": ["entertainment"],
        "description": "Berita tentang penghargaan film dan seni"
    },
    "internet security threat": {
        "relevant_categories": ["tech"],
        "description": "Berita tentang keamanan internet"
    },
    "oil price economy": {
        "relevant_categories": ["business"],
        "description": "Berita tentang harga minyak dan ekonomi"
    },
    "music album release": {
        "relevant_categories": ["entertainment"],
        "description": "Berita tentang album musik dan rilisan"
    },
    "climate change policy": {
        "relevant_categories": ["politics"],
        "description": "Berita tentang kebijakan perubahan iklim"
    },
    "artificial intelligence computer": {
        "relevant_categories": ["tech"],
        "description": "Berita tentang kecerdasan buatan dan komputer"
    }
}


def precision_at_k(retrieved_categories, relevant_categories, k=5):
    """
    Menghitung Precision@K.
    """
    top_k = retrieved_categories[:k]
    relevant_count = sum(1 for cat in top_k if cat in relevant_categories)
    return relevant_count / k if k > 0 else 0.0


def recall(retrieved_categories, relevant_categories, total_relevant):
    """
    Menghitung Recall.
    """
    relevant_found = sum(1 for cat in retrieved_categories if cat in relevant_categories)
    return relevant_found / total_relevant if total_relevant > 0 else 0.0


def average_precision(retrieved_categories, relevant_categories):
    """
    Menghitung Average Precision (AP) untuk satu query.
    """
    relevant_count = 0
    precision_sum = 0.0
    
    for i, cat in enumerate(retrieved_categories):
        if cat in relevant_categories:
            relevant_count += 1
            precision_at_i = relevant_count / (i + 1)
            precision_sum += precision_at_i
    
    if relevant_count == 0:
        return 0.0
    
    return precision_sum / relevant_count


def mean_average_precision(all_ap_scores):
    """
    Menghitung Mean Average Precision (MAP).
    """
    if not all_ap_scores:
        return 0.0
    return sum(all_ap_scores) / len(all_ap_scores)


def ndcg_at_k(retrieved_categories, relevant_categories, total_relevant, k=5):
    """
    Menghitung NDCG@K (Normalized Discounted Cumulative Gain).
    
    Parameter:
        retrieved_categories (list): Kategori dari dokumen yang dikembalikan.
        relevant_categories (list): Kategori yang dianggap relevan.
        total_relevant (int): Total dokumen relevan yang ada di dataset.
        k (int): Kedalaman ranking yang dihitung (default: 5).
    """
    retrieved_in_k = retrieved_categories[:k]
    
    # Hitung relevance score biner (1 untuk relevan, 0 untuk tidak)
    relevance = [1 if cat in relevant_categories else 0 for cat in retrieved_in_k]
    
    # Hitung DCG@K
    dcg = 0.0
    for i, rel in enumerate(relevance):
        dcg += rel / math.log2(i + 2)  # Log basis 2 (i+2 karena index 0 mewakili rank 1)
        
    # Hitung IDCG@K (Ideal DCG@K jika hasil peringkat diurutkan secara sempurna)
    idcg = 0.0
    max_possible_relevant = min(total_relevant, k)
    for i in range(max_possible_relevant):
        idcg += 1.0 / math.log2(i + 2)
        
    if idcg == 0.0:
        return 0.0
    
    return dcg / idcg


def confusion_matrix_metrics(retrieved_categories, relevant_categories, total_relevant, total_docs, k=5):
    """
    Menghitung metrik Confusion Matrix (TP, FP, FN, TN) untuk kueri tunggal.
    
    Parameter:
        retrieved_categories (list): Kategori dari dokumen yang dikembalikan.
        relevant_categories (list): Kategori yang dianggap relevan.
        total_relevant (int): Total dokumen relevan yang ada di dataset.
        total_docs (int): Total dokumen dalam dataset.
        k (int): Jumlah dokumen teratas yang terambil (default: 5).
    """
    retrieved_in_k = retrieved_categories[:k]
    
    tp = sum(1 for cat in retrieved_in_k if cat in relevant_categories)
    fp = len(retrieved_in_k) - tp
    fn = total_relevant - tp
    tn = total_docs - total_relevant - fp
    
    return {
        'tp': tp,
        'fp': fp,
        'fn': fn,
        'tn': tn
    }


def run_evaluation(search_func, vectorizer, tfidf_matrix, df):
    """
    Menjalankan evaluasi lengkap sistem IR dengan metrik tambahan.
    """
    results_per_query = []
    all_ap_scores = []
    all_precision_scores = []
    all_recall_scores = []
    all_ndcg_scores = []
    
    total_tp = 0
    total_fp = 0
    total_fn = 0
    total_tn = 0
    total_docs = len(df)
    
    print("\n" + "=" * 80)
    print("EVALUASI SISTEM TEMU KEMBALI INFORMASI (STKI)")
    print("=" * 80)
    
    for query, ground_truth in GROUND_TRUTH.items():
        # Lakukan pencarian
        search_result = search_func(
            query, vectorizer, tfidf_matrix, df, top_k=5
        )
        
        # Ambil kategori dari hasil pencarian
        retrieved_cats = [r['category'] for r in search_result['results']]
        relevant_cats = ground_truth['relevant_categories']
        
        # Hitung total dokumen relevan di dataset
        total_rel = len(df[df['category'].isin(relevant_cats)])
        
        # Hitung metrik dasar
        p_at_5 = precision_at_k(retrieved_cats, relevant_cats, k=5)
        rec = recall(retrieved_cats, relevant_cats, total_rel)
        ap = average_precision(retrieved_cats, relevant_cats)
        
        # Hitung metrik baru
        ndcg_val = ndcg_at_k(retrieved_cats, relevant_cats, total_rel, k=5)
        cm = confusion_matrix_metrics(retrieved_cats, relevant_cats, total_rel, total_docs, k=5)
        
        all_precision_scores.append(p_at_5)
        all_recall_scores.append(rec)
        all_ap_scores.append(ap)
        all_ndcg_scores.append(ndcg_val)
        
        # Akumulasikan Confusion Matrix global
        total_tp += cm['tp']
        total_fp += cm['fp']
        total_fn += cm['fn']
        total_tn += cm['tn']
        
        results_per_query.append({
            'query': query,
            'relevant_categories': relevant_cats,
            'retrieved_categories': retrieved_cats,
            'precision_at_5': round(p_at_5, 4),
            'recall': round(rec, 4),
            'average_precision': round(ap, 4),
            'ndcg_at_5': round(ndcg_val, 4),
            'confusion_matrix': cm,
            'results_count': len(search_result['results'])
        })
    
    # Hitung rata-rata
    avg_precision = sum(all_precision_scores) / len(all_precision_scores) if all_precision_scores else 0
    avg_recall = sum(all_recall_scores) / len(all_recall_scores) if all_recall_scores else 0
    map_score = mean_average_precision(all_ap_scores)
    avg_ndcg = sum(all_ndcg_scores) / len(all_ndcg_scores) if all_ndcg_scores else 0
    
    # Hitung metrik turunan dari Global Confusion Matrix
    global_accuracy = (total_tp + total_tn) / (total_tp + total_fp + total_fn + total_tn) if (total_tp + total_fp + total_fn + total_tn) > 0 else 0.0
    global_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    global_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    global_f1 = 2 * (global_precision * global_recall) / (global_precision + global_recall) if (global_precision + global_recall) > 0 else 0.0
    
    # Tampilkan tabel hasil
    table_data = []
    for r in results_per_query:
        table_data.append([
            r['query'],
            ', '.join(r['relevant_categories']),
            ', '.join(r['retrieved_categories']) if r['retrieved_categories'] else '-',
            r['precision_at_5'],
            r['recall'],
            r['ndcg_at_5'],
            r['average_precision']
        ])
    
    headers = ['Query', 'Expected Cat.', 'Retrieved Cat.', 'P@5', 'Recall', 'NDCG@5', 'AP']
    print("\n" + tabulate(table_data, headers=headers, tablefmt='grid'))
    
    print(f"\n{'=' * 50}")
    print(f"RATA-RATA EVALUASI")
    print(f"{'=' * 50}")
    print(f"  Average Precision@5 : {avg_precision:.4f}")
    print(f"  Average Recall      : {avg_recall:.4f}")
    print(f"  MAP                 : {map_score:.4f}")
    print(f"  Average NDCG@5      : {avg_ndcg:.4f}")
    print(f"{'=' * 50}")
    print(f"GLOBAL CONFUSION MATRIX")
    print(f"{'=' * 50}")
    print(f"  True Positives (TP)  : {total_tp}")
    print(f"  False Positives (FP) : {total_fp}")
    print(f"  False Negatives (FN) : {total_fn}")
    print(f"  True Negatives (TN)  : {total_tn}")
    print(f"  Global Accuracy      : {global_accuracy:.4f}")
    print(f"  Global Precision     : {global_precision:.4f}")
    print(f"  Global Recall        : {global_recall:.4f}")
    print(f"  Global F1-Score      : {global_f1:.4f}")
    print(f"{'=' * 50}\n")
    
    evaluation_summary = {
        'results_per_query': results_per_query,
        'average_precision': round(avg_precision, 4),
        'average_recall': round(avg_recall, 4),
        'map_score': round(map_score, 4),
        'average_ndcg': round(avg_ndcg, 4),
        'global_confusion_matrix': {
            'tp': total_tp,
            'fp': total_fp,
            'fn': total_fn,
            'tn': total_tn,
            'accuracy': round(global_accuracy, 4),
            'precision': round(global_precision, 4),
            'recall': round(global_recall, 4),
            'f1_score': round(global_f1, 4)
        },
        'total_queries': len(GROUND_TRUTH)
    }
    
    return evaluation_summary


# ============================================================
# Jika file ini dijalankan langsung
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("MODUL EVALUASI IR")
    print("=" * 60)
    print("\nGround Truth Queries:")
    for i, (query, gt) in enumerate(GROUND_TRUTH.items(), 1):
        print(f"  {i}. '{query}' -> {gt['relevant_categories']} ({gt['description']})")
    print(f"\nTotal query pengujian: {len(GROUND_TRUTH)}")
    print("\nJalankan evaluasi lengkap melalui app.py atau route /evaluation")
    print("=" * 60)

