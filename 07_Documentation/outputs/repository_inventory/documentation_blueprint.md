# 07_DOCUMENTATION — BLUEPRINT

**Repository:** YusakSR/Penelitian-Sentimen-Bencana-Nasional

**Commit terkunci:** `ae5107c317eaee11a909251470be4b7503a6f9db`

**Status akademik:** PROVISIONAL

**Jumlah berkas terlacak:** 455

## 1. Prinsip Dokumentasi

Fase ini menjelaskan pipeline dan bukti penelitian
tanpa mengubah raw data, label, model, prediksi OOF,
grafik, atau laporan sumber.

Setiap part memakai input terkunci, audit SHA-256,
dan tidak menimpa output yang sudah diterbitkan.

## 2. Inventaris Repository

| Fase / kategori | Berkas |
|---|---:|
| 01_Collection | 251 |
| 02_Preprocessing | 11 |
| 03_Labeling | 33 |
| 04_Modeling | 89 |
| 05_Temporal | 26 |
| 06_Result | 29 |
| 07_Documentation | 1 |
| ROOT_OR_OTHER | 15 |

Daftar lengkap tersedia pada
`repository_inventory.csv`.

Inventaris ini merepresentasikan berkas terlacak
Git pada commit yang disebutkan di atas.
Berkas lokal belum terlacak tidak termasuk.

## 3. Rencana Part2–Part7

### Part2 — Data Provenance & Collection Documentation

Dokumentasikan aliran data dari pengumpulan,
pembersihan, deduplikasi, hingga 348 tweet
berlabel yang menjadi dataset penelitian.

Artefak:
- Data lineage
- Data dictionary
- Sampling and labeling documentation
- Provenance audit

### Part3 — Modeling & Temporal Reproducibility

Dokumentasikan:
- Python environment dan dependencies
- Seed dan SGKF 3-fold
- Tokenisasi dan training LSTM
- Baseline TF-IDF + Logistic Regression
- Prediksi OOF
- Agregasi tanggal WIB
- Sumber tabel dan grafik terkunci

Artefak:
- Reproducibility guide
- Configuration registry
- Source manifest
- Audit

### Part4 — Academic Methodology Alignment

Verifikasi kecocokan proposal, RM1–RM3,
dan implementasi.

Empat isu harus tetap terbuka kecuali terdapat
keputusan eksplisit dan terdokumentasi
dari pembimbing.

### Part5 — Figures, Tables & Reporting Guide

Susun katalog tabel, gambar, caption,
sumber bukti, dan pedoman editorial BAB IV.

### Part6 — End-to-End Repository Integrity Audit

Periksa rantai hash dan konsistensi artefak
tanpa melakukan retraining atau scraping ulang.

### Part7 — Final Documentation Handoff

Susun panduan repository, ringkasan pipeline,
manifest, serta paket penyerahan penelitian.

## 4. Gerbang Kualitas

- Semua artefak sumber harus dapat diverifikasi.
- Tidak ada penulisan ulang file sumber.
- Tidak ada angka atau rumusan masalah yang dikarang.
- Dataset penelitian tetap 348 tweet.
- Keempat isu metodologis tetap dilaporkan.
- PDF BAB IV tetap berstatus PROVISIONAL.
- Pemeriksaan visual PDF harus diselesaikan
  sebelum penyerahan akademik.
- Perubahan metode memerlukan persetujuan pembimbing.

## 5. Output Part1

- `repository_inventory.csv`
- `repository_inventory_summary.json`
- `documentation_blueprint.md`
- `part1_repository_inventory_audit.json`

**Tahap berikutnya:** Documentation Part2 —
Data Provenance & Collection Documentation.
