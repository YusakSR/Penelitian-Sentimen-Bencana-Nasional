# HASIL PENELITIAN TERKONSOLIDASI

**Penelitian:** Sentimen Penetapan Bencana Nasional

**Tahap:** 06_Result Part2 — Consolidated Research Results

**Tanggal pembuatan UTC:** 2026-10-18T16:26:47.120690+00:00

## 1. Ruang Lingkup

Laporan ini mengintegrasikan hasil fase Modeling dan
Temporal menggunakan 348 tweet yang telah direkonsiliasi
pada Result Part1.

Perhitungan model bersumber dari prediksi out-of-fold (OOF).
Analisis temporal menggunakan label manusia yang dikunci.

Tidak dilakukan pelatihan model atau penambahan data baru.

## 2. Karakteristik Dataset

| case_name | total_tweets | count_NETRAL | count_POSITIF | count_NEGATIF |
| --- | --- | --- | --- | --- |
| Lombok 2018 | 101 | 65 | 33 | 3 |
| Palu 2018 | 105 | 71 | 29 | 5 |
| Sumatera 2025 | 142 | 89 | 46 | 7 |

Dataset berisi **348 tweet**, dengan distribusi label:
NETRAL **225**, POSITIF **108**, dan NEGATIF **15**.

Jumlah leakage group unik: **337**.
Distribusi kelas tidak seimbang; karena itu interpretasi
metrik tidak cukup hanya menggunakan accuracy.

## 3. Evaluasi Model

| model | n_oof | accuracy | macro_precision | macro_recall | macro_f1 | weighted_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | 348 | 0.7040 | 0.7761 | 0.4943 | 0.5236 | 0.6898 |
| lstm | 348 | 0.5862 | 0.4760 | 0.5596 | 0.4751 | 0.6175 |

Protokol evaluasi: **SGKF_3fold_seed123**.
Metrik utama: **OOF Macro-F1**.

Baseline TF-IDF + Logistic Regression memiliki
OOF Macro-F1 **0.5236**, sedangkan
LSTM memiliki **0.4751**.

Perbedaan Macro-F1 baseline dikurangi LSTM adalah
**0.0484** poin.

Baseline juga memiliki accuracy yang lebih tinggi.
Sebaliknya, Macro-Recall LSTM lebih tinggi.

Peringkat tersebut bersifat deskriptif untuk hasil OOF.
Tidak ada independent holdout test set.

## 4. Analisis Kesalahan per Kelas

| model | sentiment_label | support | true_positive | false_positive | false_negative | precision | recall | f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | NETRAL | 225 | 187 | 62 | 38 | 0.7510 | 0.8311 | 0.7890 |
| baseline | POSITIF | 108 | 56 | 41 | 52 | 0.5773 | 0.5185 | 0.5463 |
| baseline | NEGATIF | 15 | 2 | 0 | 13 | 1.0000 | 0.1333 | 0.2353 |
| lstm | NETRAL | 225 | 139 | 36 | 86 | 0.7943 | 0.6178 | 0.6950 |
| lstm | POSITIF | 108 | 57 | 58 | 51 | 0.4957 | 0.5278 | 0.5112 |
| lstm | NEGATIF | 15 | 8 | 50 | 7 | 0.1379 | 0.5333 | 0.2192 |

Kelas NEGATIF memiliki 15 contoh aktual.
Baseline menghasilkan recall NEGATIF lebih rendah,
sementara LSTM memiliki lebih banyak false positive
NEGATIF. Perbedaan ini harus dibahas sebagai
trade-off precision dan recall, bukan hanya jumlah
prediksi benar.

## 5. Perbandingan Kesalahan Berpasangan

| Kategori | Jumlah tweet |
| --- | ---: |
| Kedua model benar | 165 |
| Hanya baseline benar | 80 |
| Hanya LSTM benar | 39 |
| Kedua model salah | 64 |
| **Total** | **348** |

Perbandingan ini menunjukkan tumpang tindih dan
perbedaan pola kesalahan kedua model pada tweet
yang sama. Belum dilakukan uji signifikansi statistik.

## 6. Ringkasan Hasil Temporal

| case_name | calendar_days | observed_days | zero_tweet_days | peak_date_wib | peak_daily_tweets |
| --- | --- | --- | --- | --- | --- |
| Lombok 2018 | 9 | 6 | 3 | 2018-08-10 | 24 |
| Palu 2018 | 5 | 5 | 0 | 2018-10-01 | 36 |
| Sumatera 2025 | 6 | 4 | 2 | 2025-12-03 | 54 |

Jumlah kalender kasus: **20 hari**.
Hari dengan observasi: **15 hari**.
Hari tanpa observasi: **5 hari**.

Komposisi sentimen NETRAL merupakan yang terbesar
pada ketiga kasus. Hari tanpa tweet ditandai secara
eksplisit dan tidak dihitung sebagai persentase nol.

Perbandingan volume dan proporsi bersifat deskriptif
atas sampel yang terkumpul, bukan estimasi aktivitas
atau opini seluruh pengguna X.

## 7. Sintesis Hasil

1. Baseline mengungguli LSTM pada metrik utama
   OOF Macro-F1, tetapi LSTM memiliki Macro-Recall
   lebih tinggi.
2. Kelas NEGATIF menjadi tantangan evaluasi
   karena support sangat kecil.
3. Analisis Temporal menggambarkan dominasi NETRAL
   pada ketiga kasus dan cakupan observasi yang
   tidak seragam.
4. Hasil Modeling mengevaluasi kemampuan prediksi,
   sementara hasil Temporal menggambarkan label
   manusia menurut waktu.
5. Tidak ada bukti dalam analisis ini yang cukup
   untuk menyimpulkan hubungan kausal antara
   penetapan status bencana dan sentimen masyarakat.

## 8. Batasan Interpretasi

- Sampel penelitian terdiri atas 348 tweet.
- Label NEGATIF hanya mencakup 15 tweet.
- Evaluasi model menggunakan OOF tiga fold,
  tanpa test set independen.
- Periode pengamatan antarkasus berbeda.
- Hari tanpa tweet tidak berarti aktivitas publik nol.
- Tidak dilakukan pengujian signifikansi atas
  perbedaan model dalam tahap ini.
- Tidak dilakukan inferensi populasi atau kausal.

## 9. Kesiapan Part3

Empat tabel konsolidasi dalam laporan ini
dapat digunakan untuk menyeleksi figur yang
relevan bagi BAB IV.

**Tahap berikutnya: 06_Result Part3 —
Results Visualization & Figure Selection.**
