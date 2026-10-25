# Panduan urutan cell, Google Colab, dan bukti BAB IV

Sumber penelitian: commit `d344822ab6d6aaca76b3c658c101c54e4b25bac1` pada repository `YusakSR/Penelitian-Sentimen-Bencana-Nasional`.
Nomor di bawah adalah **posisi cell asli, termasuk Markdown, dihitung dari 1**, bukan angka `In[ ]` atau nomor pada judul komentar. Contoh: cell fisik 24 Modeling berjudul “Part18 — FINAL OOF PROBABILITIES CHECK”. Jangan mencari “cell 24” berdasarkan execution count.

## 1. Pilih tujuan sebelum menjalankan

| Tujuan | Jalur yang digunakan | Hasil |
|---|---|---|
| Orang lain memeriksa penelitian, melihat hasil, menyiapkan screenshot/gambar BAB IV | **Notebook pendamping read-only**, V01–V19 | Bisa menampilkan artefak final dan output arsip tanpa scraping/training |
| Membaca kode dan urutan proses penelitian | Buka notebook asli, baca peta fase pada bagian 4 | Mengetahui producer cell dan checkpoint manual; tidak perlu menjalankan kode asli |
| Mengulang pengolahan/pelatihan untuk menghasilkan hasil baru | Adaptasi Colab di workspace eksperimen terpisah | Memerlukan migrasi path, representasi hash, output baru dan keputusan review manual; **belum merupakan jalur Colab yang tervalidasi** |

Notebook asli saat ini bukan aplikasi “Run all” yang siap dipindah ke Colab. Mengubah satu variabel ROOT saja tidak cukup: banyak cell mendefinisikan ulang ROOT, memakai nilai SHA dari representasi Windows, dan menolak file keluaran yang sudah ada. Beberapa cell adalah rekaman pemulihan sesi lama. Panduan ini tidak menyatakan bahwa pengulangan penuh di Colab telah berhasil diuji.

Untuk menulis BAB IV dari hasil penelitian yang sudah diaudit, gunakan jalur pertama. Tidak perlu membuat ulang dataset atau melatih model demi mendapatkan gambar yang sudah tersedia.

## 2. Step by step membuka dan menjalankan di Colab

1. Unduh `Colab_BAB_IV_Read_Only.ipynb` dalam folder panduan ini. Buka [Google Colab](https://colab.research.google.com/), masuk dengan akun Google, lalu gunakan **File → Upload notebook**. Colab mendukung notebook dari GitHub atau unggahan `.ipynb`; lihat [FAQ resmi Colab](https://research.google.com/colaboratory/faq.html).
2. Simpan salinan notebook ke Google Drive jika ingin mempertahankan catatan dan output tampilan Anda. Jangan menimpa notebook sumber penelitian.
3. Pilih runtime Python dengan akselerator **None/CPU**. Notebook penayangan ini tidak melatih model dan tidak membutuhkan GPU. Tidak diperlukan token Apify, panggilan AI, atau mount Drive.
4. Jalankan **V01**. Cell ini mengambil salinan repository pada commit sumber yang disebut di atas ke `/content/penelitian_sentimen_sumber`. Jika folder sudah berada pada commit berbeda, cell berhenti; tidak melakukan reset otomatis.
5. Jalankan **V02**. Pastikan pemeriksa melaporkan `PASS_WITH_DOCUMENTED_PROVENANCE_GAP` dan 348 observasi terlacak. Status ini mempertahankan catatan bukti AI yang belum lengkap; bukan menyatakan gap tersebut selesai.
6. Jalankan **V03 → V04 → V05 → V06 → V07** untuk melihat Raw, Cleaning, Labeling, Modeling, lalu Temporal. Screenshot proses dapat diambil di sini sesuai kebutuhan penulisan.
7. Jalankan **V08 → V09 → … → V17** untuk menampilkan sepuluh gambar utama, masing-masing satu cell. Setiap gambar diperiksa terhadap SHA pada registry final sebelum ditampilkan.
8. Jalankan **V18** jika membutuhkan tujuh gambar lampiran; lewati bila tidak diperlukan.
9. Jalankan **V19** untuk melihat tabel hasil, daftar isu metodologis, lineage, dan pemeriksaan integritas penutup. Unduh PNG asli melalui panel Files Colab pada path yang dicetak di bawah gambar. Masukkan PNG tersebut ke Word untuk kualitas naskah.
10. Simpan notebook/unduh berkas yang dibutuhkan sebelum runtime berakhir. Notebook dan isi VM adalah dua hal berbeda: berkas runtime dapat hilang ketika VM dihapus atau sesi berakhir. Rujukan: [FAQ resmi Colab, penyimpanan dan execution state](https://research.google.com/colaboratory/faq.html).

Hanya cell notebook pendamping yang dijalankan dalam jalur ini. Fungsi pembaca memperlakukan source notebook asli sebagai data; tidak ada `exec`, notebook runner atau import kode penelitian terhadap source asli. Teks dengan label **ARSIP** adalah output penelitian yang sudah tersimpan, bukan hasil eksekusi baru. Jika screenshot dipakai sebagai dokumentasi audit, jelaskan bahwa hasil tersebut ditampilkan ulang dari artefak terkunci.

### Urutan notebook pendamping

| Langkah | Isi | Sumber cell asli |
|---|---|---|
| V01–V02 | Salinan sumber dan pemeriksaan integritas | Pemeriksa dokumentasi, tanpa menjalankan source cell |
| V03 | Raw 1.508 record, 411 ID unik, 381 INCLUDE, 30 EXCLUDE | Full collection 41 dan 45 |
| V04 | Contoh teks cleaning dan seleksi 348 kandidat | Cleaning 3/4/7 untuk proses; 10/11 untuk hasil akhir |
| V05 | Label fase 03/04 dan changelog | Labeling 14/15; Modeling 6 |
| V06 | Dataset, split dan evaluasi model final | Modeling 8/12/14/24/35/37 |
| V07 | Kalender harian dan cakupan temporal | Temporal 2/3/5 |
| V08–V17 | Sepuluh gambar utama | Modeling 29/30/31; Temporal 4 |
| V18 | Grafik lampiran | Modeling 26/27/28/32/33/34; Temporal 4 |
| V19 | Result, Documentation dan verifikasi penutup | Result 1–6 dan artefak Documentation; tanpa menjalankan generator aslinya |

## 3. Cara membuka notebook asli untuk membaca

Buka GitHub pada commit sumber, pilih `.ipynb` yang dimaksud, unduh lalu **File → Upload notebook** di Colab. Membuka notebook tidak sama dengan menyalin semua data repository ke runtime. V01 pada notebook pendamping menangani salinan data untuk jalur penayangan.

Urutan fase utama: **full_scraping_raw_data → 02_text_cleaning → 03_sentiment_labeling → 04_modeling → 05_temporal → 06_result → 07_documentation**.

`01_Raw Data/raw_collection.ipynb` adalah notebook pilot/pengembangan terdahulu, bukan langkah wajib sebelum full collection final. Notebook di `backup/` adalah arsip; tidak dimasukkan ke jalur utama. Menggunakan notebook pilot bersama notebook full untuk pengumpulan baru dapat menghasilkan panggilan dan output tambahan yang tidak diperlukan untuk membaca penelitian.

## 4. Peta urutan cell asli per fase

Bagian ini adalah urutan logika dan dependensi penelitian untuk membaca source atau merencanakan migrasi. **Bukan instruksi untuk menekan Run pada semua nomor di repository yang sudah memiliki hasil.** Cell yang menulis output harus diarahkan ke folder eksperimen baru; workbook review dan hasil final yang sudah ada tetap sebagai input bukti. Checkpoint manual tidak dapat digantikan dengan sekadar melanjutkan cell berikutnya.

### Fase 01 — `01_Raw Data/full_scraping_raw_data.ipynb` (48 cell)

| Urutan | Cell asli | Peran dan tindakan |
|---|---|---|
| 1 | 1 | Baca pengantar dan batas koleksi |
| 2 | **2 → 3 → 5 → 7 → 8 → 9** | Import, path, kasus/keyword, konfigurasi, preview, preflight. Tetap default tanpa scraping; baca Markdown 4 dan 6 |
| 3 | **11 → 12 → 13 → 14 → 16** | Helper audit dan checkpoint. Baca konteks Markdown 10 dan 15 |
| 4 | 17 | Lookup biaya historis opsional, default OFF; jika diaktifkan mengakses metadata remote |
| 5 | **18 → 19 → 20 → 21 → 22** | Rekonsiliasi biaya offline, preview, baseline/yield dan helper split; bergantung snapshot/tahap koleksi lama |
| 6 | **24 → 25 → 26 → 27 → 28** | Definisi worker dan tes/gate offline. Cell 24 mendefinisikan worker yang dapat memanggil Actor; bukan bukti izin scraping baru |
| 7 | 29 | Gerbang pelaksanaan scraping. Untuk penayangan hasil: **lewati**. Pengumpulan baru adalah eksperimen terpisah dengan keputusan biaya dan target baru |
| 8 | **30 → 31 → 32 → 33 → 34 → 35** | Laporan progres, kualitas, master dan review peristiwa; sebagian menulis laporan. Cell 32 menggunakan hasil/helper sebelumnya |
| 9 | 36 | Cek environment/openpyxl, opsional |
| 10 | **37 → 38 → 39 → 40 → 41 → 42 → 43** | Registry, fokus kebijakan, yield, audit akhir, snapshot dan ekspor workbook. Snapshot/ekspor sudah ada pada repository: jangan dibuat ulang pada lokasi yang sama |
| 11 | Jeda setelah 43 | Review manual 411 tweet pada workbook sebelum validasi/reconciliation; keputusan review bukan label sentimen |
| 12 | **44 → 45** | Validasi review dan rekonsiliasi 381 INCLUDE/30 EXCLUDE; ini bukti seleksi final |
| 13 | **46: lewati untuk snapshot final** | Masih memeriksa 59 task, 1.379 raw, 372 ID dan variabel sesi `recent`; koleksi final memiliki 65 task, 1.508 raw, 411 ID |
| 14 | 47 → 48 | Helper preview semantik opsional dan catatan metode; 47 tidak otomatis dipanggil |

Untuk BAB IV, hasil final yang relevan adalah **41 dan 45**, bukan target rencana pada 7 atau snapshot lama pada 46. Pengumpulan asli mencakup beberapa sesi, sehingga urutan “semua cell sekali jalan” tidak mereproduksi sejarah pengumpulan.

### Fase 02 — `02_Cleaning/02_text_cleaning.ipynb` (11 cell)

**1 → 2 → 3 → 4 → 5 → [review semantik] → 6 → 7 → 8 → 9 → [review duplikat dan teks panjang] → 10 → 11.**

| Cell | Fungsi |
|---|---|
| 1–2 | Validasi input eligible 381 dan audit kualitas awal |
| 3 | Normalisasi aman; `clean_df`; teks asli dipertahankan |
| 4 | Social cleaning; `social_df`; contoh sebelum/sesudah |
| 5 → jeda → 6 | Ekspor review semantik lalu rekonsiliasi hasil review; jangan meregenerasi workbook final yang sudah diisi |
| 7 | Normalisasi linguistik konservatif; `ling_df` |
| 8 | Audit duplikat; 21 grup dengan 54 anggota |
| 9 → jeda → 10 | Review memilih satu perwakilan/grup dan mempertahankan teks panjang; hasilnya 327 unik + 21 perwakilan = 348 kandidat |
| 11 | Handoff 381 master dan 348 kandidat dengan label masih kosong |

Cell 3/4/7 adalah proses inti walaupun preflight lama sempat menandainya AST_REVIEW. Sebanyak 33 anggota duplikat tidak dipilih untuk modeling, tetapi tetap berada dalam master 381.

### Fase 03 — `03_Labeling/03_sentiment_labeling.ipynb` (15 cell)

**1 → 2 → 3 → 4 → [anotasi pilot] → 5 → 6 → [adjudikasi pilot] → 7 → 8 → 9 → [anotasi/review penuh] → 11 → 12 → [adjudikasi duplikat] → 14 → 15.**

| Cell | Fungsi dan checkpoint |
|---|---|
| 1–3 | Validasi input, codebook v1.0 dan tes konsistensi |
| 4 → jeda → 5 | Siapkan pilot 30, isi/review workbook, kemudian validasi |
| 6 → jeda → 7 | Siapkan adjudikasi 4 pilot, isi keputusan, kemudian rekonsiliasi |
| 8 | Codebook v1.1 hasil kalibrasi |
| 9 → jeda | Workbook penuh 381; 30 pilot terkunci, 351 sisanya menunggu pada tahap historis ini |
| 10 | Diagnostik status opsional; output arsip masih 130 selesai/251 pending, **bukan status final** |
| 11 | Audit progres; output arsip juga masih tahap 130/251. Lanjut ke 12 hanya setelah input memenuhi kelengkapan 381 |
| 12 → jeda → 14 | Siapkan lalu rekonsiliasi adjudikasi duplikat; empat baris ditinjau, dua label berubah |
| 13 | Diagnostik final label opsional sebelum 14; bukan handoff final |
| 15 | Audit dan handoff final 348; gunakan untuk screenshot hasil labeling fase 03 |

Artefak hybrid 130 locked/251 pending tidak memiliki producer cell lengkap di notebook ini; file prediksi yang tersedia hanya 10 baris. Jangan menambahkan “jalankan cell AI untuk 251 tweet” karena cell/log lengkap itu belum terbukti ada. Untuk melihat hasil akhir gunakan file final, tanpa menyimpulkan proses anotasinya seluruhnya manual atau AI.

Distribusi handoff fase 03: **223 NETRAL, 110 POSITIF, 15 NEGATIF**. Distribusi dataset modeling setelah adjudikasi fase 04: **225/108/15**. Jelaskan versi jika kedua screenshot ditampilkan.

### Fase 04 — `04_Modeling/04_modeling.ipynb` (38 cell)

| Urutan logika | Cell asli | Fungsi dan batas |
|---|---|---|
| 1 | **1 → 2 → 3** | Environment, preflight, siapkan review near-duplicate |
| 2 | Jeda → **4 → 5** | Isi review near-duplicate, validasi; siapkan adjudikasi label |
| 3 | Jeda → **6 → 8 → 9 → 10 → 11 → 12** | Isi keputusan label, rekonsiliasi, bentuk 337 leakage groups, kaji dan kunci split final SGKF 3-fold seed 123 |
| 4 | 7 | Diagnostik pair-key opsional, di sekitar grouping; bukan tahap training |
| 5 | **13 → 14 → 15** | Desain baseline, **training/evaluasi baseline pada 14**, lalu analisis kesalahan |
| 6 | **16 → 17 → 18 → 19 → 20** | Desain LSTM, cek runtime TensorFlow, isolasi tokenizer, forward/masking, protokol training. Pada output arsip 16, runtime masih HOLD; readiness berikutnya ada di 18/19 |
| 7 | **21: tahap training dengan masalah tersimpan** | Melatih tiga model, 15 epoch/fold, tetapi output arsip berakhir AssertionError saat pemeriksaan kesetaraan label/index. Tidak boleh dijanjikan sebagai cell yang selesai bersih di Colab |
| 8 | **22 → 23 → 24**, hanya konteks pemulihan sesi yang relevan | Diagnosis dan rekonsiliasi OOF, lalu validasi/ekspor final. Menggunakan variabel in-memory dari training; bukan rangkaian yang bisa dijalankan pada runtime kosong. Jika 21 sudah sukses menulis output pada eksperimen baru, 24 dapat menolak overwrite |
| 9 | **25 → 26 → 27 → 28 → 29 → 30 → 31 → 32 → 33 → 34** | Load hasil final dan buat sembilan grafik. Pada jalur membaca hasil, gunakan PNG yang sudah ada, tidak memanggil `savefig` kembali ke folder terkunci |
| 10 | **35 → 37** | Evaluasi komparatif dan laporan final |
| 11 | 36; 38 | Environment berulang sebelum laporan; ekspor PDF opsional. Keduanya bukan syarat untuk membaca gambar asli |

Untuk hasil LSTM yang digunakan di BAB IV, sumber akhirnya adalah **cell 24**, didukung **35 dan 37**, bukan screenshot error cell 21. Perbaikan agar training bisa diulang bersih di Colab memerlukan migrasi kode terpisah yang ditinjau; panduan ini mempertahankan source dan hasil terkunci.

Runtime historis yang tercatat: Python 3.12.15, TensorFlow 2.21.0, Keras 3.15.1; manifest training juga mencatat NumPy 2.5.4 dan pandas 3.0.6. Ini catatan lingkungan penelitian, **bukan jaminan bahwa versi tersebut tersedia atau kompatibel dengan runtime Colab saat ini**. Tidak ada instalasi versi atau uji training Colab dalam pekerjaan panduan ini.

### Fase 05 — `05_Temporal/05_temporal.ipynb` (6 cell)

**1 → 2 → 3 → 4 → 5**, dengan **6 opsional** untuk ekspor PDF.

1. Cell 1: cek sumber timestamp raw untuk 348 ID.
2. Cell 2: canonicalization dan kunci dataset temporal; harus memakai label dataset fase 04.
3. Cell 3: agregasi harian WIB, 20 hari kalender, 348 tweet.
4. Cell 4: menghasilkan delapan PNG; masing-masing kasus memiliki grafik jumlah dan persentase, ditambah relative-day dan komposisi antarkasus.
5. Cell 5: ringkasan/perbandingan temporal.
6. Cell 6: ekspor PDF yang sudah tersedia; opsional, bukan producer hasil sentimen.

Kalender aktual: Lombok 6–14 Agustus 2018, Palu 29 September–3 Oktober 2018, Sumatra 29 November–4 Desember 2025. Ini cakupan observasi yang tersedia, berbeda dari rentang konfigurasi query. Lima hari tanpa observasi tetap ada dalam kalender; persentasenya tidak didefinisikan. Grafik temporal memakai **label anotasi terkunci**, bukan prediksi LSTM.

### Fase 06 — `06_Result/06_result.ipynb` (6 cell)

Urutan pembentukan laporan: **1 → 2 → 3 → 4 → 5 → 6**.

| Cell | Isi |
|---|---|
| 1 | Integritas lintas fase, 348 ID dan 17 gambar |
| 2 | Tabel karakteristik dataset, metrik, kesalahan dan temporal |
| 3 | Seleksi 10 gambar utama dan 7 lampiran |
| 4 | Pemetaan pertanyaan penelitian dan empat isu metode |
| 5 | Laporan terintegrasi dan **urutan final sepuluh gambar** |
| 6 | Audit teknis dan ekspor PDF provisional |

Untuk BAB IV gunakan tabel/PNG yang sudah diseleksi. Semua generator ini menulis output dan memiliki perlindungan no-overwrite; membaca hasil tidak memerlukan menjalankannya kembali. Nomor gambar pada dokumen seleksi lebih awal berbeda dengan registry final; panduan ini mengikuti `final_main_figure_order_10.csv` dari cell 5.

### Fase 07 — `07_Documentation/07_documentation.ipynb` (5 cell pada commit sumber)

1. Cell 1: generator inventory/blueprint; output sudah tersedia.
2. Cell 2: generator preflight; output sudah tersedia dan snapshotnya historis.
3. Cell 3–5: baca keputusan cleanup, panduan diagnostik dan awal Part2; ketiganya Markdown.

Untuk pemeriksaan gunakan script `07_Documentation/scripts/verify_cleanup_lineage.py` atau V02/V19 pada notebook pendamping. Audit dokumentasi cocok sebagai bukti pendukung/lampiran; bukan grafik hasil utama BAB IV. Mengulang preflight saat ada notebook pendamping baru juga akan mengubah inventaris yang dipindai, sehingga tidak boleh dipresentasikan sebagai snapshot lama yang sama.

## 5. Cell mana yang perlu di-screenshot untuk proses BAB IV?

Tidak semua cell perlu difoto. Pilih **output yang menunjukkan keputusan dan hasil**, bukan tampilan kode panjang, path komputer, token, atau log percobaan gagal. Penempatan mengikuti pedoman kampus; tabel hasil idealnya diketik ulang sebagai tabel Word dengan sumber yang jelas.

| Tahap | Cell asli yang relevan | Area output yang diambil | Prioritas penulisan |
|---|---|---|---|
| Pengumpulan | Raw **41**, **45** | 65 task/1.508 raw/411 ID dan rekonsiliasi 381 INCLUDE/30 EXCLUDE | Ringkasan proses 4.1; dapat dijadikan tabel/alur |
| Cleaning | **3, 4, 7** | Satu contoh teks asli → semantic verified → linguistic, serta audit perubahan | Pilih contoh representatif; tidak perlu tiga screenshot penuh |
| Seleksi duplikat | Cleaning **10**, **11** | 327 unik + 21 perwakilan, 33 tidak dipilih, handoff 348 | Bukti jumlah dataset pada 4.1 |
| Labeling | Labeling **14**, **15** | Adjudikasi dan jumlah/distribusi label handoff fase 03 | Jelaskan versi; bukan distribusi final fase 04 |
| Label final modeling | Modeling **6**, **8** | Dua perubahan label, 348 observasi dan 337 leakage groups | Dataset final 4.1 dan pengaturan evaluasi 4.2 |
| Split | Modeling **12** | Tiga fold, 116 validasi/fold, grup terpisah dan kelas | 4.2; jangan menyebut independent test set |
| Arsitektur/protokol | Modeling **19**, **20** | Model summary, 168.419 parameter, sequence 128, 15 epoch, batch 16 | Pendukung metode/4.2 atau lampiran sesuai kampus |
| Evaluasi | Modeling **14**, **24**, **35** | Tabel OOF baseline, LSTM, metrik per kelas dan perbandingan | Tabel utama 4.3–4.4; gunakan artefak CSV final |
| Temporal | Temporal **2**, **3**, **5** | Timestamp valid, cakupan kasus/hari dan ringkasan harian | 4.5; utamakan tabel/grafik asli |
| Integrasi | Result **1**, **2**, **5** | Konsistensi 348 ID, tabel ringkasan dan urutan gambar | Cek angka saat menulis; screenshot audit dapat masuk lampiran |

Hindari sebagai bukti hasil final: Raw 46 (snapshot lama), Labeling 10/11 (arsip progres 130/251), Modeling 21 (error), Modeling 16 bila diartikan sebagai runtime final (arsip masih HOLD), serta notebook backup/pilot. Output tersebut tetap disimpan sebagai sejarah penelitian.

## 6. Sepuluh gambar utama BAB IV dan cell sumbernya

Untuk grafik, **masukkan PNG asli ke Word** agar sumbu, legenda dan ukuran huruf tetap jelas. Jika kampus meminta screenshot, tampilkan gambar pada cell viewer yang sesuai dan ambil area gambar lengkap. Pemilihan baseline vs LSTM masih berkaitan dengan isu batas proposal yang belum ditutup; penomoran gambar tetap provisional.

| Urutan final | Isi | Notebook/cell asli | Cell viewer | Bagian |
|---|---|---|---|---|
| Gambar 4.1 | Metrik OOF baseline vs LSTM | Modeling **30** | **V08** | 4.3 |
| Gambar 4.2 | Confusion matrix LSTM | Modeling **29** | **V09** | 4.3 |
| Gambar 4.3 | F1-score per kelas | Modeling **31** | **V10** | 4.3 |
| Gambar 4.4 | Jumlah tweet harian Lombok | Temporal **4** | **V11** | 4.5 |
| Gambar 4.5 | Jumlah tweet harian Palu | Temporal **4** | **V12** | 4.5 |
| Gambar 4.6 | Jumlah tweet harian Sumatra | Temporal **4** | **V13** | 4.5 |
| Gambar 4.7 | Persentase harian Lombok | Temporal **4** | **V14** | 4.5 |
| Gambar 4.8 | Persentase harian Palu | Temporal **4** | **V15** | 4.5 |
| Gambar 4.9 | Persentase harian Sumatra | Temporal **4** | **V16** | 4.5 |
| Gambar 4.10 | Komposisi sentimen tiga kasus | Temporal **4** | **V17** | 4.6 |

Seluruh path, caption, ID cell dan SHA gambar ada di `bab4_figure_cell_map.csv`. Source metrik utama: baseline accuracy **0,7040**, Macro-F1 **0,5236**; LSTM accuracy **0,5862**, Macro-F1 **0,4751**. Metrik ini adalah OOF, tidak sama dengan accuracy training. Jangan mengganti hasil tersebut dengan angka run Colab baru tanpa memperlakukan run itu sebagai hasil eksperimen berbeda.

## 7. Gambar lampiran

| Gambar | Cell asli |
|---|---|
| Training loss per fold | Modeling **26** |
| Training accuracy per fold | Modeling **27** |
| Macro-F1 per fold | Modeling **28** |
| Vocabulary size per fold | Modeling **32** |
| Distribusi jumlah token | Modeling **33** |
| Jumlah token menurut label | Modeling **34** |
| Volume tweet menurut hari relatif | Temporal **4**, file `07_relative_day_tweet_volume.png` |

Semua dapat ditampilkan dengan **V18**. Loss/accuracy training merupakan diagnostik, bukan metrik test. Hari relatif 0 berarti hari observasi pertama pada masing-masing kasus.

## 8. Bila benar-benar ingin mengulang proses di Colab

Pengulangan penuh harus menjadi pekerjaan migrasi tersendiri: (1) pertahankan source read-only dan buat workspace eksperimen, (2) gunakan satu konfigurasi ROOT Colab yang tidak ditimpa di setiap cell, (3) pisahkan input terkunci dari output baru, (4) tentukan representasi hash portabel tanpa mengubah bukti lama, (5) hubungkan checkpoint manual yang sudah direview, (6) perbaiki rekonsiliasi LSTM agar training dan ekspor menyelesaikan satu jalur bersih, (7) uji versi/runtime dan determinisme, (8) validasi hasil baru terhadap sumber dengan toleransi/metrik yang dijelaskan.

Jangan menyelesaikan error FileExistsError atau mismatch SHA dengan menghapus folder output, mengganti expected hash sembarang, atau menghapus assert. Pada snapshot penelitian yang lengkap, FileExistsError dapat menunjukkan bahwa artefak yang hendak dibuat sudah ada. Hasil baru harus memiliki identitas eksperimen dan audit terpisah.

## 9. Cakupan verifikasi panduan

Pemetaan cell dibuat dari source/ID asli pada commit sumber, mencakup 150 cell dari delapan notebook aktif/pilot; notebook backup tidak dijadikan jalur utama. Tujuh belas PNG cocok dengan registry SHA. Notebook pendamping diuji secara lokal terhadap salinan sumber terkunci tanpa menjalankan cell notebook penelitian. Uji tersebut tidak menggantikan uji langsung pada layanan Google Colab atau uji training baru. Koneksi Google Colab memerlukan unduhan publik GitHub pada V01 dan runtime yang menyediakan pandas/IPython.

Status akademik tetap PROVISIONAL. Empat isu metodologis dan gap provenance AI tetap terbuka. Panduan ini memberi cara membaca hasil yang tersedia dan peta proses, bukan menyatakan seluruh proses sudah portabel atau mendapat persetujuan akademik akhir.
