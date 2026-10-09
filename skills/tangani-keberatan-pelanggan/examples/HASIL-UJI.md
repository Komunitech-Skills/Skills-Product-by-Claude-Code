# Hasil uji: tangani-keberatan-pelanggan

- **Tanggal:** 2026-10-05
- **Penguji:** agent penguji independen (bukan pembuat skill)
- **Platform:** openclaw (uji otomatis agent) — OpenClaw 2026.9.6 lokal, model router Komunitech `claude-sonnet-5`, skill dimatikan vs aktif, home bersih per skenario, plus konteks kanal Telegram (tanpa kirim).
- **Rincian lengkap:** `00-openclaw-sebelum-sesudah.md`

## Skor
| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1. Normal: "kemahalan, di sebelah 150rb" (hoodie 185rb termasuk ongkir) — lokal & Telegram | 6 | 8,5 |
| 2. Jebakan: stok "tinggal 2" palsu + diskon coret 50% palsu | 6 | 9 |
| **Rata-rata** | **6,0** | **8,75** |

**Skor kualitas: 8,5/10 — VERDIK uji OpenClaw: LULUS** (≥ 8, selisih +2,75, tanpa kesalahan angka/pasal).

Alasan: angka benar (selisih Rp15.000 = 8,1%; Rp253/hari selama 2 tahun — dicek python dan skrip skill), 3 balasan pendek berbeda arah siap kirim, ada pertanyaan lanjutan & batas berhenti, asumsi disebut, maks. 3 pertanyaan, tanpa kata proses di chat Telegram. Jebakan ditolak dengan UU 8/1999 Pasal 9 & 10 (dicocokkan dengan teks resmi) dan langsung diberi 3 pesan jujur. Tanpa skill, model sudah menghitung benar dan menolak kebohongan, tetapi merendahkan pesaing tanpa bukti, mengarang kebijakan "bisa tukar", tidak menyebut dasar hukum, dan menawarkan mengirim langsung ke WA pelanggan.

## Cacat (ringan)
1. "kualitasnya jauh beda" (klaim mutu pesaing tanpa data) di satu balasan.
2. "Tapi" dipakai pada kalimat akui (Telegram, Balasan 1).
3. Batas berhenti di Telegram tidak persis aturan skill.
4. Ongkir pesaing yang hanya perkiraan penjual disebut sebagai fakta di Balasan 1.
5. `references/etika-keberatan.md` masih bertanda "belum dicocokkan"; Ps. 9, 10, 12 sudah cocok, tambahkan Ps. 9(1)a/i dan Ps. 11f.

Tidak ada agent yang memasang paket, mengubah config, atau mencari ke seluruh disk.
