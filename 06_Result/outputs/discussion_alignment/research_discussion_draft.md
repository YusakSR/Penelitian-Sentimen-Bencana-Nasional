# DRAFT PEMBAHASAN DAN KESESUAIAN RUMUSAN MASALAH

**Penelitian:** Sentimen Penetapan Bencana Nasional

**Fase:** 06_Result Part4

**Sifat dokumen:** Draft akademik, bukan naskah
final yang telah disetujui pembimbing.

## 1. Kerangka Pembahasan

Rumusan masalah mengacu pada bagian 1.2 proposal
`G1F020005_Mariana ClaudyaNEW.pdf`.

Penelitian menggunakan 348 tweet berlabel manusia,
dengan distribusi NETRAL 225, POSITIF 108,
dan NEGATIF 15 tweet.

Hasil Modeling dan Temporal mengacu pada 348 tweet
yang sama, sebagaimana diaudit pada Result Part1.

## 2. Pembahasan RM1 — Penerapan LSTM

Model LSTM diterapkan pada data tweet berbahasa
Indonesia dengan evaluasi Stratified Group K-Fold
tiga fold dan prediksi out-of-fold.

LSTM menghasilkan accuracy **58.62%**
dan Macro-F1 **0.4751**.

Sebagai benchmark tambahan, baseline
TF-IDF + Logistic Regression memperoleh accuracy
**70.40%** dan Macro-F1
**0.5236**.

Selisih Macro-F1 baseline terhadap LSTM
sebesar **0.0484**.
Macro-Recall LSTM mencapai
**0.5596**, lebih tinggi dibandingkan
baseline **0.4943**.

Hasil ini tidak membuktikan bahwa LSTM unggul
dalam seluruh indikator. Evaluasi memakai OOF,
bukan independent holdout.

**Catatan penyelarasan:** proposal awal menyatakan
LSTM tanpa perbandingan metode. Penggunaan baseline
harus dikonfirmasi dan dijelaskan bersama pembimbing.

## 3. Pembahasan RM2 — Hasil Klasifikasi LSTM

Klasifikasi mencakup tiga kategori sentimen:
NETRAL, POSITIF, dan NEGATIF.

Pada kelas NEGATIF, hanya terdapat 15 tweet
aktual. LSTM memperoleh true positive
**8**,
false negative
**7**
dan false positive
**50**.

Recall NEGATIF LSTM sebesar
**53.33%**,
tetapi precision hanya
**13.79%**.

Dengan demikian, kenaikan sensitivitas model
terhadap NEGATIF disertai peningkatan prediksi
NEGATIF yang keliru.

Kinerja tidak dapat dinilai berdasarkan accuracy
saja karena ketidakseimbangan kelas.

Hasil klasifikasi LSTM adalah prediksi model yang
dievaluasi terhadap label manusia, bukan pengukuran
langsung seluruh opini publik.

## 4. Pembahasan RM3 — Dinamika Temporal

Analisis Temporal menggunakan timestamp publikasi
tweet yang dikonversi menjadi WIB dan label
manusia yang telah dikunci.

Total cakupan adalah 20 hari kalender kasus,
terdiri atas 15 hari dengan observasi dan
5 hari tanpa tweet pada dataset.

- **Lombok 2018:** 101 tweet, 6/9 hari berobservasi, 3 hari tanpa observasi. Puncak sampel harian 24 tweet pada 2018-08-10 (WIB).
- **Palu 2018:** 105 tweet, 5/5 hari berobservasi, 0 hari tanpa observasi. Puncak sampel harian 36 tweet pada 2018-10-01 (WIB).
- **Sumatera 2025:** 142 tweet, 4/6 hari berobservasi, 2 hari tanpa observasi. Puncak sampel harian 54 tweet pada 2025-12-03 (WIB).

NETRAL menjadi kategori terbesar pada ketiga
kasus. Fluktuasi jumlah dan proporsi harian
merupakan gambaran sampel tweet yang terkumpul.

Tanggal tanpa tweet tidak boleh diartikan
sebagai tidak adanya percakapan publik.

Hari relatif dalam grafik adalah hari sejak awal
jendela observasi, bukan hari sejak kejadian
bencana atau keputusan penetapan status.

**Batasan penting:** hasil temporal saat ini
menggunakan label manusia, bukan hasil prediksi
LSTM. Karena itu, hasil ini menjawab dinamika
label sentimen dalam sampel, belum membuktikan
dinamika prediksi berbasis model LSTM.

## 5. Integrasi Ketiga Rumusan Masalah

RM1 dijawab melalui implementasi dan evaluasi LSTM.

RM2 dijawab melalui performa prediksi LSTM
pada tiga kategori sentimen dan analisis kesalahan.

RM3 dijawab secara deskriptif melalui agregasi
harian sentimen berlabel manusia untuk tiga kasus.

Interpretasi RM1–RM3 harus membedakan
evaluasi prediksi dari karakteristik data berlabel.

## 6. Keterbatasan dan Validitas

1. Dataset berisi 348 tweet, bukan sampel
   representatif seluruh pengguna X.
2. Kelas NEGATIF hanya 15 tweet.
3. Tidak tersedia independent holdout test set.
4. Periode pengamatan tiga kasus tidak sama.
5. Lima hari kalender kasus tidak memiliki observasi.
6. Tidak terdapat bukti hubungan sebab-akibat
   antara kebijakan dan pergeseran sentimen.
7. Benchmark baseline belum selaras dengan batasan
   metode pada proposal.
8. Agregasi temporal saat ini tidak menggunakan
   prediksi LSTM.

## 7. Keputusan Metodologis Sebelum BAB IV Final

- Konfirmasi kepada pembimbing apakah baseline
  Logistic Regression boleh dipertahankan sebagai
  benchmark tambahan.
- Konfirmasi apakah RM3 cukup dianalisis dari
  label manusia atau memerlukan analisis tambahan
  dari prediksi model.
- Seragamkan definisi penetapan bencana nasional
  dengan kebijakan penanggulangan bencana.
- Pertahankan penjelasan sampling, class imbalance,
  dan keterbatasan generalisasi.

**Status:** Draft pembahasan siap ditinjau.
Persetujuan metodologis masih diperlukan.
