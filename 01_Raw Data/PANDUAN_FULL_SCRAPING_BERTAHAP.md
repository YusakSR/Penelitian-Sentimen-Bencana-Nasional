# Panduan Full Scraping Bertahap (versi sebelum panggilan berbayar)

Sumber penelitian: repository `YusakSR/Penelitian-Sentimen-Bencana-Nasional`, diperiksa dari commit `P8part2` (4b819eb...) dan notebook pipeline v2 yang mempertahankan query, actor, CONFIG_VERSION dan task-key yang sama. **File ini belum mengubah GitHub pengguna.**

## Apa yang sudah diperbaiki

- Default `RUN_MODE='full'` + `EXECUTE_SCRAPING=False`: aman jika `Run All` (tidak meminta token Apify).
- `FULL_WINDOW_HOURS=6`, `E01_P01` saja, 3 kasus (34 + 34 + 36 hari), **416 task**; bukan seluruh 42 batch, yang jika dijalankan pada jendela 6 jam akan menghasilkan 5.904 panggilan.
- Prioritas jam `[06, 12, 18, 00]` per hari, tetapi seluruh 4 rentang tetap diwakili pada rencana penuh.
- `MAX_NEW_RUNS=3`; `MAX_SESSION_SPEND_USD=0.12`; server API `max_items=20` dan `max_total_charge_usd=0.03` tiap run (cek tarif/dukungan Apify aktual).
- Kredit `$1.21` adalah **terpakai**, bukan saldo tersisa. `AVAILABLE_CREDIT_USD=None` mencegah panggilan berbayar sampai pengguna mengisi saldo tersisa terkini.
- `PAID_RUN_CONFIRMATION` harus disetel persis `I_APPROVE_PAID_FULL_SCRAPING` dan `EXECUTE_SCRAPING=True` untuk membuka gerbang.
- Checkpoint append-only, hash compatible dengan pilot, record `RESERVED` sebelum pemanggilan dan `NEEDS_REVIEW` ketika terjadi error untuk mencegah tagihan ganda.
- Pemeriksaan biaya historis nonaktif secara default.
- Test offline fake-Actor yang memeriksa pembatasan tingkat Apify API serta simpan checkpoint dalam temp folder.
- Laporan `full_coverage_grid.csv` (tanpa API) dan ID global unik untuk task FULL tersimpan.

## Sebelum produksi: seberapa penting?

**WAJIB (gratis, tanpa Actor):**
1. Cadangkan `raw_collection.ipynb` sebelumnya; verifikasi path `01_Raw Data`, actor ID, token disimpan via env/getpass (jangan commit token).
2. Jalankan semua cell dengan `EXECUTE_SCRAPING=False`; pastikan total tugas 416 (Lombok 136, Palu 136, Sumatra 144), preflight PASS, unit test offline PASS.
3. Pastikan `P8part2` tetap ada di checkpoint; cek hash `sumatra_2025_4f7c...` dan `sumatra_2025_92a73...` konsisten.
4. Lihat saldo **tersedia** di dashboard (bukan kredit terpakai 1.21), baca tarif Actor dan batas harian kredit; isi `AVAILABLE_CREDIT_USD` dari dashboard.
5. Pertahankan `MAX_NEW_RUNS=3`, konfirmasi per-run cap, budget sesi, dan cadangan saldo. Jangan aktivasi lewat `Run All`.

**TINGGI (batch berbayar pertama yang terkendali):**
- Baru setelah semua tes gratis lulus, jalankan **maksimal 3 call** sebagai smoke test produksi nyata; jangan jalankan 416 sekaligus.
- Bandingkan charge aktual yang tampil di dashboard dengan estimasi/usageTotalUsd; periksa propagasi flags, raw, checkpoint, dan apakah rerun melewati task tersimpan.
- Jika banyak mock pada tanggal awal, jangan langsung memperluas semua 42 query. Evaluasi distribusi waktu sebelum menggeser urutan pengerjaan.

**PENTING untuk riset, sebelum menyatakan dataset final:**
- Uji manual relevansi semantik sampel bertingkat menurut kasus/tanggal/jam; pisahkan opini kebijakan dari judul berita, promosi, pertanyaan netral, serta klaim berita belum terverifikasi.
- Pantau jumlah ID asli unik **global** dan luas cakupan tanggal. Jangan gunakan 6.000 raw sebagai kepastian 4.000–5.000 unik.
- Perhatikan kepatuhan platform X dan keamanan raw yang memuat nama pengguna atau metadata lain; pertimbangkan repo/data privat.

## Aktivasi dengan sengaja (di notebook yang telah diuji)

Pada Cell `04`:

```python
AVAILABLE_CREDIT_USD = Decimal('ISI_SALDO_TERSEDIA_SEBENARNYA')
PAID_RUN_CONFIRMATION = 'I_APPROVE_PAID_FULL_SCRAPING'
EXECUTE_SCRAPING = True
MAX_NEW_RUNS = 3
```

Ini **contoh**: masukkan angka saldo riil, jangan string placeholder. Lalu jalankan kembali Cell 04, seluruh definisi fungsi selanjutnya, dan terakhir gerbang Cell 10. Setelah batch pertama, kembalikan `EXECUTE_SCRAPING=False` dan periksa dashboard sebelum sesi berikutnya.

**Keterbatasan:** harga Actor dapat berubah, minimum charge dapat berlaku saat tidak ada hasil, dan `max_total_charge_usd` adalah cap per run (bukan saldo akun). Kontrol sesi menggunakan reservasi konservatif dari tiap cap. Jangan menganggap pengecekan di notebook dapat menghentikan penagihan dari sumber lain pada akun Apify.
