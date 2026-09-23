---
name: follow-up-prospek
description: Menyusun urutan pesan follow-up WhatsApp dan email untuk calon pembeli/klien yang belum membalas atau belum deal (H+1, H+3, H+7, H+14), sopan dan tidak memaksa, disesuaikan tahapnya (setelah kirim penawaran, setelah demo/meeting, setelah dijawab "nanti dulu", setelah tanya harga lalu hilang), lengkap dengan jadwal tanggal kirim dari script. Gunakan saat pengguna bilang prospek ghosting, klien belum balas, follow up penawaran, sales follow-up sequence, atau chasing a lead. Bukan untuk menagih pembayaran (pakai tagih-piutang) atau broadcast promo massal (pakai broadcast-wa).
---

# Follow-up Prospek

## Tujuan
Membantu penjual menindaklanjuti prospek yang diam tanpa terkesan mengejar-ngejar: tiap pesan membawa alasan baru untuk membalas, memudahkan prospek berkata "ya" **atau** "tidak", dan berhenti dengan sopan di akhir urutan. Hasilnya: urutan pesan siap kirim + tanggal kirimnya.

## Kapan digunakan
- "Sudah kirim penawaran ke Bu Rina 3 hari lalu, belum dibalas. Bikinin follow-up."
- "Habis demo aplikasi kasir ke resto, katanya mau diskusi internal, terus hilang."
- "Klien bilang 'nanti dulu ya, belum ada budget'. Gimana follow-up-nya?"
- "Banyak yang tanya harga di WA terus nggak balas lagi."

## Kapan TIDAK digunakan
- Pelanggan sudah beli tapi belum bayar / invoice lewat jatuh tempo → `tagih-piutang`.
- Kirim promo ke banyak kontak sekaligus → `broadcast-wa`.
- Jika skill rujukan di atas tidak terpasang, jelaskan singkat bedanya dan beri satu draf pesan netral saja (bukan urutan follow-up).
- Membalas pertanyaan/komplain pelanggan yang masuk → `balas-chat-cs`.
- Prospek sudah jelas menolak atau minta tidak dihubungi → jangan buat urutan; buat satu pesan penutup yang sopan saja (atau tidak mengirim apa pun).

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Tahap prospek: penawaran / demo-meeting / "nanti dulu" / tanya harga lalu hilang | Ya | Tebak dari cerita; sebutkan asumsi |
| Nama prospek (+ perusahaan, jabatan jika B2B) | Ya | `[Nama]` |
| Produk/jasa & nilai penawaran singkat | Ya | — (tanyakan) |
| Tanggal kontak terakhir (H+0) | Tidak | Hari ini |
| Saluran: WA, email, atau keduanya | Tidak | WA (B2C/UMKM); WA + email (B2B/korporat) |
| Hal baru yang bisa ditawarkan (testimoni, studi kasus, promo terbatas, sampel, stok baru) | Tidak | Tidak ada; pakai nilai tambah non-diskon (info, tips, jawaban keberatan) |
| Keberatan yang sudah terdengar (harga, waktu, atasan, budget) | Tidak | Tidak diketahui |
| Nama & gaya bahasa pengirim (formal/santai, Bapak/Ibu/Kak) | Tidak | Sopan semi-formal, "Bapak/Ibu" untuk B2B, "Kak" untuk B2C |
| Batas waktu promo/penawaran (jika ada) | Tidak | Tidak disebut |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat, pakai default dan tulis "Asumsi" di akhir.

## Langkah kerja
1. **Tentukan tahap & tujuan tiap pesan** memakai pola di bawah (detail & contoh lengkap per tahap: `references/urutan-per-tahap.md`).

   | Ke | Waktu | Tujuan | Isi utama |
   |---|---|---|---|
   | 1 | H+1 | Memastikan diterima | Cek sampai, tawarkan jawab pertanyaan, 1 pertanyaan mudah |
   | 2 | H+3 | Memberi nilai | Info baru: testimoni/foto/studi kasus/jawaban keberatan umum |
   | 3 | H+7 | Memudahkan keputusan | Opsi sederhana (A/B, versi lebih kecil, uji coba, jadwal call 10 menit) |
   | 4 | H+14 | Penutup sopan ("pesan pamit") | Tutup urutan, pintu tetap terbuka, tanpa menyalahkan |

   Tahap "nanti dulu": ikuti waktu yang disebut prospek (mis. "bulan depan") dan jarakkan lebih longgar (H+7, H+21, H+45) — atur dengan `--hari`.
2. **Hitung tanggal kirim dengan script** (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/jadwal_followup.py --mulai 2026-09-23
   python3 <folder-skill-ini>/scripts/jadwal_followup.py --mulai 2026-09-23 --hari "7,21,45" --libur "2026-12-25"
   ```
   Default menggeser jadwal dari Sabtu/Minggu/libur ke hari kerja berikutnya (cocok B2B), **dan** menjaga jarak minimal antar-pesan sesuai rencana (mis. H+3 → H+7 tetap berjarak ≥ 4 hari) sehingga pesan tidak menumpuk setelah digeser. Untuk pembeli perorangan/online shop tambahkan `--termasuk-akhir-pekan`.
   - Jika kolom menandai `SUDAH LEWAT` (H+0 sudah lama), jangan kirim pesan beruntun: pilih satu pesan yang sesuai situasi hari ini, lalu buat jadwal baru dengan `--mulai <hari ini>`. Jika Python tidak bisa dijalankan, hitung manual dari kalender (H+0 + N hari, geser ke hari kerja) dan beri tahu pengguna.
3. **Tulis pesan** untuk tiap jadwal, per saluran:
   - **WA:** 2–5 kalimat, satu tujuan, satu pertanyaan penutup yang gampang dijawab. Maks. 1 emoji. Tanpa huruf kapital berteriak.
   - **Email (B2B):** subjek pendek & spesifik (balas di thread yang sama untuk ke-1 s.d. ke-3), 50–120 kata, tanda tangan lengkap.
   - Variasikan pembuka; jangan mengulang "Mau follow up ya" di setiap pesan.
4. **Sertakan aturan main** untuk pengguna: jam kirim yang disarankan, kapan berhenti, cara menanggapi balasan umum (lihat format output).
5. **Periksa** dengan checklist; tawarkan versi lebih santai/formal atau bahasa Inggris.

### Prinsip nada (wajib)
- Tidak memaksa, tidak menyindir ("kok nggak dibalas?", "saya tunggu kabarnya dari kemarin"), tidak membuat rasa bersalah.
- Jangan membuat urgensi palsu ("stok tinggal 1", "harga naik besok") kecuali benar dan diberikan pengguna.
- Selalu beri jalan keluar yang mudah: "Kalau belum jadi prioritas, cukup balas 'nanti' saja, Pak/Bu. Saya tidak akan mengganggu."
- Hormati privasi (UU PDP 27/2022): hanya hubungi orang yang memberi kontaknya untuk urusan ini; berhenti bila diminta; jangan menambahkan ke grup/broadcast tanpa persetujuan.

## Format output
```
### Jadwal follow-up – [Nama prospek] ([tahap])
[Tabel dari script]

### Pesan ke-1 · [tanggal] · WA
[isi]

### Pesan ke-1 · [tanggal] · Email   ← hanya jika B2B/email diminta
Subjek: ...
[isi]

... (ke-2 s.d. ke-4)

### Aturan main
- B2B: kirim pukul 09.00–11.00 atau 13.00–15.00 hari kerja; hindari jam salat Jumat & larut malam.
- B2C/online shop: 19.00–20.30 sering lebih efektif; jangan lewat pukul 21.00.
- Jika prospek membalas di tengah urutan → hentikan urutan, tanggapi balasannya.
- Jika dijawab "tidak" / "jangan dihubungi" → kirim ucapan terima kasih singkat, hapus dari daftar follow-up.
- Balasan umum & cara menjawab: "mahal" → ..., "tanya atasan dulu" → ..., "nanti" → ...

### Asumsi (jika ada)
```

## Contoh
**Input pengguna:** "Aku jual jasa laundry seragam untuk hotel di Bali, 'Bersih Kilat Laundry'. Tanggal 23 September kirim penawaran Rp 8.500/kg ke Pak Made, Housekeeping Manager Hotel Taman Sari Ubud. Belum dibalas."

**Output (ringkas):** jadwal Kamis 24 Sep, Senin 28 Sep (H+3 digeser dari Sabtu), Jumat 2 Okt dan Jumat 9 Okt 2026 (digeser agar jarak antar-pesan tetap 4 dan 7 hari).
```
Pesan ke-1 · Kamis, 24 September 2026 · WA
Selamat pagi, Pak Made 🙏 Saya Wayan dari Bersih Kilat Laundry. Mau memastikan penawaran laundry seragam yang kami kirim kemarin sudah Bapak terima. Jika ada bagian yang perlu dijelaskan, misalnya jadwal jemput-antar atau penanganan noda, saya siap bantu.

Pesan ke-2 · Senin, 28 September 2026 · WA
Selamat siang, Pak Made. Sebagai gambaran, pelanggan hotel kami biasanya memakai jadwal jemput pagi dan antar sore di hari yang sama, sehingga stok seragam tidak menumpuk. Apakah pola seperti itu cocok untuk kebutuhan Taman Sari?

Pesan ke-3 · Jumat, 2 Oktober 2026 · WA
Pak Made, supaya lebih mudah menilai, kami bisa mulai dengan uji coba 1 minggu untuk seragam housekeeping saja, tanpa kontrak. Kalau Bapak berkenan, cukup balas "coba" dan saya atur jadwal jemput pertamanya.

Pesan ke-4 · Jumat, 9 Oktober 2026 · WA
Selamat pagi, Pak Made. Sepertinya laundry seragam belum jadi prioritas saat ini, dan itu sama sekali tidak apa-apa. Saya tidak akan mengirim pengingat lagi. Jika suatu saat butuh cadangan laundry, nomor ini tetap aktif. Terima kasih atas waktunya, Pak 🙏
```
Asumsi: nama pengirim "Wayan", uji coba 1 minggu diperbolehkan (konfirmasi ke pengguna sebelum dikirim).

## Checklist sebelum mengirim hasil
- [ ] Tanggal dari output script (atau hitung manual tertulis).
- [ ] Tiap pesan punya tujuan berbeda dan satu ajakan yang mudah dijawab.
- [ ] Tidak ada nada menyalahkan, urgensi palsu, atau klaim yang tidak diberikan pengguna.
- [ ] Penawaran baru (diskon, uji coba, bonus) hanya yang disetujui pengguna; jika disarankan AI, beri label "usulan — konfirmasi dulu".
- [ ] Pesan terakhir menutup urutan dengan sopan dan meninggalkan pintu terbuka.
- [ ] Sapaan & gaya konsisten (Bapak/Ibu vs Kak), nama prospek benar.

## Batasan & penanganan error
- Skill tidak mengirim pesan otomatis; pengguna yang menyalin & mengirim.
- Maksimal 4 pesan per urutan untuk satu tahap (script membatasi 8 jadwal). Jika pengguna ingin lebih sering/lebih banyak, jelaskan risikonya (diblokir/dilaporkan spam) dan sarankan jarak lebih longgar.
- Jika prospek sudah membalas dengan keberatan spesifik, jangan pakai urutan — tulis satu balasan yang menjawab keberatannya (lihat bagian "balasan umum" di references).
- Tanggal libur nasional/cuti bersama tidak diketahui script; minta pengguna menyebutkannya lewat `--libur` bila relevan.
