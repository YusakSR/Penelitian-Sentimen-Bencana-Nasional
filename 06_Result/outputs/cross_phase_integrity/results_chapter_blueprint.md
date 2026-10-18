# BLUEPRINT BAB IV — HASIL DAN PEMBAHASAN

**Penelitian:** Sentimen Penetapan Bencana Nasional

**Status:** Blueprint awal berdasarkan hasil audit lintas fase.

> Struktur ini dapat disesuaikan dengan proposal dan
> pedoman penulisan kampus. Belum merupakan naskah
> BAB IV final.

## 4.1 Gambaran Umum Dataset

- Jelaskan sumber dan proses seleksi data.
- Sajikan 348 tweet berlabel manusia.
- Distribusi kasus: Lombok 101, Palu 105, Sumatera 142.
- Distribusi sentimen: NETRAL 225, POSITIF 108, NEGATIF 15.
- Jelaskan 337 leakage groups dan pengendalian leakage.
- Jelaskan keterbatasan cakupan sampel.

## 4.2 Metode dan Pengaturan Evaluasi

- Stratified Group K-Fold tiga fold, seed 123.
- Baseline TF-IDF + Logistic Regression.
- Model LSTM_SMALL_V1.
- Metrik utama Out-of-Fold Macro-F1.
- Bedakan training, validation, dan OOF.
- Tidak ada independent holdout test set.

## 4.3 Hasil Pemodelan Sentimen

- Sajikan metrik kedua model.
- Baseline: accuracy 0.7040, Macro-F1 0.5236.
- LSTM: accuracy 0.5862, Macro-F1 0.4751.
- Bahas grafik hasil modeling dan confusion matrix.
- Jelaskan indikasi overfitting LSTM.
- Bahas kelemahan kedua model pada kelas NEGATIF.

## 4.4 Analisis Kesalahan Klasifikasi

- Kedua model benar: 165 tweet.
- Hanya baseline benar: 80 tweet.
- Hanya LSTM benar: 39 tweet.
- Kedua model salah: 64 tweet.
- Jelaskan perbedaan precision dan recall NEGATIF.
- Jangan menyatakan signifikansi statistik tanpa pengujian.

## 4.5 Distribusi Sentimen dan Analisis Temporal

- Gunakan label manusia, bukan prediksi model.
- Sajikan jumlah dan persentase harian per kasus.
- Tampilkan 20 hari kalender kasus.
- Sebanyak 15 hari memiliki observasi dan 5 hari kosong.
- Gunakan grafik temporal asli Part4.
- Hari relatif 0 berarti awal observasi, bukan awal bencana.

## 4.6 Pembahasan Perbandingan Kasus

- Bandingkan Lombok, Palu, dan Sumatera secara deskriptif.
- Bedakan jumlah tweet dan proporsi sentimen.
- Jelaskan variasi cakupan waktu dan distribusi sampel.
- Hindari generalisasi sebagai opini seluruh masyarakat.
- Hindari klaim hubungan sebab-akibat kebijakan.

## 4.7 Keterbatasan Penelitian

- Hanya 348 tweet berlabel.
- Kelas NEGATIF sangat kecil (15 tweet).
- Perbedaan jendela pengamatan antarkasus.
- Pengaruh strategi scraping dan seleksi sampel.
- Tidak tersedia independent holdout.
- Potensi overfitting pada LSTM.
- Hasil temporal bersifat deskriptif.

## 4.8 Ringkasan Temuan

- Baseline lebih tinggi menurut OOF Macro-F1.
- LSTM memiliki Macro-Recall lebih tinggi.
- NETRAL mendominasi sampel ketiga kasus.
- Pola temporal berbeda menurut kasus.
- Simpulan terbatas pada sampel dan metode penelitian.

## Catatan Integrasi

Modeling menjelaskan performa prediksi.
Temporal menjelaskan distribusi label manusia.
Keduanya menggunakan 348 tweet yang sama,
tetapi menjawab pertanyaan analitis berbeda.

Dokumen ini merupakan blueprint.
Finalisasi BAB IV harus disesuaikan dengan
rumusan masalah, tujuan, serta pedoman akademik.
