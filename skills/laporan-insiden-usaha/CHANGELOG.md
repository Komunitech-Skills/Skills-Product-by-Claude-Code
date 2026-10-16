# Riwayat perubahan — laporan-insiden-usaha

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-16)
Temuan uji bot Telegram asli gelombang 20 (DENGAN 1.0.4 dibatasi maks 5: klaim tanpa dasar). Perubahan di SKILL.md dan `references/panduan-5-kenapa.md`; logika perhitungan tidak berubah (skill tidak punya skrip):
- Tindakan cepat dipisah dua daftar: **Sudah dilakukan** hanya berisi tindakan yang disebut pengguna (kutip/parafrase); sisanya ke **Disarankan (belum dilakukan)** atau `[isi: ...]`. Status yang belum diketahui ditulis "belum ada kabar" (bukan "masih dalam penanganan"); hasil yang belum dikonfirmasi ditulis sesuai pesan ("sudah menghubungi kurir untuk membatalkan 25 pesanan; hasil pembatalan: [isi: ...]").
- Langkah "kenapa" dan akar masalah yang tidak disebut pengguna wajib bertanda `(dugaan, perlu dikonfirmasi)`; akar masalah ditulis sebagai hipotesis sampai pemilik mengonfirmasi, ditutup 1–2 pertanyaan konfirmasi. Contoh di `references/panduan-5-kenapa.md` disesuaikan. Dugaan tidak masuk draf maaf/ringkasan WA.
- Langkah 10 baru: cek konsistensi angka antarbagian sebelum mengirim (total terdampak = sudah komplain + belum komplain, dst.), satu fakta = satu kalimat.
- Kanal chat: bila jawaban > 4.000 karakter, pecah per bagian berjudul jelas atau lampirkan laporan lengkap + ringkasan di chat; tanpa menyebut jalur folder dan tanpa kata proses.

## Catatan revisi 1.0.4 (2026-10-15)
Verifikasi rujukan aturan C33 (`koordinasi/c33-verifikasi-aturan-2026-10-15.md` §2; butir opsional "README K3"):
- README: tambah catatan **Di luar cakupan** — kecelakaan kerja dilaporkan pemberi kerja ke BPJS Ketenagakerjaan dan Dinas Provinsi/unit pengawasan ketenagakerjaan setempat paling lama 2×24 jam (Permenaker 5/2021 Pasal 8 ayat 1–2; sumber: https://pasal.id/peraturan/permen/permenaker-no-5-tahun-2021, diakses 2026-10-15), bukan lewat laporan insiden skill ini.
- SKILL.md (Batasan → Di luar cakupan): pengalihan kecelakaan kerja kini menyebut rujukan yang sama dan melarang merujuk Permenaker 5/2018 (itu K3 lingkungan kerja, bukan tata cara lapor kecelakaan). Skill tetap tidak mengisi formulir K3 dan tidak memaksakan format laporan insiden untuk kecelakaan kerja.
- Klaim UU 27/2022 Pasal 46 (3×24 jam) tidak berubah (verifikasi C33: COCOK).

## Catatan revisi 1.0.3 (2026-10-13)
- Batasan di SKILL.md: aturan anti-karangan diperluas dari angka ke tindakan (tindakan yang "sudah dilakukan" hanya dari input pengguna; selebihnya `[isi: ...]`). Temuan audit contoh: `examples/01` memuat tindakan "menghubungi 15 pelanggan / membalas 5 komplain" yang tidak ada di input; kini diganti `[isian: tindakan yang sudah Anda lakukan]`. Logika langkah kerja tidak berubah.

## Catatan revisi 1.0.2 (2026-10-01)
Hasil uji sebelum/sesudah di OpenClaw (`examples/00-openclaw-sebelum-sesudah.md`):
- **Cabang khusus insiden data pribadi** (Langkah 6 + `references/insiden-data-pribadi.md`): fakta UU 27/2022 Pasal 46 ditulis jelas (tertulis, paling lambat 3×24 jam, ke subjek data & lembaga; isi minimal ayat 2), tenggat dihitung dari jam ketahuan, draf pemberitahuan per pelanggan terdampak, catatan untuk lembaga (bila kanal resmi tersedia, tanpa mengarang alamat). Ditandai PERLU REVIEW HUKUM.
- Bila pemilik ingin tidak memberi tahu pelanggan, skill mengoreksi dengan sopan (tanpa menakut-nakuti) dan status tetap "Masih ditangani".
- Hubungi proaktif **semua** yang terdampak, bukan hanya yang sudah komplain.
- Kanal permintaan maaf mengikuti asal pelanggan (chat marketplace per pesanan / WA pribadi), bukan broadcast/status WA.
