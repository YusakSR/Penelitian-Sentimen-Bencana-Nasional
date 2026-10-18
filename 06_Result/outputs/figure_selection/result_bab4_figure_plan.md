# RENCANA VISUALISASI BAB IV

**Penelitian:** Sentimen Penetapan Bencana Nasional

**Tahap:** 06_Result Part3

## 1. Prinsip Seleksi

Pemilihan grafik mengutamakan kaitan langsung dengan
rumusan masalah dan hasil penelitian utama.

Seluruh grafik berasal dari artefak Modeling dan Temporal
yang telah diaudit. Tidak ada grafik dilatih, dihitung ulang,
atau dibuat ulang dalam Part3.

Sepuluh gambar direkomendasikan sebagai visual utama.
Tujuh gambar menjadi pendukung atau lampiran.

## 2. Urutan Naratif yang Disarankan

### 4.3 Hasil Pemodelan

- Perbandingan metrik baseline vs LSTM
- Confusion matrix LSTM
- F1-score per kelas

Gunakan metrik OOF dan beri penjelasan
bahwa tidak ada independent holdout test set.

### 4.5 Analisis Temporal

- Jumlah tweet harian Lombok, Palu, Sumatera
- Persentase sentimen harian Lombok, Palu, Sumatera

Gunakan label manusia, bukan prediksi LSTM.
Semua tanggal dalam WIB.
Tanggal tanpa observasi bukan bukti aktivitas publik nol.
Pembahasan persentase harus memperhatikan ukuran sampel.

### 4.6 Perbandingan Kasus

- Komposisi sentimen pada tiga kasus

Grafik menggambarkan proporsi sampel tweet,
bukan estimasi opini seluruh masyarakat.

## 3. Lampiran

- Training loss per fold
- Training accuracy per fold
- Macro-F1 LSTM per fold
- Vocabulary size per fold
- Token count distribution
- Token count by label
- Relative-day tweet volume

Untuk grafik relative-day, hari 0 adalah hari pertama
observasi, bukan awal kejadian bencana.

## 4. Batasan Interpretasi

- Sampel berlabel berjumlah 348 tweet.
- NEGATIF hanya memiliki 15 tweet aktual.
- Evaluasi model memakai SGKF 3-fold OOF.
- Grafik temporal memakai label manusia yang dikunci.
- Periode pengamatan antarkasus berbeda.
- Tidak dilakukan inferensi populasi atau kausal.
- Penomoran Gambar 4.x bersifat provisional.

## 5. Ketentuan Reproducibility

Seluruh PNG direferensikan ke lokasi aslinya.
Tidak ada penggandaan atau perubahan file gambar.
SHA-256 disimpan di result_figure_selection_17.csv
dan part3_figure_selection_audit.json.

## 6. Pemeriksaan Editorial

Buka Markdown preview sebelum finalisasi.
Periksa keterbacaan label, legenda, caption,
dan posisi gambar pada dokumen akhir.

**Tahap berikutnya:** Result Part4 —
Discussion & Research Question Alignment.
