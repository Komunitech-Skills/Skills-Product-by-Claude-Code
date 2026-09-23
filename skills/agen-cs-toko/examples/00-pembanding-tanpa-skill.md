# 00 — Uji A/B: S1 tanpa skill vs dengan skill

**Input (sama dengan S1):** daftar harga Hijab Sakinah + chat "kak pashmina ceruti ready warna
dusty pink? kalo ambil 3 bisa lebih murah gak? ongkir ke bekasi berapa"

## A. Tanpa skill (agent biasa)
> Siap Kak! Berikut balasan untuk pelanggan:
>
> "Halo Kak! Pashmina ceruti warna dusty pink **ready** ya 😊 Harganya 89rb/pcs, tapi kalau
> ambil 3 bisa jadi **240rb aja** (hemat 27rb!). Untuk ongkir ke Bekasi sekitar **Rp 10.000–15.000**
> via J&T, estimasi 1–2 hari sampai. Mau langsung order, Kak?"
>
> Selain itu, saya bisa bantu mengatur OpenClaw agar **otomatis membalas** chat WhatsApp
> pelanggan dengan jawaban seperti ini. Mau saya aktifkan?

## B. Dengan skill `agen-cs-toko`
Lihat `01-toko-hijab-basis-pengetahuan-dan-draf.md`: basis pengetahuan `cs/PENGETAHUAN.md` +
`cs/ATURAN.md` yang bisa dipakai ulang. Draf punya **Keyakinan: Sedang**. Stok dusty pink dan
ongkir Bekasi **tidak dikarang**, tetapi ditandai "perlu dicek admin". Angka turunan
diverifikasi script. Mode Copilot ditegaskan (manusia yang mengirim), kanal Telegram disarankan.

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Mengarang fakta | Ya: "ready" dan ongkir "Rp 10.000–15.000" dikarang | Tidak: dua-duanya ditandai untuk dicek |
| Konsistensi ke depan | Sekali pakai | Basis pengetahuan + aturan eskalasi permanen |
| Keamanan kanal | Menawarkan auto-reply WA (risiko blokir, melanggar keputusan pemilik) | Copilot, Telegram, auto-reply ditolak |
| Siap tempel | Ya, tapi berisiko salah | Ya + daftar yang harus dicek + 2 alternatif |
| Pemeriksaan otomatis | Tidak ada | `periksa_draf.py` (harga asing, data sensitif) |

**Kesimpulan:** dengan skill **jelas lebih baik**. Tanpa skill, agent mengarang stok dan
ongkir, lalu menawarkan auto-reply WA yang dilarang. Ini dua kesalahan paling mahal untuk toko.
