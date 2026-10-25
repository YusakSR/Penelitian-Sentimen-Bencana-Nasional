# Safe Cleanup Plan — batch pertama

Baseline: `09391e6c5777a8c34edd8482a8bf3e2859f64408` (`Documentation Notebook Cleanup Preflight`).
Branch kerja: `docs/cleanup-lineage-phase01-03`.
Backup Git: `backup/pre-cleanup-20261025-09391e6`, menunjuk baseline yang sama.

Permintaan saat ini mengizinkan cleanup aman dan PR. Review sumber statis telah dilakukan; persetujuan manusia atas PR masih **PENDING**. Gate preflight yang melarang penghapusan, perpindahan, dan penggabungan cell sebelum persetujuan tetap berlaku.

## Tindakan per cell

`cleanup_decision_matrix.csv` adalah daftar lengkap 81 cell, dengan indeks asli, ID, SHA-256 sumber, tujuan, dependensi, alasan keputusan, dan tindakan berikutnya. Ringkasan:

| Disposisi | Cell | Tindakan batch ini |
|---|---:|---|
| KEEP_PIPELINE | 18 | Pertahankan di lokasi semula |
| KEEP_CONTEXT | 9 | Pertahankan konteks metode dan keselamatan |
| KEEP_HISTORICAL | 48 | Pertahankan seluruh notebook backup tanpa perubahan byte |
| DIAGNOSTIC_EXPLAINED | 4 | Jelaskan peran diagnostik melalui panduan baca |
| OPTIONAL_EXPLAINED | 2 | Jelaskan preview opsional melalui panduan baca |

## Controlled cleanup yang diterapkan

Tambahkan tiga cell **Markdown** pada akhir `07_Documentation/07_documentation.ipynb`: navigasi keputusan, penjelasan diagnostik/opsional, dan awal Part2. Seluruh dua cell lama beserta source, ID, metadata, output, dan execution count harus identik dengan baseline.

Panduan baca memisahkan penjelasan diagnostik dari jalur utama tanpa memindahkan cell penelitian. Seluruh sembilan notebook penelitian/backup, semua raw, checkpoint, label, workbook review, dataset, model, OOF, gambar, dan laporan sumber tetap identik dengan Git baseline. Tidak ada metadata penelitian yang ditulis ulang. Penandaan dilakukan dalam dokumentasi pendamping.

Indeks asli tidak berubah. Tidak ada cell yang dihapus, digabung, diurutkan ulang, atau dijalankan. Tidak ada scraping, training, pemasangan library penelitian, panggilan AI, atau perubahan default API. Kode preflight lama tetap sebagai bukti historis.

## Diagnostik dan opsional

| Notebook | Cell asli | Penjelasan dan batas |
|---|---:|---|
| `01_Raw Data/full_scraping_raw_data.ipynb` | 17 | Riwayat biaya; `CHECK_HISTORICAL_COSTS=False`. Jika diaktifkan, dapat membaca metadata remote. Pertahankan default dan posisi. |
| `01_Raw Data/full_scraping_raw_data.ipynb` | 47 | Definisi helper preview raw tersimpan; tidak dipanggil oleh cell ini. Bukan labeling atau bukti representativitas. |
| `01_Raw Data/raw_collection.ipynb` | 20 | Preview kandidat otomatis dari audit lokal; mengisi `SAMPLE_TWEETS`, tanpa consumer berikutnya yang ditemukan. Bukan label final. |
| `03_Labeling/03_sentiment_labeling.ipynb` | 10 | Tampilan ketidaksesuaian label/status workbook; pertahankan global/import dan posisi. |
| `04_Modeling/04_modeling.ipynb` | 22 | Diagnosis label/index OOF; pertahankan di dekat rekonsiliasi Part18 dan hasil tersimpan. |
| `04_Modeling/04_modeling.ipynb` | 36 | Pemeriksaan environment berulang sebelum Part20; import membantu menjalankan bagian laporan secara terpisah. |

## Verifikasi sebelum PR

1. Cocokkan persis seluruh 238 sumber cell dan ID dengan inventaris preflight; cocokkan 81 kandidat tanpa cell yang hilang atau ganda.
2. Parse sumber Python langsung, tanpa menjalankan cell. Sembilan AST_REVIEW lama lolos parser; filter magic lama salah mengganti baris lanjutan yang diawali `!=` atau `%`. Graph baru tetap perkiraan statis, bukan bukti runtime.
3. Verifikasi 464 file baseline dengan Git blob dan SHA-256. Hanya notebook dokumentasi yang boleh berubah, dengan perubahan append Markdown saja. `source_integrity.csv` mencatat SHA sebelum/sesudah.
4. Periksa hash historis terpisah dalam `historical_sha_checks.csv`. Status rekonstruksi CRLF **bukan** kecocokan byte asli. Rekonstruksi hanya di memori; tidak ada normalisasi file sumber.
5. Rekonsiliasi 348 observasi ke raw JSONL, ID/case, text/hash, seleksi duplikat, dan dua versi label fase 03/04. Pertahankan empat isu metodologis dan status PROVISIONAL.
6. Jalankan `python 07_Documentation/scripts/verify_cleanup_lineage.py`. Perintah ini hanya membaca bukti dan mencetak laporan; tidak menjalankan notebook atau menulis output penelitian.

## Tahap yang memerlukan persetujuan berikutnya

Pemindahan diagnostik fisik, penghapusan import berulang, penggabungan helper, perbaikan kode preflight, serta refactor path hard-coded memerlukan proposal terpisah setelah PR ini ditinjau. Tidak ada rekomendasi hapus pada batch ini. Jika kelak disetujui, pekerjaan dilakukan di branch baru dan tetap mempertahankan snapshot serta audit artefak sumber.

PR ini tidak boleh di-merge ke main tanpa persetujuan pengguna. Tidak ada auto-merge.
