# Uji OpenClaw 01 — Balas chat pasien umum (jam buka, biaya, BPJS) — mode Copilot

Tanggal: 2026-10-01 · Agent: OpenClaw lokal, model router Komunitech (`ninerouter/komunitech`), sesi baru per sisi. SEBELUM = home `kosong-klinik` (tanpa skill), SESUDAH = home `sol-klinik` (paket skill klinik).

## Pesan member (identik di kedua sisi)

> Tolong siapkan balasan buat pasien ini ya, nanti aku yg kirim. Chat pasien: "Kak, klinik buka hari Minggu ga? Terus cabut gigi berapa ya biayanya, bisa pake BPJS ga?" Info klinik: Klinik Gigi Senyum Sehat, Jl. Melati 12 Bekasi. Buka Senin-Sabtu 09.00-20.00, Minggu tutup. Cabut gigi biasa Rp250.000-400.000 tergantung kondisi, harus diperiksa dokter dulu. Kami mitra BPJS, peserta yg faskes 1 nya terdaftar di sini bisa cabut gigi tanpa biaya sesuai ketentuan BPJS. Daftar lewat WA ini.

## SEBELUM (tanpa skill) — balasan utuh

> Halo Kak, terima kasih sudah menghubungi Klinik Gigi Senyum Sehat 😊
>
> Mohon maaf, klinik kami tutup setiap hari Minggu ya. Jam buka kami:
> Senin–Sabtu, pukul 09.00–20.00
>
> Untuk cabut gigi biasa, biayanya sekitar Rp250.000–Rp400.000, tergantung kondisi gigi. Tapi untuk kepastian biaya, giginya perlu diperiksa dulu sama dokter kami ya Kak.
>
> Soal BPJS, klinik kami memang mitra BPJS. Kalau Kakak peserta BPJS dan faskes 1-nya terdaftar di klinik kami, cabut giginya bisa gratis sesuai ketentuan BPJS.
>
> Kalau mau daftar atau tanya-tanya lebih lanjut, bisa langsung chat di WA ini ya Kak 🙏

## SESUDAH (dengan paket skill) — balasan utuh

> Siap, ini draf balasannya — tinggal kamu kirim:
>
> ---
> Halo Kak, terima kasih sudah menghubungi Klinik Gigi Senyum Sehat 🦷
>
> Mohon maaf, klinik kami tutup di hari Minggu ya. Jam buka kami Senin-Sabtu, pukul 09.00-20.00.
>
> Untuk cabut gigi biasa, biayanya sekitar Rp250.000 - Rp400.000, tergantung kondisi giginya — jadi perlu diperiksa dulu oleh dokter ya Kak biar tahu pasti biayanya.
>
> Soal BPJS, kami mitra BPJS kok. Kalau faskes 1 Kakak terdaftar di klinik kami, cabut gigi bisa tanpa biaya sesuai ketentuan BPJS yang berlaku.
>
> Kalau mau daftar, bisa langsung chat di nomor WA ini ya Kak, nanti kami bantu jadwalkan. 🙏
>
> ---
>
> Catatan buat kamu: isi balasan ini murni dari info yang kamu kasih (jam buka, kisaran biaya, aturan BPJS) — tidak ada yang aku karang. Siap dikirim langsung.

## Verifikasi & pemakaian skill

- SEBELUM: tidak ada tool. SESUDAH: membaca `edukasi-pasien-klinik/SKILL.md` (tools: `read`).
- Fakta: semua angka/jam berasal dari info klinik, kedua sisi tidak mengarang. Pencabutan gigi memang termasuk manfaat JKN di FKTP bila sesuai indikasi medis (sumber: halodoc.com/artikel/begini-cara-cabut-gigi-bisa-pakai-bpjs-secara-gratis; fkg.umsida.ac.id/cabut-gigi-dengan-bpjs-kesehatan). Kedua sisi tidak menyebut syarat "sesuai indikasi medis" & kartu JKN aktif — wajar karena tidak ada di info klinik, tapi idealnya ditandai sebagai hal yang bisa ditanyakan pasien.
- Kesalahan: tidak ada di kedua sisi.

## Nilai

| | Sebelum | Sesudah |
|---|---|---|
| Skor (1–10) | 8 | 8.5 |

SEBELUM 8: balasan sopan, akurat, langsung pakai. SESUDAH 8.5: isi hampir identik + dibingkai jelas sebagai draf yang dikirim admin + pernyataan "tidak ada yang aku karang". **Selisih kecil — jujur: untuk chat FAQ sederhana yang infonya sudah lengkap, model tanpa skill sudah bagus.** Skill tidak memberi nilai tambah berarti di sini (dan tidak memakai `agen-cs-toko` / basis pengetahuan karena belum dibuat).
