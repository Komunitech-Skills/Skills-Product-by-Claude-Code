# Uji A/B — Skenario S1 (Renovasi Toko), tanpa skill vs dengan skill

## Input pengguna (sama persis untuk kedua kondisi)
> Ringkas grup Renovasi Toko Nanda ini, aku Pak Nanda, tolong yang perlu aku tanggapi apa aja.
> (melampirkan file `renovasi-toko.txt`, 99 baris, format Android)

## A. TANPA skill (agent umum, tanpa membaca SKILL.md/script apa pun)
Cara kerja: agent generik hanya membaca file .txt secara langsung sebagai teks, lalu meringkas
"dengan pemahamannya sendiri" tanpa parser terstruktur, tanpa daftar tindakan wajib, tanpa
pemisahan Perlu Perhatian/Info/Obrolan yang konsisten format, dan tanpa penghitungan statistik
yang diverifikasi lewat kode.

```
Oke, saya baca chatnya. Ringkasan grup renovasi toko selama 2 hari ini:

Progress renovasi berjalan lancar — bongkar dinding, pasang atap galvalum warna abu-abu, dan
sekarang masuk tahap plafon. Ada beberapa hal yang perlu Bapak tahu:

- Ada pembayaran ke supplier (Fajar) untuk semen dan keramik, sekitar Rp 12 jutaan, sudah di-DP
  sebagian dan katanya sisanya menyusul.
- Lantai dekat kasir sempat retak dan perlu di-cor ulang, ada biaya tambahan.
- Ada komplain dari tetangga soal debu, sudah ditangani dengan minta maaf dan aturan bersih-bersih.
- Sempat ada masalah listrik mati di hari kedua tapi sudah normal lagi.
- Tim menambahkan anggota baru bernama Ridho untuk bantu finishing.
- Beberapa pesan dihapus orang, dan ada foto-foto progress yang dikirim.

Secara umum semuanya berjalan sesuai rencana dan keputusan-keputusan sudah diambil. Semoga
membantu!
```

## B. DENGAN skill (SKILL.md + `scripts/parse_ekspor_wa.py`)
Lihat output lengkap di `examples/01-renovasi-toko.md`. Ringkasnya: parser membaca 99 pesan
terstruktur, memilah 11 butir Perlu Perhatian (per hari) dengan **kutipan asli + jam persis**,
daftar tindakan siapa-apa-tenggat dalam tabel, angka statistik dari kode (bukan tebakan) — dan
secara jujur menandai 2 item yang **belum benar-benar dijawab Pak Nanda** di chat (sisa
pembayaran Rp 6.250.000 dan budget material), yang di versi "tanpa skill" di atas malah salah
disimpulkan sebagai "sisanya menyusul" / "keputusan sudah diambil" — padahal faktanya file tidak
menunjukkan Pak Nanda menjawab.

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Nominal disebut presisi (Rp 6.250.000, Rp 800.000, dll) | Tidak (dibulatkan "Rp 12 jutaan", nominal lain hilang) | Ya, semua persis dan dicek ke sumber |
| Kutipan asli + jam per item Perlu Perhatian | Tidak ada sama sekali | Ada di setiap butir |
| Daftar tindakan siapa-apa-tenggat | Tidak ada (hanya narasi) | Tabel lengkap, item tak jelas ditandai ⚠️ |
| Deteksi hal yang BELUM dijawab pemilik | **Salah** — mengklaim "keputusan sudah diambil"/"sisanya menyusul" padahal belum ada konfirmasi Pak Nanda di chat (berisiko pembeli awam kecolongan transfer telat) | Benar — ditandai eksplisit ⚠️ "belum ada jawaban dari Anda" |
| Statistik (jumlah pesan, jam ramai, media/dihapus) | Tidak ada | Ada, dihitung skrip & diverifikasi independen |
| Pembagian per hari untuk grup 2 hari | Tidak (digabung jadi satu paragraf) | Ya, sesuai SKILL.md |
| Siap tempel/kirim langsung | Tidak, masih perlu ditulis ulang manual | Ya, format siap pakai |

**Kesimpulan:** hasil dengan skill jelas lebih baik dan lebih aman dipakai bisnis nyata — bukan
cuma soal format, tapi versi tanpa skill secara faktual **salah menyimpulkan** status pembayaran
yang sebenarnya masih menggantung, risiko nyata untuk pembeli (bisa terlambat bayar supplier atau
lupa follow up). Ini nilai tambah yang signifikan dan terukur.
