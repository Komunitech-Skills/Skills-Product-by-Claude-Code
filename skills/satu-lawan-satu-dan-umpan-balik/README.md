# Ngomong ke Tim Tanpa Tidak Enak Hati

**Naskah ucapan dan pesan WA siap pakai untuk obrolan 1-on-1 (empat mata), teguran halus, karyawan baru, dan pengumuman perubahan.**

Diuji AI penguji independen di OpenClaw: 5,5 → 8,4 dari 10 (tanpa skill, saran umum yang ikut menyinggung masalah rumah tangga karyawan dan tanpa pesan WA ajakan; dengan skill, ada pesan ajakan, naskah empat mata berisi tanggal dan jam kejadian, serta usulan tanggal cek ulang).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Berani bicara, tetap hangat:** kalimat halus tapi jelas, bukan sindiran.
- ✅ **Agenda obrolan 1-on-1 30 menit** yang rutin dan tidak bertele-tele.
- ✅ **Rencana 30 hari untuk karyawan baru (onboarding)** dengan pesan sambutan dan titik cek.
- ✅ **Pengumuman perubahan** yang tidak bikin gaduh: yang terdampak dikabari dulu.
- ✅ **Ada batasnya:** skill menolak membantu pemutusan hubungan kerja (PHK) sepihak lewat WA dan mengarahkan ke jalur yang sah.

## Cocok untuk siapa
Pemilik/atasan UMKM dengan tim 3-20 orang. Bukan untuk memecat atau menghitung pesangon (lihat skill Surat Peringatan Karyawan dan konsultan hukum ketenagakerjaan). Melengkapi skill KPI Tim (target kinerja) dan skill SOP Onboarding (dokumen pembekalan karyawan baru); skill ini khusus untuk percakapan.

## Contoh sebelum & sesudah
**Permintaan:** "Si Rina kasir saya sering telat (09.40, 09.35, 09.50; toko buka 09.00). Dedi jadi sendirian, ada pelanggan pergi. Anaknya baik, kabarnya lagi ada masalah rumah. Saya nggak enak negur."

| Tanpa skill (uji OpenClaw, 12 Okt 2026) | Dengan skill (uji OpenClaw yang sama) |
|---|---|
| Saran umum "pisahkan empati dari ekspektasi kerja" dengan contoh kalimat. Naskahnya membuka dengan "kelihatan agak berat ya?" dan ikut menyinggung masalah di rumah yang hanya kabar orang lain. Tidak ada pesan WA ajakan siap kirim, dan cek ulang hanya "dua minggu ke depan" tanpa tanggal. | Langsung jadi: pesan WA ajakan bicara (terpisah dari teguran), naskah empat mata urut konteks → fakta tanggal & jam → dampak → tanya → sepakat (tiba 08.45, cek ulang Jumat 16 Okt sebagai usulan), langkah lanjut bertanggal. Kabar rumah tangga sengaja tidak dimasukkan; yang belum diketahui ditandai `[isian]`, 2 pertanyaan di akhir. |

Cuplikan keluaran nyata dengan skill (uji OpenClaw otomatis, v1.0.2, 12 Okt 2026, dipotong; `examples/01-teguran-kasir-terlambat.md`):

> **Pesan WA ajakan ngobrol (kirim dulu, jangan langsung tegur lewat WA):**
>
> "Rin, nanti setelah tutup bisa ngobrol 10 menit? Mau bahas soal jadwal masuk sebentar."
>
> **Naskah ngobrol empat mata (besok, bukan di depan Dedi/pelanggan):**
>
> "Rin, saya mau ngobrol soal jam masuk. Minggu ini kamu masuk jam 09.40 hari Senin (5 Okt), 09.35 hari Rabu (7 Okt), dan 09.50 hari Kamis (8 Okt) — padahal harusnya siap jam 08.45 sebelum toko buka jam 09.00.
>
> Akibatnya Dedi jadi pegang kasir sendirian pas lagi ramai, antreannya numpuk, dan kemarin sampai ada pelanggan yang pergi karena nunggu kelamaan.
>
> Dari sisi kamu sendiri, ada kendala apa sampai beberapa hari ini telat? [dengarkan dulu, jangan motong]
> …

## Cara pakai
Cukup ketik, misalnya:
- "Saya nggak enak negur kasir yang sering telat."
- "Buatkan agenda 1-on-1 30 menit dengan staf gudang saya."
- "Karyawan baru masuk Senin, bantu rencana 30 harinya."

## Instalasi
Salin folder `satu-lawan-satu-dan-umpan-balik` ke folder skills platform Anda. Lokasi untuk OpenClaw, Codex, Claude Code, dan Cursor ada di `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Tidak perlu akun atau API key.

**Hasil uji (angka nyata):** skor 1–10 penguji independen.
- Uji OpenClaw (uji otomatis agent, 12 Okt 2026, v1.0.2, 4 skenario): tanpa skill **5,5** → dengan skill **8,4** (lulus acuan kami). Sumber: `examples/HASIL-UJI.md` dan `examples/00-openclaw-sebelum-sesudah.md`.
- Uji simulasi agent sebelumnya (9 Okt 2026, bukan OpenClaw, 5 skenario; sisi tanpa dan dengan skill ditulis penguji yang sama, jadi condong ke skill): tanpa skill **6,2** → dengan skill **8,5**. Sumber: `examples/HASIL-UJI-simulasi-2026-10-09.md`.
- Hasil di bot Telegram asli ada di bagian berikutnya.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan bot Telegram uji. Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Uji terakhir: 12 Okt 2026, versi 1.0.2, di bot OpenClaw asli (grup uji internal Komunitech). Pesan yang sama dikirim dua kali, sekali tanpa skill dan sekali dengan skill: kasir bernama Rina sering terlambat (Senin 5 Okt masuk 09.40, Rabu 7 Okt 09.35, Kamis 8 Okt 09.50, padahal harus siap 08.45 dan toko buka 09.00), rekannya jadi sendirian di kasir dan ada pelanggan pergi, pemilik "nggak enak negur" dan minta dibuatkan apa yang harus diomongkan. Skor 1-10 dari penilai independen: tanpa skill **6** → dengan skill **8,5**, selisih **+2,5**: **lulus acuan kami** (dengan skill minimal 8 dan selisih minimal 1,5).

Bedanya yang terasa: tanpa skill jawabannya saran umum yang malah menyuruh menanyakan kabar masalah rumah tangga karyawan, tanpa pesan ajakan bicara dan tanpa tanggal tindak lanjut. Dengan skill langsung ada pesan WhatsApp ajakan bicara, naskah empat mata berisi hari dan jam keterlambatan yang benar, dampaknya ke rekan dan pelanggan, pertanyaan ke karyawan, serta tanggal cek ulang; kabar rumah tangga sengaja tidak diangkat.

Catatan jujur: uji ini baru satu skenario (teguran karyawan terlambat), dan tindak lanjut di jawaban hanya satu jalur (bila masih berulang baru naik ke teguran tertulis). Uji lain: uji OpenClaw otomatis 12 Okt 2026, 5,5 → 8,4 (lihat di atas).

## FAQ
**Apakah ini nasihat hukum?**
Bukan. Skill ini alat bantu menyiapkan naskah bicara; untuk PHK dan sengketa, konsultasikan ke ahli ketenagakerjaan.

**Kalau saya minta pecat lewat WA?**
Ditolak singkat; Anda tetap dibantu pesan ajakan bicara, naskah empat mata, dan format catatan kejadian (versi 1.0.2).

**Boleh dipakai untuk menegur lewat WA?**
WA hanya untuk mengajak bicara; teguran inti disampaikan empat mata.

**Perlu instal apa-apa?**
Tidak perlu program tambahan: cukup salin folder skill ke AI agent Anda (lihat Instalasi), tanpa akun atau API key dari Komunitech. Langganan AI agent-nya tetap Anda tanggung sendiri.

## Catatan
Bukan nasihat hukum; naskah ini alat bantu bicara, bukan pengganti ahli ketenagakerjaan. Skill ini menyiapkan naskah; Anda yang menyampaikannya. Diadaptasi dan diubah dari ide "Manager's Playbook" karya Kamal Sindi (CC BY 4.0); pembuat asli tidak mendukung hasil adaptasi ini. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
