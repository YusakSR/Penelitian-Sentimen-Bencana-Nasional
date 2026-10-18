# LAPORAN KOMPARATIF TEMPORAL SENTIMEN

**Penelitian:** Sentimen Penetapan Bencana Nasional

**Tahap:** Temporal Part5 — Comparative Findings & Interpretation

**Tanggal laporan (UTC):** 2026-10-18T15:55:30.451390+00:00

**Sumber:** Agregasi Part3 dan delapan grafik Part4
yang telah dikunci dan diaudit.

## 1. Pendahuluan dan Ruang Lingkup

Laporan ini menjelaskan distribusi temporal sentimen
terhadap penetapan status bencana nasional pada sampel
tweet terkait Lombok 2018, Palu 2018, dan Sumatera 2025.

Analisis menggunakan **348 tweet berlabel manusia**.
Tidak dilakukan pelatihan model, pengubahan label,
penambahan tweet, atau estimasi data yang hilang.

Hasil dilaporkan secara **deskriptif**, bukan sebagai
estimasi representatif opini seluruh masyarakat.

## 2. Metodologi Analisis Temporal

Timestamp publikasi tweet berasal dari `createdAt`
pada arsip raw, direkonsiliasi melalui ID tweet,
dan dikonversi dari UTC ke WIB (`Asia/Jakarta`).

Agregasi menggunakan satu hari kalender WIB dan
tiga kelas sentimen: NETRAL, POSITIF, NEGATIF.

Satu tweet dihitung tepat satu kali. Kalender tetap
mencakup hari tanpa observasi, tetapi persentase
pada hari tersebut tidak dihitung.

Hari relatif ke-0 didefinisikan sebagai hari pertama
jendela observasi kasus; **bukan hari pertama bencana**.

## 3. Distribusi Sentimen Antarkasus

| Kasus | Total | NETRAL | POSITIF | NEGATIF |
| --- | --- | --- | --- | --- |
| Lombok 2018 | 101 | 65 | 33 | 3 |
| Palu 2018 | 105 | 71 | 29 | 5 |
| Sumatera 2025 | 142 | 89 | 46 | 7 |
| **TOTAL** | 348 | 225 | 108 | 15 |

Secara keseluruhan, NETRAL mencakup
**64.66%** sampel,
POSITIF **31.03%**,
dan NEGATIF **4.31%**.

Kelas NETRAL mendominasi ketiga kasus, sementara
NEGATIF merupakan kelas paling sedikit.
Dengan hanya **15 tweet NEGATIF** pada seluruh
sampel, interpretasi persentase harian memerlukan
kehati-hatian, khususnya ketika jumlah tweet kecil.

![Komposisi sentimen keseluruhan berdasarkan kasus](../timeline_visualizations/08_sentiment_composition_by_case.png)

*Komposisi sentimen keseluruhan berdasarkan kasus.*

## 4. Cakupan Observasi Temporal

| Kasus | Hari kalender | Hari berisi tweet | Hari tanpa tweet |
| --- | --- | --- | --- |
| Lombok 2018 | 9 | 6 | 3 |
| Palu 2018 | 5 | 5 | 0 |
| Sumatera 2025 | 6 | 4 | 2 |

Terdapat **20 hari kalender kasus** dan
**15 hari dengan observasi tweet**, sehingga
terdapat **5 hari tanpa observasi**.

Hari kosong tidak dapat diartikan sebagai
tidak adanya diskusi publik.

## 5. Analisis Temporal Setiap Kasus

### Lombok 2018

Dalam sampel Lombok 2018, terdapat **101 tweet**
pada rentang **2018-08-06**
sampai **2018-08-14** (WIB).
Observasi tersedia pada **6 dari
9 hari kalender**.

Komposisi sentimen terdiri atas NETRAL
**65**
(64.36%),
POSITIF **33**
(32.67%),
dan NEGATIF **3**
(2.97%).

Volume sampel harian tertinggi berjumlah
**24 tweet**, tercatat
pada **2018-08-10**.
Jumlah tersebut merupakan
**23.76%** dari total
sampel kasus.

Tanggal tanpa observasi: **2018-08-07, 2018-08-08, 2018-08-09**.
Tanggal tanpa tweet tetap dipertahankan pada kalender
dan tidak diberi persentase sentimen.

![Jumlah tweet per hari — Lombok 2018](../timeline_visualizations/01_lombok_daily_counts.png)

*Jumlah tweet per hari — Lombok 2018.*

![Proporsi sentimen per hari — Lombok 2018](../timeline_visualizations/04_lombok_daily_percentage.png)

*Proporsi sentimen per hari — Lombok 2018.*
### Palu 2018

Dalam sampel Palu 2018, terdapat **105 tweet**
pada rentang **2018-09-29**
sampai **2018-10-03** (WIB).
Observasi tersedia pada **5 dari
5 hari kalender**.

Komposisi sentimen terdiri atas NETRAL
**71**
(67.62%),
POSITIF **29**
(27.62%),
dan NEGATIF **5**
(4.76%).

Volume sampel harian tertinggi berjumlah
**36 tweet**, tercatat
pada **2018-10-01**.
Jumlah tersebut merupakan
**34.29%** dari total
sampel kasus.

Tanggal tanpa observasi: **tidak ada**.
Tanggal tanpa tweet tetap dipertahankan pada kalender
dan tidak diberi persentase sentimen.

![Jumlah tweet per hari — Palu 2018](../timeline_visualizations/02_palu_daily_counts.png)

*Jumlah tweet per hari — Palu 2018.*

![Proporsi sentimen per hari — Palu 2018](../timeline_visualizations/05_palu_daily_percentage.png)

*Proporsi sentimen per hari — Palu 2018.*
### Sumatera 2025

Dalam sampel Sumatera 2025, terdapat **142 tweet**
pada rentang **2025-11-29**
sampai **2025-12-04** (WIB).
Observasi tersedia pada **4 dari
6 hari kalender**.

Komposisi sentimen terdiri atas NETRAL
**89**
(62.68%),
POSITIF **46**
(32.39%),
dan NEGATIF **7**
(4.93%).

Volume sampel harian tertinggi berjumlah
**54 tweet**, tercatat
pada **2025-12-03**.
Jumlah tersebut merupakan
**38.03%** dari total
sampel kasus.

Tanggal tanpa observasi: **2025-11-30, 2025-12-01**.
Tanggal tanpa tweet tetap dipertahankan pada kalender
dan tidak diberi persentase sentimen.

![Jumlah tweet per hari — Sumatera 2025](../timeline_visualizations/03_sumatra_daily_counts.png)

*Jumlah tweet per hari — Sumatera 2025.*

![Proporsi sentimen per hari — Sumatera 2025](../timeline_visualizations/06_sumatra_daily_percentage.png)

*Proporsi sentimen per hari — Sumatera 2025.*

## 6. Perbandingan Puncak Volume Sampel

| Kasus | Tanggal puncak WIB | Jumlah tweet | Persentase sampel kasus |
| --- | --- | --- | --- |
| Lombok 2018 | 2018-08-10 | 24 | 23.76% |
| Palu 2018 | 2018-10-01 | 36 | 34.29% |
| Sumatera 2025 | 2025-12-03 | 54 | 38.03% |

Perbedaan tanggal dan jumlah tweet puncak
mencerminkan karakteristik **sampel penelitian**.
Jumlah puncak yang lebih besar tidak otomatis
menunjukkan aktivitas masyarakat atau
intensitas opini yang lebih besar.

## 7. Perbandingan Hari Relatif Observasi

![Perbandingan volume harian berdasarkan hari relatif observasi](../timeline_visualizations/07_relative_day_tweet_volume.png)

*Perbandingan volume harian berdasarkan hari relatif observasi.*

Grafik ini menyelaraskan tiga kasus berdasarkan
hari pertama *observasi tweet*, bukan berdasarkan
tanggal terjadinya bencana ataupun tanggal keputusan
pemerintah.

Karena jendela observasi dan sebaran data berbeda,
grafik digunakan untuk membaca pola sampel,
bukan mengukur kesamaan respons publik secara kausal.

## 8. Temuan Penelitian

1. **NETRAL merupakan sentimen terbesar pada ketiga kasus.**
   Temuan ini berlaku pada tweet sampel yang telah diberi label.

2. **Komposisi sentimen berbeda antarkasus secara deskriptif.**
   Perbedaan tersebut tidak membuktikan adanya
   perbedaan opini populasi.

3. **Sebaran waktu pengamatan tidak merata.**
   Lombok memiliki tiga hari tanpa tweet,
   Sumatera dua hari, sedangkan Palu memiliki
   observasi pada seluruh lima hari kalender.

4. **Puncak volume sampel harian berbeda.**
   Puncak Lombok, Palu, dan Sumatera masing-masing
   24,
   36,
   dan 54
   tweet.

5. **Kelas NEGATIF sangat terbatas.**
   Fluktuasi persentase harian dapat dipengaruhi
   sejumlah kecil tweet.

## 9. Keterbatasan Penelitian

- Sampel terdiri atas 348 tweet dari arsip
  pengumpulan yang telah melalui cleaning dan labeling.
- Periode pengamatan antarkasus tidak sama panjang.
- Hari tanpa observasi tidak berarti aktivitas publik nol.
- Distribusi tweet yang terkumpul dapat dipengaruhi
  strategi scraping, kata kunci, dan seleksi data.
- Data tidak membuktikan hubungan kausal antara
  peristiwa atau keputusan pemerintah dan sentimen.
- Kelas NEGATIF hanya terdiri atas 15 tweet,
  sehingga analisis kelas minoritas berketidakpastian tinggi.
- Hari relatif belum diselaraskan terhadap tanggal
  kejadian bencana atau peristiwa kebijakan.
- Tidak terdapat klaim representasi populasi pengguna X.

## 10. Kesimpulan Temporal

Pada sampel penelitian, NETRAL menjadi sentimen
terbesar di Lombok 2018, Palu 2018, dan Sumatera 2025.
Pola volume serta proporsi sentimen bervariasi menurut
tanggal, dengan lima hari tanpa observasi yang
dipertahankan secara eksplisit.

Analisis ini mendukung pembahasan deskriptif
distribusi sentimen dalam waktu, tetapi
belum cukup untuk menyimpulkan perubahan
opini masyarakat secara umum atau akibat
langsung suatu keputusan kebijakan.

## 11. Kesiapan Integrasi Fase 06_Result

Artefak temporal Part2, Part3, Part4, dan Part5
dapat dijadikan masukan fase hasil penelitian.

Tahap pertama `06_Result` harus mengaudit
konsistensi lintas fase, memisahkan evaluasi
model dari analisis label manusia, serta
menyatukan batasan metodologis.

**Rekomendasi: GO untuk 06_Result Part1 —
Cross-Phase Integrity & Results Blueprint.**

## 12. Provenance

- Dataset temporal: `TEMPORAL_LABELED_348_V1`.
- Data agregasi: `daily_sentiment_counts_20_days.csv`.
- SHA-256 agregasi:
  `4e4e1fd9e8b4e25b1aef729905b81306dd55a0d8053a2b509cee5d8acf89df21`.
- Grafik: delapan PNG asli Part4.
- Seluruh sumber diperiksa tanpa modifikasi.
- Tidak dilakukan training ulang.
