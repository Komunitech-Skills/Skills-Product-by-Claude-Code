# 01 — Owner rumah makan 2 cabang, 55 karyawan, ingin laporan rutin

**Skenario:** S1 (normal). Persona member VIP terbanyak: pengusaha F&B skala 50+ orang, usia 50-an,
kendala "tidak tahu mulai dari mana" dan "tidak punya waktu". Semua jawaban wawancara sudah
ada di pesan pertama, jadi agent cukup merangkum (tidak bertanya ulang).

**Input pengguna (persis):**
> mulai karyawan AI dong. saya punya rumah makan 2 cabang (kemang & bekasi), karyawan 55 orang. yang paling nyita waktu: bikin laporan penjualan harian, laporan keuangan bulanan buat bank, sama ngecek stok bahan baku. saya biasa pakai telegram, laptop kantor nyala terus. data karyawan jangan sampai kemana2 ya

**Yang dijalankan agent (nyata, OpenClaw 2026.9.5, HOME uji terisolasi, skill v1.1.0):**
```bash
python3 ~/.openclaw/skills/karyawan-ai-mulai/scripts/peta_kebutuhan.py \
  --tugas "laporan penjualan harian" --tugas "laporan keuangan bulanan buat bank" \
  --tugas "ngecek stok bahan baku" --industri "rumah makan" --json
# → rekap-penjualan-csv, laporan-keuangan-emkm, balas-chat-cs (isian paket F&B);
#   "ngecek stok bahan baku" tanpa padanan (script tidak mengenali "ngecek"/"stok" saja)
# Agent mencocokkan manual ke tabel peta-skill.md (sumber kebenaran): baris
# "Catat stok/inventori" → buku-stok. balas-chat-cs diganti karena tidak diminta.
openclaw skills list --eligible          # rekap-penjualan-csv sudah ada
# [setelah pengguna menjawab "ya"; folder Starter Kit ditemukan di ~/Downloads/starter-kit-karyawan-ai/]
openclaw skills install ~/Downloads/starter-kit-karyawan-ai/laporan-keuangan-emkm --global
openclaw skills install ~/Downloads/starter-kit-karyawan-ai/buku-stok --global
openclaw skills info buku-stok            # ✓ Ready, Visible to model: yes
python3 ~/.openclaw/skills/rekap-penjualan-csv/scripts/rekap.py penjualan-contoh-resto.csv \
  --kolom-tanggal Tanggal --kolom-produk Menu --kolom-qty Qty --kolom-total Total
```
(Rekap dijalankan pada **data contoh fiktif** 84 baris, 15–21 Sep 2026, 6 menu, 2 cabang.)

---

## Output

## Ringkasan Anda
Bapak/Ibu pemilik rumah makan (F&B) dengan 2 cabang (Kemang & Bekasi) dan 55 karyawan. Tiga
pekerjaan yang paling menyita waktu: laporan penjualan harian, laporan keuangan bulanan untuk
bank, dan pengecekan stok bahan baku. Kanal favorit Telegram, laptop kantor menyala terus
(cocok untuk laporan otomatis nanti). Anda minta data karyawan tidak keluar ke mana-mana.
Kalau ada yang salah tangkap, silakan koreksi.

## Rekomendasi Paket Kerja Pertama
1. **rekap-penjualan-csv**: kirim file ekspor kasir, langsung jadi rekap omzet, menu terlaris, dan tren harian.
2. **laporan-keuangan-emkm**: dari buku kas, jadi Laba Rugi + Neraca format SAK EMKM, bentuk yang umum diminta bank.
3. **buku-stok**: buku stok lokal untuk bahan baku: barang masuk/keluar, stock opname, dan daftar stok menipis.

Saran untuk 2 cabang: simpan data **per cabang** (satu file/folder ekspor kasir dan stok per
cabang), supaya rekap dan stok tidak tercampur.

Ide otomasi lanjutan (opsional, bisa nanti): rekap omzet kemarin per cabang dikirim otomatis ke
**Telegram** Anda setiap pagi jam 07.00 lewat skill `laporan-otomatis-terjadwal`. Laptop kantor
menyala terus, jadi ini bisa jalan.

## Status Pemasangan
- Sudah terpasang: rekap-penjualan-csv
- Perlu dipasang: laporan-keuangan-emkm, buku-stok → **Saya akan pasang 2 skill ini dari folder
  Starter Kit di `~/Downloads/starter-kit-karyawan-ai/` ke folder skill OpenClaw Anda
  (`~/.openclaw/skills`). Lanjut? (ya/tidak)**

*[Pengguna: "ya"]*

Selesai: `laporan-keuangan-emkm` dan `buku-stok` sudah terpasang (dicek dengan `openclaw skills info`: Ready). Skill baru akan terbaca
mulai pesan berikutnya.

## Hasil Tugas Pertama
Anda belum mengirim file penjualan, jadi saya coba dulu dengan **data contoh** (fiktif, 1 minggu,
2 cabang). Nanti tinggal kirim file ekspor kasir Anda sendiri, hasilnya persis seperti ini:

**Rekap Penjualan 15 – 21 September 2026 (DATA CONTOH)**

**Total omzet:** Rp 46.477.000
**Jumlah transaksi (baris):** 84
**Rata-rata omzet per hari:** Rp 6.639.571

| # | Menu | Qty | Omzet | % |
|---|---|---|---|---|
| 1 | Nasi Ayam Bakar | 358 | Rp 11.456.000 | 24,6% |
| 2 | Soto Betawi | 300 | Rp 10.500.000 | 22,6% |
| 3 | Mie Goreng Spesial | 280 | Rp 7.840.000 | 16,9% |
| 4 | Paket Keluarga | 53 | Rp 7.685.000 | 16,5% |
| 5 | Kopi Susu Gula Aren | 342 | Rp 6.156.000 | 13,2% |

Hari terbaik: Sabtu 19 Sep (Rp 8.763.000). Hari terendah: Senin 21 Sep (Rp 5.286.000).

Insight:
1. Dua menu utama (Nasi Ayam Bakar + Soto) = 47% omzet. Pastikan bahan dua menu ini tidak pernah kosong.
2. Sabtu–Minggu omzet 43–66% di atas Senin (Rp 7,5–8,8 juta vs Rp 5,3 juta). Jadwal shift dan belanja bahan bisa disesuaikan ke akhir pekan.
3. Es Teh Manis laku 355 gelas tapi omzetnya kecil (6%). Bisa dicoba paket "menu + es teh" untuk naikkan nilai per transaksi.

## Rencana 7 Hari
| Hari | Kebiasaan baru | Skill |
|---|---|---|
| 1 | Kirim file ekspor kasir kemarin, minta rekap singkat | rekap-penjualan-csv |
| 2 | Kumpulkan buku kas bulan lalu (Excel/foto) | — |
| 3 | Minta Laba Rugi + Neraca bulan lalu | laporan-keuangan-emkm |
| 4 | Rekap penjualan 1 minggu, bandingkan 2 cabang | rekap-penjualan-csv |
| 5 | Catat stok awal 10 bahan baku utama di cabang Kemang | buku-stok |
| 6 | Catat barang masuk dari supplier, lihat daftar stok menipis | buku-stok |
| 7 | Evaluasi. Kalau cocok, kita pasang laporan pagi otomatis ke Telegram | — |

## Privasi
Data Anda tetap di komputer Anda. File penjualan dan buku kas dibaca oleh OpenClaw di laptop
Anda sendiri. Isi yang diproses dikirim hanya ke penyedia model AI yang Anda pilih, tidak ke
Komunitech. Karena Anda menyebut data karyawan, saya sarankan cek privasi dasar (skill
`cek-privasi-openclaw`): siapa saja yang bisa chat ke AI Anda, dan apakah AI boleh menjalankan
perintah komputer tanpa izin. Mau saya jalankan sekarang, atau lain kali?

**Asumsi yang dipakai:** file kasir berupa CSV (Excel bisa disimpan sebagai CSV). Data contoh di
atas masih gabungan 2 cabang. Untuk data asli, kirim file per cabang.

---

## Catatan penguji (uji ulang v1.1.0)
- **Bagus:** alur lengkap, bahasa awam, rekomendasi 3 skill, saran per cabang (baru di v1.1.0),
  otomasi diarahkan ke Telegram + `laporan-otomatis-terjadwal`, dan folder Starter Kit dicari
  dulu sebelum install. Perintah `skills list --eligible`, `skills install <folder> --global`,
  `skills info` **terverifikasi jalan** di HOME uji baru. Angka rekap **diverifikasi independen**
  (total Rp 46.477.000, 5 menu teratas, hari terbaik/terendah cocok).
- **Kurang:** script v1.1.0 sudah memberi 3 rekomendasi, tapi frasa "ngecek stok bahan baku"
  tidak cocok ke `buku-stok` (`\bcek` tidak cocok dengan "ngecek", dan "stok" sendirian bukan
  kunci), jadi slot ketiga terisi `balas-chat-cs` yang tidak diminta. Agent harus mengoreksinya
  manual. Frasa "kirim laporan penjualan otomatis tiap pagi" juga cocok ke `rekap-penjualan-csv`,
  bukan `laporan-otomatis-terjadwal`. `buku-stok` dan `laporan-otomatis-terjadwal` masih berstatus
  **uji** di catalog.csv (belum rilis), padahal direkomendasikan seolah pasti ada di paket.
