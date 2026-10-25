# Sampling dan labeling — bukti awal Part2

Baseline: `09391e6c5777a8c34edd8482a8bf3e2859f64408`. Status akademik: **PROVISIONAL**.

## Sampling dan unit observasi

Konfigurasi `01_Raw Data/full_scraping_raw_data.ipynb`, cell 5, menggunakan gabungan keyword peristiwa dan kebijakan, bahasa `lang:in`, serta periode inklusif WIB: Lombok 29 Juli–31 Agustus 2018, Palu 28 September–31 Oktober 2018, dan Sumatra 26 November–31 Desember 2025. Ini adalah rentang konfigurasi pencarian; jangan mengartikannya sebagai cakupan data setiap hari. Rencana full awal 416 task dan target 4.000–5.000 tweet bukan jumlah observasi hasil akhir.

Bukti koleksi final mencatat 65 task tersimpan, 1.508 record raw, 989 kemunculan tweet asli, 519 mock dan 411 ID unik. ID dipertahankan sebagai string, tanpa konversi float/angka spreadsheet. Manual review menghasilkan 381 INCLUDE dan 30 EXCLUDE, dengan audit keputusan tetap tersimpan. Screening relevansi tidak sama dengan pemberian sentimen.

Pada cleaning, seluruh 381 ID tetap di master. Dua puluh satu grup duplikat mencakup 54 anggota; satu perwakilan dipilih dari setiap grup. Dengan 327 tweet nonduplikat, kandidat modeling menjadi 348. Sebanyak 33 anggota yang tidak dipilih tetap ada di master. Dua belas teks panjang berstatus KEEP_FULL menurut summary/review; tidak ada pemotongan ulang dalam pekerjaan dokumentasi ini.

## Label dan versi keputusan

Codebook v1.1 adalah sumber definisi operasional POSITIF, NEGATIF dan NETRAL terhadap sasaran kebijakan; sumber codebook dan hash ada pada manifest. Dokumentasi ini tidak menebak label dari polaritas umum teks. Pilot 30 memiliki distribusi 20 NETRAL, 8 POSITIF, 2 NEGATIF setelah adjudikasi; workbook penuh disiapkan dengan 351 sisanya menunggu. Kedua angka adalah tahap historis, bukan status akhir.

Master final 381 mencatat 351 `FULL_MANUAL` dan 30 `PILOT_ADJUDICATED`. Handoff 348 mencatat 318 `FULL_MANUAL` dan 30 `PILOT_ADJUDICATED`. Field `label_notes`, `annotator`, `labeled_at`, `sentiment_label_original`, `adjudication_applied` dan catatan adjudikasi dipertahankan. Kategori provenance yang tercatat tidak cukup untuk menilai independensi anotator atau reliabilitas antar-penilai; metrik tersebut tidak dibuat.

Pada fase 03, empat baris dalam dua grup duplikat ditinjau dan dua label berubah; seluruh 381 memiliki label final, lalu 348 kandidat dipilih dengan ID yang sama seperti input. Pada fase 04, empat tweet near-duplicate ditinjau lagi dan dua POSITIF diubah menjadi NETRAL. Handoff fase 03 memiliki 223/110/15 (NETRAL/POSITIF/NEGATIF); dataset modeling terkunci memiliki 225/108/15. Kedua versi tetap disimpan dan disandingkan per ID.

## Bukti hybrid yang belum lengkap

`hybrid_preflight_manifest.json` mencatat 130 locked (30 pilot + 100 batch A) dan 251 pending. Snapshot CSV keduanya membentuk partisi 381 ID yang lengkap dan tidak beririsan. Namun file bernama `ai_predictions_251.csv` hanya berisi 10 prediksi, semuanya termasuk ID pending, dengan field model `qwen2.5:3b` pada bukti yang tersedia.

Tidak ada producer cell hybrid yang tercatat pada notebook labeling sumber dan tidak ada log lengkap penerimaan/review AI untuk 251 baris. Kecocokan label AI dengan label final, seandainya ada, tidak membuktikan adopsi saran AI. Pernyataan metode labeling final memerlukan bukti pelengkap atau klarifikasi peneliti. Tidak dilakukan pemanggilan AI ulang, pengisian label, atau perubahan `annotation_source`.

## Batas interpretasi dan tahap berikutnya

Sampel akhir terdiri atas 101 Lombok, 105 Palu, 142 Sumatra dan hanya 15 NEGATIF. Cakupan query/waktu dan proses seleksi membatasi generalisasi. Jumlah ID bukan jumlah responden independen yang telah dibuktikan. Hasil pengamatan tidak membuktikan efek kausal keputusan kebijakan.

Empat isu metodologis yang diwarisi dari fase Result tetap terbuka: benchmark di luar batas proposal, hubungan label temporal versus prediksi LSTM, istilah kebijakan/interpretasi kausal, serta cakupan sampel dan desain evaluasi. Gap provenance hybrid dicatat sebagai kebutuhan bukti Part2 terpisah dan tidak mengubah atau menutup empat isu tersebut.

Langkah berikutnya adalah melengkapi log provenance labeling dan meninjau dokumen dengan peneliti/pembimbing. Pekerjaan saat ini hanya mendokumentasikan bukti tersimpan. Tidak ada klaim bahwa metode, hasil akademik atau PDF sudah mendapat persetujuan akhir.
