# Sentiment Labeling Codebook v1.0

## 1. Tujuan
Mengidentifikasi sikap penulis terhadap penetapan status
bencana nasional pada Lombok 2018, Palu 2018,
dan Sumatera 2025.

## 2. Unit Analisis
Satu postingan/tweet dengan tweet ID unik.

Setiap tweet diberi tepat satu label akhir.

## 3. Objek Sentimen
Kebijakan atau keputusan penetapan status bencana nasional.

Penilaian bukan didasarkan pada sentimen umum terhadap
bencana, korban, maupun pemerintah.

## 4. Kategori

### POSITIF
Dukungan, persetujuan, desakan, tuntutan, atau kritik
yang secara jelas mendukung penetapan status
bencana nasional.

### NEGATIF
Penolakan, ketidaksetujuan, atau pernyataan bahwa
penetapan status bencana nasional tidak diperlukan.

### NETRAL
Berita, laporan, pertanyaan informatif, kutipan tanpa
persetujuan penulis, atau unggahan tanpa sikap jelas
terhadap penetapan status bencana nasional.

## 5. Prinsip Anotasi
1. Utamakan maksud penulis, bukan hanya keyword.
2. Jangan samakan kesedihan akibat bencana dengan POSITIF.
3. Jangan samakan kritik kepada pemerintah dengan POSITIF
   kecuali terkait dukungan terhadap penetapan status.
4. Bedakan opini penulis dari kutipan atau laporan berita.
5. Pertanyaan retoris dinilai dari konteks.
6. Jika penulis mendukung sekaligus menolak dan sikap
   dominan tidak jelas, tandai untuk review.
7. Gunakan text_original dan text_semantic_verified
   untuk memahami konteks.
8. Jangan menggunakan label hasil prediksi model
   sebagai pengganti keputusan anotator.
9. Jangan mengubah teks sumber ketika memberikan label.
10. Label akhir hanya POSITIF, NEGATIF, atau NETRAL.

## 6. Status Review
PENDING: belum dianotasi.
LABELED: label telah diberikan.
AMBIGUOUS: membutuhkan adjudikasi.
ADJUDICATED: kasus telah diputuskan melalui review.

AMBIGUOUS bukan kelas sentimen keempat.

## 7. Contoh Ilustratif
- "Segera tetapkan Palu sebagai bencana nasional."
  Label: POSITIF

- "Tidak perlu menetapkan status bencana nasional."
  Label: NEGATIF

- "Pemerintah menjelaskan alasan status belum ditetapkan."
  Label: NETRAL

- "Mengapa Lombok belum menjadi bencana nasional?"
  Label: NETRAL jika pertanyaan informatif.
  Review apabila konteks mengisyaratkan desakan.

## 8. Konsistensi
- Satu ID harus memiliki satu label final.
- Konten identik perlu diperiksa konsistensinya.
- Label untuk kandidat modeling diturunkan dari ALL_381.
- Semua keputusan ambigu harus diselesaikan sebelum
  ekspor dataset final.

## 9. Versi
Version: 1.0
Status: DRAFT_FOR_PILOT
