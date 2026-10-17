# Uji 05 (Akun B, normal #3) — Admin Salah Kirim Broadcast Harga Lama ke Pelanggan

## Input pengguna
> "Admin kita salah kirim broadcast WA harga lama (belum naik) ke 200 kontak pelanggan pagi ini jam 08.00, padahal harga baru sudah berlaku dari kemarin. Ketahuan jam 08.20 pas ada 6 pelanggan langsung chat nanya kok harga beda pas checkout. Kita udah kirim broadcast susulan jam 08.30 buat klarifikasi harga yang benar. Belum ada yang terlanjur transaksi pakai harga lama. Nama usaha: Kedai Kopi Arasta."

## Output simulasi (mengikuti SKILL.md persis)

# Laporan Insiden: Broadcast WA Harga Lama Terkirim ke Pelanggan

**Tanggal kejadian:** [isi: tanggal] · **Ketahuan:** 08.20 · **Status:** Selesai (klarifikasi sudah dikirim)

## Kronologi
08.00 — Admin mengirim broadcast WA berisi daftar harga lama ke 200 kontak pelanggan.
08.20 — 6 pelanggan menanyakan perbedaan harga saat checkout; kesalahan diketahui.
08.30 — Broadcast susulan dikirim untuk mengklarifikasi harga yang benar (harga baru).

## Dampak
- Pelanggan terdampak: 200 kontak menerima broadcast salah, 6 di antaranya sempat bertanya
- Kerugian: Tidak ada transaksi yang terlanjur memakai harga lama (belum ada yang dirugikan secara nominal)
- Lainnya: [isi: potensi kebingungan pelanggan lain yang belum sempat bertanya]

## Akar Masalah (5 Kenapa)
1. Kenapa broadcast berisi harga lama? → Karena admin memakai template/daftar harga yang belum diperbarui saat mengirim.
2. Kenapa template belum diperbarui? → Karena tidak ada langkah memastikan template harga di-refresh setelah ada perubahan harga.
3. Kenapa langkah itu tidak ada? → Karena belum ada checklist "cek ulang isi sebelum broadcast" di proses kirim broadcast.
4. Kenapa checklist itu belum ada? → [isi: alasan, mis. broadcast baru mulai rutin dipakai/belum pernah jadi masalah sebelumnya]

**Akar masalah:** Belum ada langkah verifikasi isi (khususnya harga) sebelum broadcast dikirim ke seluruh kontak.

## Tindakan Cepat (sudah/sedang dilakukan)
- Mengirim broadcast susulan berisi klarifikasi harga yang benar
- Membalas 6 pelanggan yang bertanya dengan penjelasan harga yang benar

## Rencana Pencegahan
| Tindakan | Penanggung jawab | Tenggat |
|---|---|---|
| Tambahkan langkah cek ulang isi (harga, tanggal, promo) sebelum broadcast dikirim | Admin | [isi: tenggat] |
| Simpan satu sumber data harga resmi (bukan beberapa file/template tersebar) yang wajib dicek sebelum broadcast | [isi: penanggung jawab] | [isi: tenggat] |
| [isi: tindakan tambahan bila diperlukan, mis. jeda konfirmasi 2 orang sebelum broadcast besar] | [isi: penanggung jawab] | [isi: tenggat] |

## Draf Permintaan Maaf ke Pelanggan

**Versi lengkap (DM ke pelanggan yang bertanya):**

Halo Kak [Nama],

Mohon maaf, broadcast harga yang Kakak terima pagi ini keliru menampilkan harga lama akibat kesalahan pada sisi kami. Harga yang berlaku saat ini adalah [isi: daftar harga terbaru]. Kami sedang membenahi proses pengecekan sebelum mengirim broadcast agar tidak terulang.

Terima kasih sudah mengonfirmasi ke kami, Kak.
Kedai Kopi Arasta

**Versi pendek (broadcast klarifikasi — sudah dikirim, dicatat untuk arsip):**

Mohon maaf, broadcast harga pagi ini keliru (masih harga lama). Harga yang berlaku: [isi: daftar harga terbaru]. Terima kasih atas pengertiannya 🙏 — Kedai Kopi Arasta

## Ringkasan untuk Tim/Pemilik (WA)

*Insiden: Broadcast Harga Lama ke 200 Kontak*
Apa: Admin kirim broadcast harga lama, belum sesuai harga baru
Dampak: 6 pelanggan sempat tanya, tidak ada transaksi rugi
Status: Selesai, klarifikasi sudah dikirim 08.30
Pencegahan: Cek ulang isi sebelum broadcast — PJ: Admin, tenggat [isi]

## Catatan penguji
- Skenario ini **tidak** menyangkut data pribadi pelanggan (bukan kebocoran data, hanya kesalahan isi pesan) — skill dengan benar **tidak** memunculkan bagian "Kewajiban Pemberitahuan Data Pribadi". Ini menguji bahwa skill tidak over-triggering bagian UU PDP hanya karena ada kata "broadcast ke 200 kontak".
- Angka dampak nominal ("kerugian") ditulis apa adanya ("tidak ada transaksi yang terlanjur") karena memang tidak ada kerugian uang yang disebutkan pengguna — bukan dikarang jadi nol secara sembarangan, tapi disimpulkan wajar dari fakta "belum ada yang terlanjur transaksi pakai harga lama".
- Tidak menyalahkan admin sebagai pribadi; akar masalah diarahkan ke proses verifikasi sebelum broadcast.
- **Lulus.**

## Penyegaran v1.0.5 (2026-10-17)
> Output simulasi dan kesimpulan penguji (Lulus) **tidak diubah**. Menurut SKILL.md v1.0.5 bagian-bagian berikut kini ditulis berbeda:
- **Tindakan Cepat:** Sudah dilakukan (sesuai keterangan Anda): mengirim broadcast susulan jam 08.30 untuk klarifikasi harga yang benar. Butir "Membalas 6 pelanggan yang bertanya" **tidak** disebut pengguna, jadi pindah ke Disarankan (belum dilakukan): "Balas 6 pelanggan yang bertanya satu per satu: [isi: sudah/belum dibalas]".
- **5 Kenapa:** langkah 1 = admin mengirim broadcast harga lama (sesuai keterangan Anda). "Template/daftar harga belum diperbarui" dan "belum ada checklist cek ulang isi" tidak disebut pengguna, jadi ditandai `(dugaan, perlu dikonfirmasi)`. Akar masalah ditulis sebagai dugaan + pertanyaan konfirmasi (mis. "Daftar harga untuk broadcast disimpan di mana, dan sudah diganti saat harga naik kemarin?").
- **Dampak:** 200 kontak menerima harga lama; 6 sempat bertanya; 194 lainnya belum bertanya (200 − 6, dihitung ulang dengan Decimal 2026-10-17). Penerima broadcast susulan ditulis sesuai pesan; bila jumlahnya tidak disebut, tulis `[isi: jumlah penerima susulan]`.
- Broadcast susulan di sini memang tindakan pengguna (pesan awalnya juga broadcast ke kontak yang sama), jadi tidak bertentangan dengan aturan kanal; draf baru tetap ditujukan per orang untuk yang bertanya.
