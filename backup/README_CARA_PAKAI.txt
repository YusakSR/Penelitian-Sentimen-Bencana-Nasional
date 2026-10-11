PATCH OFFLINE EVENT SCOPE V2 — full_scraping_raw_data.ipynb
Repository: YusakSR/Penelitian-Sentimen-Bencana-Nasional
Baseline diperiksa: commit 844e9260d785bffb7eefbacf341d803a5adbe7a5 (fix historis)

TUJUAN
- Mempertahankan kode dan seluruh CSV event_scope_v1_*.
- Memperbaiki pemisahan diskusi banjir/longsor Sumatra 2025 dan referensi Aceh 2004.
- Tidak mengubah DISASTER_CASES, kueri, task_key(), checkpoint, audit CSV lama, atau data mentah.
- Tidak memanggil API Apify / tidak menggunakan kredit.

PENEMPATAN DI NOTEBOOK
1. Biarkan Cell 06B dan Cell 11C V1 TANPA perubahan.
2. Sisipkan CODE CELL baru "06C" setelah Cell 06B (sebelum heading Langkah 4).
   Tempel semua isi Cell_06C_Event_Scope_V2.py.
3. Sisipkan CODE CELL baru "11D" setelah Cell 11C.
   Tempel semua isi Cell_11D_Event_Scope_V2_Report.py.
4. Opsional: tambah CODE CELL baru "11E" setelah Cell 11D.
   Tempel semua isi Cell_11E_Review_Evaluation.py.

URUTAN EKSEKUSI OFFLINE
- Pastikan Cell 04 masih EXECUTE_SCRAPING=False dan PAID_RUN_CONFIRMATION=''.
- Jalankan Cell 01, 02, 03, 04, 06, 06B, 06C, 07 (jika kernel baru).
  Cell 06C: EVENT SCOPE V2 TEST: PASS (12 kasus; tanpa Apify).
- Jalankan Cell 11C agar event_scope_v1_by_tweet.csv tersedia/terbarui.
- Jalankan Cell 11D.
- Tinjau event_scope_v2_manual_review.csv dan isi kolom manual_scope,
  manual_notes, reviewer, reviewed_at bila memang melakukan review.
- Setelah mengisi label, jalankan Cell 11E untuk tabel perbandingan.
- Simpan notebook dan semua laporan baru, kemudian commit dan push.

FILE BARU DI outputs/reports/
- event_scope_v2_by_tweet.csv (rekaman V1 dan V2 side-by-side, waktu sumber)
- event_scope_v2_by_case.csv (per kasus)
- event_scope_v2_transitions.csv (transisi label V1 -> V2)
- event_scope_v2_manual_review.csv (antrean review dan label manual; isian lama dipertahankan pada rerun)

DEFINISI MANUAL_SCOPE
- TARGET_CURRENT: secara substantif menyinggung keputusan status nasional untuk bencana target.
- TARGET_WITH_HISTORY: membahas bencana target dan membandingkan peristiwa historis.
- HISTORICAL_ONLY: merujuk peristiwa historis tanpa konteks substantif bencana target.
- NEEDS_REVIEW: teks/post tunggal tidak cukup; buka thread/tautan jika tersedia.

BATASAN
- Aturan V2 tetap heuristik, bukan pengganti anotasi manual atau label sentimen.
- Unit-test menggunakan CUPLIKAN yang dipersingkat dari sejumlah tweet terverifikasi ID-nya,
  ditambah contoh sintetik; ini bukan ukuran precision/recall dataset keseluruhan.
- Daftar review berisi seluruh perubahan V1/V2, semua HISTORICAL_ONLY dan NEEDS_REVIEW,
  serta sampel deterministik ~20% dari target yang tidak berubah.
- Akurasi yang dihitung dari antrean prioritas bukan estimasi akurasi global acak.
- Jangan gunakan status scope sebagai label sentimen mendukung/menolak.
