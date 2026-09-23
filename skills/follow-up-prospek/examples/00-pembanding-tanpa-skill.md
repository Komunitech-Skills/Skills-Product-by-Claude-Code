# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama dengan S1):**
> Kemarin (22 Sept) saya demo aplikasi kasir KasirPintar Fiktif ke Pak Joni, pemilik Resto Padang Rasa Minang Fiktif di Depok. Paket 199rb/bulan, gratis setup. Dia bilang bagus, tapi mau diskusi dulu sama istrinya yang pegang keuangan. Dia sempat nanya apakah bisa cetak struk ke printer lama mereka (Epson TM-U220) — jawabannya bisa. Nama saya Rudi. Bikinin follow-up WA ya.

## Output TANPA skill (AI agent biasa, lengkap)
```
Berikut contoh pesan follow-up WhatsApp untuk Pak Joni:

Pesan 1 (1–2 hari setelah demo):
"Selamat siang Pak Joni, saya Rudi dari KasirPintar. Terima kasih atas waktunya kemarin untuk demo
aplikasi kasir kami. Sekadar mengingatkan, paket kami hanya Rp199.000/bulan dengan gratis setup, dan
bisa langsung terhubung ke printer Epson TM-U220 Bapak. Bagaimana, Pak, apakah sudah ada keputusan?"

Pesan 2 (3–5 hari kemudian):
"Halo Pak Joni, bagaimana hasil diskusinya dengan Ibu? Jika Bapak mendaftar minggu ini, kami bisa
berikan bonus 1 bulan gratis! Promo terbatas ya, Pak 😊"

Pesan 3 (1 minggu kemudian):
"Selamat pagi Pak Joni, mohon maaf mengganggu lagi. Saya ingin menanyakan kembali terkait aplikasi
kasir kami. Ditunggu kabar baiknya ya, Pak."

Tips: follow-up secara konsisten, jangan menyerah, dan tetap sopan.
```

## Output DENGAN skill
Lihat `01-setelah-demo-aplikasi-kasir.md` (jadwal bertanggal + 4 pesan + aturan main + asumsi).

## Perbandingan

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Jadwal | "1–2 hari", "3–5 hari" — kabur | Tanggal pasti dari script, digeser dari akhir pekan |
| Tujuan tiap pesan | Semua menanyakan "sudah ada keputusan?" | Berbeda: rangkuman → nilai untuk si pengambil keputusan (istri) → pilihan mudah 1/2 → pamit |
| Tekanan | "apakah sudah ada keputusan?" di pesan pertama; "ditunggu kabar baiknya" | Tidak menekan; ada jalan keluar ("cukup balas 1 atau 2") |
| Klaim/promo | **Mengarang** promo "bonus 1 bulan gratis, promo terbatas" (urgensi palsu, tidak diberikan pengguna) | Tidak ada promo; usulan fitur diberi label "konfirmasi dulu" |
| Penutup urutan | Tidak ada; saran "jangan menyerah" (berisiko spam) | Pesan pamit yang menjaga hubungan |
| Menjawab balasan | Tidak ada | Aturan main + bank balasan "mahal", "diskusi dulu", "nanti" |

## Penilaian
Hasil dengan skill **jelas lebih baik**: tanggal pasti, tiap pesan membawa alasan baru untuk membalas, tidak mengarang promo/urgensi palsu (risiko janji yang tidak bisa ditepati), dan ada titik berhenti yang sopan. Versi tanpa skill cenderung mendesak dan berulang.
