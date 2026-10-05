# Uji 01 — Warung makan sepi siang hari, modal ≤ Rp5 juta (skenario normal)

Penguji independen (Tahap 6), 2026-09-25. Agent membaca `SKILL.md` + `references/` + `templates/` lalu menjalankan sesi. Script dijalankan dari salinan skill di scratchpad (`uji-biu/brainstorming-ide-usaha/`). Jawaban pengguna disimulasikan secara wajar.

## Permintaan awal

> "Pak/Bu, warung makan saya ramai pagi sama malam, tapi jam 1 sampai jam 4 sore sepi banget. Ada ide produk baru buat naikin omzet? Modal paling 5 juta lah."

## Dialog (ringkas, sesuai alur SKILL.md)

**Agent (Langkah 0 — klasifikasi):** "Ini ide produk baru untuk usaha yang sudah jalan, dengan modal terbatas dan bisa dites minggu ini — saya proses sebagai **Jalur B (Perlu Diuji)**: saya tanya beberapa hal penting dulu, lalu kasih 2–3 pilihan ide dengan untung-ruginya. Kalau menurut Anda ini perubahan besar (mis. mau renovasi/tambah karyawan), bilang saja, nanti saya naikkan ke jalur yang lebih lengkap."

**Pengguna:** "Oke."

**Agent (B.1 — satu pertanyaan):** "Warungnya di dekat apa saja? (a) kantor/toko/bengkel, (b) sekolah/kampus, (c) perumahan, (d) jalan raya/lalu lintas kendaraan — boleh pilih lebih dari satu."

**Pengguna:** "A sama C. Ada deretan ruko, bengkel, sama kantor kelurahan. Belakangnya perumahan."

**Agent:** "Siapa yang jaga warung jam 1–4, dan menu andalan sekarang apa (plus kira-kira harga jual & modal bahan per porsi)?"

**Pengguna:** "Saya sama istri. Andalan nasi campur 15 ribu, modal bahannya sekitar 9 ribu. Jam segitu kami cuma nunggu."

**Agent:** "Ada yang sudah pernah dicoba untuk jam sepi itu? Dan ada momen tertentu yang mau dikejar (gajian, Lebaran, dll.) atau untuk sepanjang waktu?"

**Pengguna:** "Pernah diskon 10% jam siang, nggak ngaruh. Sepanjang waktu aja."

**Agent (B.2 — tulis ulang pemahaman):**

> **Yang Anda sebutkan:** warung makan, ramai pagi & malam, sepi 13.00–16.00; lokasi dekat ruko/bengkel/kantor kelurahan + perumahan; tenaga Anda berdua; nasi campur Rp15.000 (bahan ±Rp9.000); diskon 10% pernah dicoba & tidak berhasil; modal maks Rp5 juta; tidak mengejar momen khusus.
> **Asumsi saya (tolong koreksi):** tujuan = mengisi jam 13.00–16.00 dengan pemasukan tambahan tanpa menambah karyawan; berhasil = minimal 10 pesanan/transaksi tambahan per hari di jam sepi setelah 1 minggu, tanpa rugi.
>
> Betul begitu?

**Pengguna:** "Betul, target 10 sehari oke."

**Agent (B.3 — teknik: Pembalikan Masalah + SCAMPER "P" & "C"):**
- *Pembalikan masalah:* kenapa orang TIDAK datang jam 13–16? → sudah makan siang di tempat kerja / tidak sempat keluar (→ **antar ke mereka**); yang datang jam segitu bukan cari nasi, tapi minum/camilan (→ **produk sore**); diskon tidak ngaruh karena masalahnya bukan harga (→ jangan ulangi diskon).
- *P (alihkan kegunaan):* dapur & tenaga yang menganggur jam 13–16 dipakai untuk **pesanan nasi kotak** yang dimasak di jam sepi.
- *C (gabung):* minuman dingin + gorengan jadi **paket "ngopi sore"** untuk tukang bengkel/ojol.

**Agent (B.4 — 2–3 pendekatan, titik impas dihitung script):**

Perintah yang dijalankan (dari folder skill):
```
python3 scripts/skor_ide.py impas --modal 750000 --margin 6000
python3 scripts/skor_ide.py impas --modal 1500000 --margin 3000
python3 scripts/skor_ide.py impas --modal 1000000 --margin 7000
```
Keluaran asli (baris BEP): `125 unit`, `500 unit`, `143 unit`. Verifikasi independen: `ceil(750000/6000)=125`, `ceil(1500000/3000)=500`, `ceil(1000000/7000)=ceil(142,86)=143` — cocok.

| # | Pendekatan | Modal awal (perkiraan) | Margin/unit (asumsi, cek ulang) | Balik modal kasar | Risiko utama |
|---|---|---|---|---|---|
| 1 | **Pre-order makan siang antar** ke ruko/bengkel/kelurahan (pesan via WA s.d. jam 11, antar jam 12–13, sore tawarkan "menu sore" ke grup yang sama) | Rp750.000 (thinwall, stiker, cetak menu kecil, bensin minggu pertama) | Rp6.000 (harga Rp15.000 + ongkir Rp0 di radius 1 km; bahan Rp9.000) | 125 porsi ≈ 2–3 minggu jika 8 porsi/hari | Waktu antar bertabrakan dengan jam ramai; harus disiplin batas pesan |
| 2 | **Paket "ngopi sore"** (es teh/kopi susu + 2 gorengan) jam 13–17 | Rp1.500.000 (cooler box/dispenser, gelas cup, sealer tangan) | Rp3.000 | 500 paket ≈ 2 bulan jika 8/hari | Margin tipis; bersaing dengan penjual minuman keliling |
| 3 | **Nasi kotak pesanan** (rapat kelurahan, arisan, pengajian), dimasak di jam sepi, min. 20 kotak | Rp1.000.000 (stok kotak, cetak brosur, contoh gratis untuk 2 calon pemesan) | Rp7.000 | 143 kotak ≈ 7 pesanan × 20 kotak | Pesanan tidak rutin; perlu 1–2 langganan tetap dulu |

**Rekomendasi agent:** mulai dari **#1 Pre-order makan siang antar** — modal paling kecil, memakai menu yang sudah terbukti laku, dan langsung menjawab alasan utama pelanggan tidak datang (tidak sempat keluar). #3 cocok jadi pelengkap setelah punya daftar kontak kantor. Catatan: angka margin & perkiraan penjualan per hari adalah **asumsi** dari angka Anda, bukan data pasar.

**Agent (B.5 — gerbang persetujuan):** "Mau lanjut dengan #1 saja, atau #1 dan #3 berdampingan? Saya belum menyusun rencana ujinya sebelum Anda pilih."

**Pengguna:** "Yang nomor 1 dulu."

## Output akhir (Format Output Jalur B)

**1. Ringkasan pemahaman** — Isi jam sepi 13.00–16.00 / siang dengan pemasukan tambahan, tenaga berdua, modal maks Rp5 juta, target ≥10 pesanan tambahan/hari setelah 1 minggu tanpa rugi.

**2. Ide yang dipertimbangkan**

| Ide | Teknik sumber | Skor |
|---|---|---|
| Pre-order makan siang antar | Pembalikan masalah | tidak dihitung (Jalur B) |
| Paket "ngopi sore" | SCAMPER-C (gabung) | – |
| Nasi kotak pesanan | SCAMPER-P (alihkan kegunaan) | – |
| (dibuang) Diskon jam siang | – | sudah dicoba, gagal; masalahnya bukan harga |

**3. Ide terpilih** — Pre-order makan siang antar, karena modal kecil, menu sudah teruji, dan menyasar orang yang tidak sempat keluar kantor/bengkel.

**4. Rencana uji murah (MVP)** — sesuai `templates/kerangka-uji-murah.md`
- **Cara uji:** datangi langsung 15 ruko/bengkel/kantor kelurahan, bagikan menu kecil + nomor WA, catat yang mau masuk "grup pesan makan siang". Pesan s.d. 11.00, antar 12.00–13.00.
- **Durasi:** 7 hari (mulai Senin, evaluasi Minggu).
- **Target:** rata-rata ≥10 porsi antar/hari di hari 5–7, tanpa rugi (harga jual Rp15.000 ≥ bahan Rp9.000 + kemasan ±Rp1.000 + bensin).
- **Lanjut** jika target tercapai & tidak ada keluhan berulang. **Perbaiki** jika 6–9 porsi/hari (cek menu, jam antar). **Hentikan** jika < 3 porsi/hari.
- **Biaya uji maksimal:** Rp400.000 dari modal Rp750.000 (sisanya hanya dibelanjakan bila lanjut).

**5. Rencana Aksi 7 Hari**

| Hari | Tugas |
|---|---|
| 1 | Cetak 30 menu kecil (menu hari ini + cara pesan WA) & beli 50 thinwall |
| 2 | Datangi 15 ruko/bengkel/kelurahan, minta izin masukkan nomor ke grup/daftar siaran pesan |
| 3 | Kirim menu jam 09.00, tutup pesanan 11.00, antar 12.00–13.00; catat jumlah porsi |
| 4 | Ulangi; tanya 3 pemesan: apa yang kurang (porsi, jam antar, variasi) |
| 5 | Tambah 1 variasi menu yang diminta; catat porsi |
| 6 | Tawarkan ke 10 tempat baru di radius 1 km; catat porsi |
| 7 | Rekap rata-rata porsi/hari & biaya → putuskan lanjut, perbaiki, atau ganti ke ide #3 |

**6. Asumsi yang dipakai** — margin Rp6.000/porsi (dari harga & bahan yang Anda sebut, belum termasuk gas/listrik); perkiraan 8 porsi/hari untuk hitung balik modal adalah angka contoh, bukan data pasar.

## Catatan penguji
- Alur mengikuti SKILL.md: klasifikasi diumumkan, pemahaman ditulis ulang dan dikoreksi, 2–3 pendekatan + untung-rugi, gerbang persetujuan, MVP, aksi 7 hari. Tidak ada janji untung.
- Jalur B **tidak punya langkah skor tertimbang**; `impas` hanya disebut di C.8, tetapi dipakai di B.4 agar "balik modal kasar" dihitung (bukan dikira). SKILL.md sebaiknya menyebut `impas` juga boleh/wajib di B.4.
- Ambang "hentikan" di template (<30% target) meninggalkan celah 3–5 porsi/hari tanpa aturan.
- Dialog butuh 4 giliran tanya karena aturan "satu pertanyaan per pesan" (agent menggabungkan yang terkait).
