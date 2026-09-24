# Skenario 4 (S4) — Input tidak lengkap/malas

## Input pengguna
> bikinin konten minggu depan

## Output agent (yang seharusnya terjadi, mengikuti SKILL.md §Input & §Langkah kerja 1)
```
Oke, sebelum aku buatkan, aku perlu tahu dulu usahamu apa (baru sekali ini aja, nanti dipakai terus
tiap minggu tanpa tanya ulang). Jawab santai, boleh singkat-singkat aja:

1. Nama usaha & produk/jasa utama apa yang mau didorong minggu ini?
2. Target pembelinya siapa dan di kota/wilayah mana?
3. Order/booking lewat mana (WA/DM/lainnya), dan platform yang dipakai jualan (IG/TikTok/FB/WA Status)?
4. Sanggup bikin berapa video pendek minggu ini (sisanya foto/Story aja)?
5. Ada izin resmi (BPOM/PIRT/halal/dll) yang BENAR-BENAR dimiliki? Ada klaim yang TIDAK boleh dipakai?

Kalau kamu buru-buru dan mau langsung jadi, bilang aja "pakai default" — aku isi asumsi wajar (usaha
umum, platform IG+TikTok+WA Status, nada santai-sopan, tanpa klaim BPOM/PIRT) dan kucatat semua asumsi
itu di akhir hasil supaya gampang dikoreksi.
```

## Variasi: pengguna balas "pakai default aja, cepetan"
```
Oke, aku pakai default berikut (nanti tinggal kamu koreksi bagian yang salah):
- Jenis usaha: usaha kecil umum (belum diketahui produk spesifik)
- Target pembeli: masyarakat umum sekitar
- Platform: Instagram + TikTok + WA Status
- Cara order: DM/WA (nomor belum diisi — CTA akan generik "hubungi kami")
- Video: 2-3 per minggu
- Tanpa klaim BPOM/PIRT/halal apa pun (karena belum dikonfirmasi)

⚠️ Karena nama usaha & produk belum diketahui, aku BELUM bisa membuat caption/hook yang spesifik dan
"siap tempel" — hasilnya akan generik dan kurang berguna. Supaya paket kontenmu benar-benar bisa
langsung dipakai, minimal aku perlu **nama usaha & produk utama** (poin 1). Bisa dikasih itu aja dulu?
Sisanya boleh aku asumsikan.
```

## Catatan penguji
**Bagus:**
- Skill mengikuti aturan CLAUDE.md "instan tapi powerful": tetap menawarkan jalur cepat ("pakai
  default") alih-alih memaksa wawancara panjang, sesuai §Input SKILL.md ("Pengguna ingin cepat → isi
  kolom kosong dengan asumsi wajar dan sebutkan di akhir").
- Pertanyaan wawancara dibatasi maksimal 5 dan dikirim dalam **satu pesan** (bukan tanya-jawab
  berulang), sesuai instruksi eksplisit SKILL.md.
- Ada penyeimbang yang baik: skill TIDAK asal comot default untuk field yang paling krusial (nama usaha
  & produk) karena tanpa itu, hasil justru jadi generik dan gagal memenuhi janji "siap tempel" —
  ini keputusan tepat karena kalau semua field pakai default termasuk nama usaha, hasilnya tidak akan
  "powerful" seperti dijanjikan README ("Powerful: hasil langsung siap pakai, bukan saran umum").

**Kurang / catatan:**
- **Cacat RINGAN:** SKILL.md tidak secara eksplisit menyatakan field mana yang **boleh** didefaultkan
  vs **tidak boleh** (nama usaha/produk). Penanganan di atas adalah interpretasi wajar penguji terhadap
  semangat instruksi ("isi kolom kosong dengan asumsi wajar" — tapi nama usaha bukan "kolom" yang masuk
  akal untuk diasumsikan), namun agent lain yang lebih literal terhadap instruksi bisa saja tetap
  memaksakan default untuk SEMUA field termasuk nama usaha (mis. "Usaha Kamu"), menghasilkan output
  generik yang gagal memenuhi janji "siap tempel". **Saran perbaikan konkret:** tambahkan di SKILL.md
  §Input, kalimat eksplisit seperti: "Nama usaha & produk utama TIDAK boleh didefaultkan (kosongkan/
  tanyakan ulang secara ringkas bila ini yang hilang) — field lain (target pembeli, nada, jam) boleh
  memakai asumsi wajar." Ini akan membuat perilaku antar-run lebih konsisten.
