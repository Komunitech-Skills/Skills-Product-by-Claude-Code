---
name: klon-diri-konten
description: Panduan aman membuat konten talking-head dengan avatar/suara AI DIRI SENDIRI (atau orang yang setuju tertulis) tanpa shooting berulang - checklist persetujuan + formulir, pilih alat (HeyGen, ElevenLabs, CapCut, D-ID, Synthesia vs open-source lokal), panduan rekam sampel + naskah latihan Indonesia, alur konten bulanan, hitung menit/kredit dan biaya Rupiah, label AI, keamanan dan langkah jika ditiru. Use for AI avatar, voice clone of myself, digital twin, talking head, HeyGen/ElevenLabs/CapCut, consent form, AI disclosure, content without filming. Bukan untuk meniru orang lain.
---

# Klon Diri untuk Konten (avatar & suara sendiri)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu pemilik usaha/kreator memakai wajah dan suara **dirinya sendiri** versi AI untuk video bicara ke kamera, tanpa shooting tiap kali. Skill ini menghasilkan: keputusan alat, formulir persetujuan, panduan rekam sampel, rencana bulanan, dan hitungan biaya. Skill **tidak** membuat klon, tidak memasang software, tidak butuh API key, dan tidak memposting apa pun.

## Kapan Dipakai / Tidak
Pakai: "mau bikin avatar/suara AI diri sendiri", "pilih HeyGen atau ElevenLabs", "buat surat izin talent/staf", "rencana konten bulanan pakai avatar", "cukup tidak paket ini untuk 12 video".
Tolak dengan sopan (tawarkan jalur aman):
- Meniru wajah/suara **orang lain tanpa izin tertulis** (artis, tokoh, pesaing, mantan karyawan, kenalan, orang yang sudah meninggal). Alternatif: avatar/suara bawaan alat, atau minta izin tertulis dengan formulir.
- Testimoni palsu, endorsement yang tidak pernah diucapkan pemilik, klaim kesehatan/keuangan menyesatkan, konten politik/kampanye, penipuan, menyamar sebagai orang/lembaga lain.
- Menyembunyikan label AI atau membuat klon tampak seperti rekaman asli agar menipu.
- Menjalankan/memasang model klon lokal (GPT-SoVITS, F5-TTS dsb.) untuk pembeli awam: hanya dijelaskan di `references/pilihan-alat.md`, tidak dipandu langkah instalasi.
- Membuat naskah lengkap per video: serahkan ke skill `studio-video-pendek-ai` (lihat langkah 5).

## Input
Tanyakan **sekali** dalam satu pesan, hanya yang belum diketahui:
1. Untuk siapa klon: diri sendiri, atau staf/talent (perlu izin tertulis)?
2. Kebutuhan: wajah+suara, atau suara saja? Bahasa Indonesia saja atau juga bahasa lain?
3. Jumlah video per bulan dan durasi rata-rata; anggaran per bulan (Rp).
4. Sudah punya akun alat mana? HP/laptop apa? Ruang rekam tenang tersedia?
5. Platform tayang (TikTok/Reels/Shorts/YouTube/WA Status).
Jika pengguna ingin cepat: pakai default (1 orang = diri sendiri, wajah+suara, 8 video x 45 detik, TikTok+Reels, anggaran di bawah Rp500.000) dan **sebut asumsinya**.

## Langkah Kerja
1. **Gerbang persetujuan (wajib, sebelum apa pun).** Jalankan checklist di `references/persetujuan-dan-verifikasi.md`. Pemilik wajah/suara = pengguna? Jika untuk orang lain, wajib `templates/formulir-persetujuan-klon.md` terisi dan ditandatangani; jika belum, berhenti dan tawarkan draf formulir. Untuk pihak yang tidak hadir/tidak setuju: tolak.
2. **Pilih alat.** Baca `references/pilihan-alat.md` (harga bertanggal, kebijakan). Rekomendasi default untuk awam: SaaS berbayar, bukan open-source lokal (butuh GPU, instalasi rumit, sebagian bobot model non-komersial). Ringkasan jalur:
   - Suara saja: ElevenLabs (klon suara instan mulai paket Starter, klon profesional mulai Creator; dicek 2026-09-29).
   - Wajah+suara, pemula: HeyGen, atau Synthesia (cek dulu di halaman harga resmi apakah paketnya termasuk avatar pribadi; verifikasi persetujuan lebih ketat).
   - Edit + suara ringan dan bayar rupiah lewat app store: CapCut.
   Sebutkan harga **sebagai perkiraan bertanggal**, bukan janji, dan minta pengguna mengecek halaman resmi. Selalu tulis: skill ini tidak berafiliasi dengan merek yang disebut.
3. **Hitung kecukupan paket.** Minta pengguna mengisi tabel paket (nama, harga, batas menit/kredit, kredit per menit, mata uang) dari halaman harga resmi, lalu jalankan:
   `python3 scripts/rencana_konten_avatar.py --paket paket.json --video 12 --menit 0.75 --revisi 25 --kurs 16500 --anggaran 500000`
   (Windows: `python` atau `py`; format: `examples/contoh-paket.json`, isi dengan angka halaman resmi). Jika script tidak bisa dijalankan, hitung manual: menit = video x menit x (1 + revisi%); kredit = menit x kredit per menit; bandingkan dengan batas paket; biaya Rupiah = harga x kurs. Selalu sisakan cadangan revisi minimal 25%. **Aturan rekomendasi:** jangan pernah merekomendasikan paket berstatus `kurang` atau `lewat-anggaran`, atau paket yang tidak menyediakan fitur yang dibutuhkan (mis. avatar pribadi). Bila tidak ada yang muat, katakan terus terang dan tawarkan opsi (kurangi video/durasi/revisi, naikkan anggaran, rekam sebagian asli). Jangan mengarang paket atau angka.
4. **Panduan rekam sampel.** Ikuti `references/panduan-rekam-sampel.md` (cahaya, audio, latar, pengaturan HP) dan naskah latihan 2-5 menit Indonesia di `references/naskah-latihan-rekam.md`. Sarankan rekam ulang bila ada noise/gema/bayangan; kualitas sampel menentukan hasil.
5. **Alur konten bulanan** (`references/alur-bulanan.md`): rencana tema -> naskah lewat skill `studio-video-pendek-ai` (hook-isi-CTA, sulih suara) -> render avatar/suara di alat -> tinjau (lafal, angka, harga, klaim) -> beri **label AI** + kalimat pengungkapan di caption (`references/label-ai.md`, tercatat 2026-09-29; cek halaman resmi platform) -> unggah **manual**. Jangan janjikan atau klaim posting otomatis.
6. **Keamanan** (`references/keamanan-dan-penyalahgunaan.md`): 2FA, jangan bagikan akun, hapus sampel bila tak dipakai, cadangan formulir, dan langkah jika ditiru (lapor platform, bukti, UU ITE/PDP, arahkan ke ahli hukum).
7. **Serahkan hasil** sesuai Format Output.

## Format Output
Susun berurutan dan ringkas, siap tempel:
1. **Status persetujuan** (lolos/belum + yang kurang).
2. **Rekomendasi alat** (1 pilihan utama + 1 cadangan, alasan 2 kalimat, harga perkiraan + tanggal cek, catatan tidak berafiliasi).
3. **Hitungan paket** (keluaran script apa adanya + kesimpulan 1 kalimat).
4. **Rencana rekam sampel** (jadwal, perlengkapan, naskah latihan).
5. **Kalender konten bulan ini** (tabel: minggu, tema, durasi, ajakan bertindak) + perintah siap tempel ke `studio-video-pendek-ai`.
6. **Kalimat label AI** siap tempel untuk caption + centang platform.
7. **Peringatan keamanan** (maks. 3 butir paling relevan).

## Contoh
Input: "Saya pemilik toko hijab, mau video bicara pakai wajah AI saya sendiri, 12 video/bulan, anggaran Rp500 ribu."
Ringkas: gerbang persetujuan (diri sendiri: lolos, simpan catatan tanggal), rekomendasi HeyGen/CapCut/alat lain sesuai hitungan script, contoh label: "Video ini dibuat dengan bantuan AI; avatar dan suara adalah tiruan digital saya sendiri." Contoh lengkap: `examples/01-toko-hijab-12-video.md`.

## Batasan & Penanganan Error
- Harga, kuota, dan kebijakan alat berubah cepat: semua angka di `references/pilihan-alat.md` bertanggal **2026-09-29**; jangan menyajikannya sebagai harga pasti. Bila pengguna memberi angka terbaru, pakai angka pengguna.
- Data paket rusak/tidak masuk akal (harga negatif, batas 0, USD tanpa kurs): script berhenti dengan pesan GALAT; minta pengguna memperbaiki. Jangan menebak.
- Info kurang: bertanya sekali; jika tidak dijawab, pakai default dan sebut asumsinya.
- Bukan nasihat hukum. Iklan kesehatan/kosmetik (mis. klinik): jangan klaim hasil pasti, cocokkan dengan izin edar/aturan iklan yang berlaku dan konsultasikan ke ahli. UU ITE/UU PDP dijelaskan garis besar (tanggal cek 2026-09-29); arahkan ke advokat untuk kasus nyata.
- Kebijakan persetujuan HeyGen/CapCut belum terverifikasi lewat halaman resmi pada tanggal cek; minta pengguna membaca syarat penggunaan terbaru sebelum mengunggah wajah/suara.
- Tidak menyimpan atau meminta foto, rekaman, atau data identitas ke dalam percakapan; sampel diunggah langsung ke alat oleh pemiliknya.
