# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Tolong bikinin broadcast WA buat pelanggan toko roti saya, Roti Hangat Mbak Sri di Solo. Promo gajian 25-30 September: roti sobek cokelat 25rb jadi 20rb, terus roti manis beli 2 gratis 1. Order tinggal bales chat, bisa diantar buat area Laweyan. Aku ada file pelanggan.csv, mulai kirim Jumat 25 Sept jam 10 pagi ya. Yang udah bilang stop aku taruh di stop.txt.

## Output TANPA skill (AI agent biasa, tanpa membaca skill apa pun)
```
Berikut draf pesan broadcast WhatsApp untuk promo gajian Roti Hangat Mbak Sri:

🍞✨ PROMO GAJIAN ROTI HANGAT MBAK SRI! ✨🍞

Halo Kak! 👋
Gajian udah cair? Saatnya manjain keluarga dengan roti hangat favorit! 😍

🔥 Roti Sobek Cokelat: dari Rp25.000 jadi Rp20.000 aja (hemat 20%)!
🎁 Roti Manis: Beli 2 GRATIS 1!

📅 Berlaku: 25–30 September
🛵 Bisa diantar untuk area Laweyan
📲 Order? Langsung balas chat ini ya!

Stok terbatas, jangan sampai kehabisan! 🏃‍♀️💨

Roti Hangat Mbak Sri – Fresh setiap hari dari Solo 💛

---
Tips mengirim:
- Gunakan fitur Broadcast List di WhatsApp Business agar pesan terkirim ke banyak pelanggan sekaligus.
- Kirim sekitar jam 10 pagi sesuai rencana.
- Untuk file pelanggan.csv, kamu bisa mengimpor nomor-nomornya ke kontak HP lalu memasukkannya ke broadcast list.
  Jangan lupa hapus nomor yang ada di stop.txt ya.
```

## Output DENGAN skill
Lihat `01-promo-gajian-toko-roti-dengan-csv.md` (3 variasi personal + versi daftar siaran + jadwal bertahap + hasil olah 40 kontak → 25 siap kirim + checklist UU PDP).

## Berdampingan

| Aspek | TANPA skill | DENGAN skill |
|---|---|---|
| Personalisasi | "Halo Kak" untuk semua | `{sapaan} {nama}` → "Halo Bu Sri", "Halo Pak Joko" |
| Variasi | 1 pesan | 3 variasi berbeda (pembuka, susunan, CTA) + versi daftar siaran |
| Teks berhenti (opt-out) | **Tidak ada** | Ada di setiap variasi (wajib, dicek script) |
| Persetujuan (UU PDP) | Tidak disaring; menyarankan impor **semua** nomor | Hanya 25 kontak yang setuju; 10 belum/tidak setuju dibuang |
| Nomor dobel/rusak/berhenti | Dihapus manual oleh pengguna ("jangan lupa hapus") | Otomatis: 1 duplikat, 1 tidak valid, 3 berhenti dibuang |
| Angka | "hemat 20%" dihitung sendiri (benar, tapi tidak diminta) | Hanya angka dari pengguna |
| Klaim | "Stok terbatas, jangan sampai kehabisan!" dan "Fresh setiap hari" — **tidak diberikan pengguna** | Tidak ada klaim karangan |
| Gaya | Kapital + 15 emoji, mirip spam | Emoji ≤ 1–2 per variasi, seperti chat biasa |
| Jadwal | "jam 10 pagi" sekaligus | Bertahap 20/batch, jeda, peringatan jam salat Jumat |
| Link kirim | Tidak ada | `broadcast_siap.csv` berisi link wa.me per kontak |

## Penilaian
- **Lebih baik berkat skill:** (1) kepatuhan persetujuan & opt-out — versi tanpa skill tidak memberi cara berhenti dan
  menyarankan mengirim ke semua nomor di file, yang berisiko UU PDP dan nomor diblokir; (2) urgensi/klaim palsu ("stok
  terbatas", "fresh setiap hari") tidak muncul; (3) personalisasi nama + variasi mengurangi laporan spam; (4) pengolahan
  CSV yang terverifikasi (25/40) dan link wa.me siap klik; (5) jadwal bertahap.
- **Setara:** isi promo inti dan cara order sama-sama benar.
- **Kesimpulan:** hasil dengan skill **jelas lebih baik**, terutama pada aspek yang paling berisiko bagi pembeli (izin & opt-out).
