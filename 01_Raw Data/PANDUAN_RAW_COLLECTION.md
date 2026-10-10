# Panduan `raw_collection_v2.ipynb`

## Tujuan
Tahap 01 dari penelitian *Analisis Sentimen Temporal Masyarakat terhadap Kebijakan Penetapan Bencana Nasional di Indonesia pada Aplikasi X (Twitter)*. Notebook memuat tiga kasus (Lombok 2018, Palu 2018, Sumatra 2025) dan 42 query batch yang menggabungkan istilah peristiwa serta kebijakan. Raw disimpan apa adanya; cleaning final dilakukan pada Tahap 02.

## Instalasi / penempatan
1. Buat **salinan cadangan** `01_Raw Data/raw_collection.ipynb` dari repository GitHub sebelum menghapus isinya.
2. Salin `raw_collection_v2.ipynb` ke folder **`01_Raw Data`** (nama folder persis dengan spasi). Kamu boleh mengganti namanya menjadi `raw_collection.ipynb` setelah membuat backup.
3. Buka repository pada VS Code dan gunakan Python environment yang telah berisi `apify-client` dan `pandas`.
4. Jika paket belum terpasang pada Windows dengan Python terkelola `uv`, contoh instalasi:

   ```powershell
   uv venv .venv
   uv pip install --python .venv/Scripts/python.exe apify-client pandas ipykernel
   ```

   Pilih interpreter/kernel `.venv` pada VS Code. Jangan menginstal paket ke Python global yang `externally-managed`.
5. Jalankan notebook dari atas ke bawah. Default adalah **preview** dan **tidak** menjalankan Actor.

## Mode pilot (3 panggilan Actor maksimal)
Di cell **04 — MODE EKSEKUSI**:

```python
RUN_MODE = 'pilot'
EXECUTE_SCRAPING = True
MAX_NEW_RUNS = 3
PILOT_QUERY_LIMIT = 1
PILOT_HOURS = 24
ENABLE_ADAPTIVE = False
```

Jalankan semua cell mulai awal. Jika token belum tersedia sebagai variabel lingkungan `APIFY_API_TOKEN`, notebook akan memintanya secara tersembunyi. **Jangan cetak/commit token.**

Periksa `01_Raw Data/outputs/reports/collection_summary.csv`, terutama:
- `rows_real_in_window`
- `rows_event_and_policy_in_window`
- `quality_flags`
- contoh teks dan tanggal di `outputs/audit/<case>/*_audit.csv`

`BASIC_CHECKS_PASS` hanya berarti lolos validasi programatik, bukan jaminan relevansi secara semantik dan bukan kepastian seluruh tweet di X sudah tercakup. Bila `MOCK_PRESENT`, `OUT_OF_WINDOW`, atau `NO_POLICY_CANDIDATE`, evaluasi kueri/aktor dan jangan langsung lanjut full scraping.

## Mode full
**Hanya setelah pilot layak dan kredit Apify terpantau**:

```python
RUN_MODE = 'full'
EXECUTE_SCRAPING = True
MAX_NEW_RUNS = 3      # naikkan bertahap jika telah aman
FULL_WINDOW_HOURS = 24
ENABLE_ADAPTIVE = False
```

Rencana awal menggunakan 1.476 query-jendela harian tanpa split/retry: 9×34 Lombok + 9×34 Palu + 24×36 Sumatra. Jumlah panggilan riil dikendalikan `MAX_NEW_RUNS` per eksekusi dan checkpoint. Query dicoba bergiliran antarkasus, bukan menghabiskan seluruh kredit pada satu kasus terlebih dahulu.

Bila ada `POSSIBLE_TRUNCATION`, banyaknya tweet tidak dapat dipastikan hanya dari batas `maxItems`; pemeriksaan lebih lanjut dan pemecahan interval dapat diperlukan. `ENABLE_ADAPTIVE=True` memungkinkan split 24 jam → 6 jam → 1 jam → 15 menit tetapi jumlah run dapat naik drastis. Jangan aktifkan sebelum memeriksa pilot dan biaya.

## Output

```text
01_Raw Data/
├── raw_collection.ipynb
└── outputs/
    ├── raw_jsonl/<case>/<task_id>.jsonl    # seluruh keluaran Actor, termasuk mock
    ├── raw_csv/<case>/<task_id>.csv        # tabular raw (bila tidak kosong)
    ├── audit/<case>/<task_id>_audit.csv    # audit kualitas, bukan cleaned final
    ├── state/collection_checkpoint.jsonl  # penanda task dan run
    └── reports/collection_summary.csv     # ringkasan status dan kualitas
```

**Jangan menghapus checkpoint** untuk mencoba melanjutkan: notebook melewati task yang sudah tersimpan. Task yang gagal bisa dicoba pada eksekusi berikutnya. Bila kamu mengubah definisi query, perbarui `CONFIG_VERSION` agar task lama tidak dianggap sama. Jangan membagikan seluruh `outputs/` melalui GitHub publik tanpa memeriksa privasi pengguna X dan ketentuan penggunaan data.

Tambahkan ini pada `.gitignore` root repository:

```gitignore
01_Raw Data/outputs/
.env
.ipynb_checkpoints/
__pycache__/
```

## Keterbatasan yang harus dicatat untuk metodologi
- Hasil Actor bisa lebih banyak dari `maxItems` dan pencarian historis dapat tidak lengkap atau mengembalikan data tanggal lain.
- Tweet yang memuat **peristiwa + frasa kebijakan** hanyalah kandidat; opini atas kebijakan harus diverifikasi pada Tahap 02–03.
- Keyword generik (misalnya "pemerintah pusat") mungkin memerlukan penilaian konteks khusus.
- Interval tanpa hasil bukan bukti tidak adanya opini di X.
- Dataset raw dan hasil audit bukan dataset berlabel untuk LSTM.
