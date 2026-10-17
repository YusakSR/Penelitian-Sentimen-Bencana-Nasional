# Sentiment Labeling Codebook v1.1

Version: 1.1
Status: CALIBRATED_FOR_FULL_ANNOTATION
Source: Pilot 30 tweet, 4 keputusan adjudication

## 1. Tujuan

Mengklasifikasikan sikap penulis tweet terhadap
penetapan status bencana nasional untuk:
- Lombok 2018
- Palu 2018
- Sumatera 2025

Unit analisis utama adalah tweet dengan ID unik.

## 2. Target Sentimen

Objek penilaian adalah kebijakan penetapan
status bencana nasional.

Bukan sentimen umum terhadap:
- Bencana alam
- Korban bencana
- Bantuan kemanusiaan
- Pemerintah secara umum
- Partai politik atau tokoh politik

Kecuali pernyataan tersebut secara jelas
berkaitan dengan sikap terhadap penetapan status.

## 3. Kelas Sentimen

### POSITIF

Penulis secara jelas mendukung, menyetujui,
mendesak, atau menuntut penetapan status
bencana nasional.

Contoh ilustratif:
"Pemerintah harus segera menetapkan status
bencana nasional untuk Palu."

### NEGATIF

Penulis secara jelas menolak penetapan,
tidak menyetujui peningkatan status,
atau menyatakan status nasional tidak diperlukan.

Contoh ilustratif:
"Status bencana nasional tidak diperlukan."

### NETRAL

Penulis tidak memperlihatkan sikap
yang jelas terhadap penetapan status.

Termasuk:
- Laporan berita tanpa endorsement
- Kutipan pendapat orang lain
- Pertanyaan informatif
- Penjelasan pemerintah
- Informasi korban dan bantuan
- Kritik umum yang tidak menjelaskan sikap
  terhadap penetapan status

Contoh ilustratif:
"BNPB menjelaskan alasan status belum ditetapkan."

## 4. Aturan Keputusan Terstandardisasi

### R1 — Identifikasi objek
Pastikan opini mengarah ke penetapan status
bencana nasional, bukan sekadar peristiwa bencana.

### R2 — Identifikasi pemilik sikap
Pisahkan sikap penulis dari pernyataan pihak
ketiga yang diberitakan atau dikutip.

### R3 — Berita bukan otomatis dukungan
Judul seperti "PKS desak pemerintah menetapkan
status bencana nasional" diberi NETRAL apabila
hanya menyampaikan berita tanpa endorsement.

### R4 — Pertanyaan bukan otomatis dukungan
Pertanyaan tentang alasan atau proses penetapan
diberi NETRAL jika tidak menunjukkan tuntutan
atau penolakan yang jelas.

### R5 — Kritik pemerintah perlu konteks
Kritik terhadap pemerintah tidak otomatis POSITIF
atau NEGATIF. Tentukan apakah kritik tersebut
mendukung atau menolak penetapan.

### R6 — Kutipan dan repost
Kutipan dukungan atau penolakan pihak lain
tidak otomatis menjadi sikap penulis.
Cari komentar persetujuan atau penolakan yang jelas.

### R7 — Sindiran
Gunakan sikap tersirat hanya apabila maknanya
cukup jelas dari konteks lengkap. Jika tidak,
tandai untuk adjudication.

### R8 — Sikap campuran
Jika terdapat dukungan dan penolakan sekaligus
tanpa sikap dominan yang jelas, tandai AMBIGUOUS.

### R9 — Negasi
Perhatikan kata seperti tidak, belum, bukan,
tak, jangan, dan tidak perlu.
Kata "belum" saja bukan bukti penolakan.

### R10 — Konflik beberapa peristiwa
Jika tweet membahas beberapa bencana,
identifikasi sikap terhadap peristiwa target.
Apabila target dan sikap tidak jelas,
tandai AMBIGUOUS.

## 5. Alur Anotasi

1. Baca text_semantic_verified.
2. Periksa text_original jika konteks kurang jelas.
3. Identifikasi target penetapan.
4. Identifikasi pemilik sikap.
5. Tentukan POSITIF, NEGATIF, atau NETRAL.
6. Tulis alasan keputusan pada label_notes.
7. Untuk kasus tidak pasti, gunakan status AMBIGUOUS.
8. Selesaikan adjudication sebelum data final dikunci.

AMBIGUOUS adalah status review,
bukan kelas sentimen keempat.

## 6. Metadata Anotasi

Kolom yang perlu dicatat:
- sentiment_label
- annotation_status
- label_notes
- annotator
- labeled_at

Kolom sumber dan ID tidak boleh diubah.

## 7. Audit dan Konsistensi

- Satu ID memiliki satu label akhir.
- Tweet dengan teks identik perlu audit konsistensi.
- Keputusan reviewer harus terdokumentasi.
- Label modeling diturunkan berdasarkan ID.
- Jangan menggunakan prediksi model untuk
  menggantikan label manual.

## 8. Riwayat Kalibrasi

v1.0: aturan awal sebelum pilot.
v1.1: diperjelas setelah audit 30 tweet
dan adjudication terhadap 4 tweet ambigu.

Keempat keputusan adjudication mengubah
label menjadi NETRAL berdasarkan pemeriksaan
terhadap atribusi sikap dan konteks.

Distribusi pilot final:
- POSITIF: 8
- NEGATIF: 2
- NETRAL: 20

Distribusi pilot tidak digunakan untuk
mengestimasi proporsi sentimen keseluruhan.

## 9. Batasan

Pilot ini belum mengukur inter-annotator agreement.
Cohen's Kappa hanya dapat dihitung secara sah
jika ada anotasi independen dari dua anotator
terhadap item yang sama.

Codebook ini dapat digunakan untuk anotasi penuh,
dengan audit dan adjudication untuk kasus sulit.
