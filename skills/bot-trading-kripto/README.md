# Bot Trading Kripto: Aturan Anda, Dijalankan Disiplin

**Tulis aturan trading Anda sekali; bot menjalankannya sesuai jadwal (selama komputer atau server sewaan/VPS Anda menyala) dengan rem darurat,
batas rugi, dan catatan lengkap, mulai dari simulasi tanpa uang asli.**

---

> ## ⚠️ PERINGATAN RISIKO — WAJIB DIBACA
> - **Ini bukan nasihat investasi dan bukan sinyal trading.** Komunitech tidak memilih koin,
>   tidak memberi angka "yang menguntungkan", dan tidak menjanjikan keuntungan apa pun.
> - **Aset kripto sangat berisiko.** Harga bisa jatuh puluhan persen dalam hitungan hari.
>   Anda bisa kehilangan **seluruh** modal. Contoh nyata di `examples/contoh-01`: aturan beli rutin (DCA)
>   contoh pada data setahun terakhir berakhir **rugi 32,76%** dan berhenti oleh stop-loss (batas rugi otomatis).
> - **Bot hanya sebaik aturan Anda.** Aturan yang buruk dijalankan dengan disiplin tetap
>   menghasilkan kerugian. Hasil uji masa lalu tidak menjamin hasil masa depan.
> - **Bawaan bot adalah simulasi (paper) atau testnet (bursa percobaan).** Mode live memakai uang asli dan order
>   yang sudah terjadi tidak bisa dibatalkan; baru terbuka setelah konfirmasi bertahap.
>   Mulai dari simulasi, lalu nominal kecil.
> - Gunakan bursa **berizin OJK** (cek daftar di ojk.go.id). Janji "untung pasti" = tanda
>   penipuan; laporkan ke OJK 157 / Satgas PASTI.
> - Keputusan dan risiko **sepenuhnya milik Anda**.

---

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
1. **Disiplin tanpa emosi**: beli rutin (DCA, beli nominal tetap berkala), grid (beli-jual
   bertahap di rentang harga), ambil untung/batasi rugi, atau jaga porsi aset sesuai aturan
   yang Anda tulis, tanpa panik atau serakah.
2. **Rem berlapis bawaan**: batas modal per order & total, stop-loss, batas rugi harian, batas
   order terbuka, dan **tombol berhenti** ("stop bot" dari Telegram; pengiriman lewat Telegram
   belum diuji langsung). Bot berhenti sendiri saat batas tersentuh.
3. **Coba dulu tanpa uang asli**: uji mundur (backtest) pada data setahun + simulasi dengan harga
   asli, sebelum menyentuh uang sungguhan.
4. **Kunci API tanpa izin tarik dana**: kunci API (kunci akses bot ke akun bursa) hanya yang
   *tanpa izin tarik dana*, disimpan di komputer Anda sendiri, tidak ditampilkan atau dicatat
   oleh bot.
5. **Catatan rapi & pajak terhitung**: setiap transaksi tercatat (tabel CSV yang bisa dibuka di
   Excel + catatan audit), lengkap
   dengan fee dan PPh final 0,21% (PMK 50/2025), siap direkap per bulan.

## Cocok untuk siapa
- Pemilik usaha/profesional yang sudah punya **aturan investasi kripto sendiri** (mis. nabung
  BTC rutin) dan ingin itu berjalan otomatis dan tercatat.
- Trader yang ingin **grid atau TP/SL** (ambil untung/batasi rugi otomatis) berjalan saat ia sibuk, dengan batas rugi yang tegas.
- **Tidak cocok** untuk yang mencari "bot pasti cuan", sinyal, futures/leverage (kontrak
  berjangka dan pinjaman modal), atau mengelola dana orang lain.

## Sebelum / sesudah
| Tanpa skill | Dengan skill |
|---|---|
| Buka aplikasi tiap Senin untuk beli rutin, kadang lupa, kadang ragu. | Bot membeli sesuai jadwal Anda; notifikasi Telegram tiap transaksi (belum diuji langsung). |
| Tidak ada batas rugi tertulis; saat harga jatuh, keputusan diambil dalam panik. | Stop-loss & batas rugi harian ditulis di awal; bot berhenti otomatis dan memberi tahu alasannya. |
| Untung/rugi, fee, dan pajak dihitung kira-kira. | Angka dihitung skrip dengan ketelitian desimal, PPh dibulatkan ke bawah (belum dicocokkan dengan Coretax), rekap bulanan tersedia. |
| "Bot trading" dari internet minta API key lengkap (termasuk tarik dana). | Kunci **khusus trading** saja; kunci yang punya izin tarik dana (withdraw) **ditolak** (Binance) atau izin itu wajib Anda pastikan mati sendiri (Indodax). |

## Cara pakai (kalimat biasa ke agen AI Anda)
- "Buat bot beli BTC Rp100 ribu tiap minggu di Indodax, modal maks Rp2 juta, stop-loss 25%."
- "Backtest aturan itu pakai data setahun."
- "Jalankan simulasinya tiap jam dan kabari saya di Telegram." (jadwal dan notifikasi Telegram belum diuji langsung)
- "Status bot?" · "Stop bot sekarang!"

Urutan yang disarankan: **backtest → simulasi (paper, order pura-pura dengan harga asli) →
testnet (bursa percobaan, opsional) → live** dengan konfirmasi bertahap (Anda sendiri mengetik
kalimat persetujuan berisi kode unik).

Contoh keluaran uji mundur (aturan DCA contoh pada data harga asli Indodax setahun; aturannya hanya contoh format, bukan anjuran; dari `examples/contoh-01-backtest-dca-btcidr.md`):
```
UJI MUNDUR (backtest) btc_idr - strategi dca - 2025-09-29 s.d. 2026-09-29 (366 baris)
Modal bot: Rp2.000.000 -> akhir Rp1.344.864 (-32.76%)
Untung/rugi terealisasi: -Rp655.136 | koin tersisa 0 BTC
Transaksi: 20 | total fee Rp6.300 | PPh Rp2.624
Penurunan terdalam (drawdown): 33.02%
Bot berhenti: STOP-LOSS: harga Rp1.063.498.000 sudah 25% atau lebih di bawah harga rata-rata beli Rp1.616.605.684. Posisi dijual & bot berhenti.
Pembanding faktual beli sekali & tahan: Rp1.575.171 (-21.24%)
Catatan: Hasil masa lalu tidak menjamin hasil masa depan.
```

## Bursa yang didukung (v1.0.6)
| Bursa | Simulasi | Testnet/demo | Live |
|---|---|---|---|
| Indodax (PAKD berizin OJK*) | Ya (harga asli, teruji) | demo-indodax.com (belum teruji) | Ya (belum diuji di akun sungguhan) |
| Binance Spot | Ya (harga asli, teruji) | Spot Testnet (belum diuji dengan akun testnet) | Ya, dengan pernyataan khusus (bukan PAKD berizin OJK*); belum diuji di akun sungguhan |
\*PAKD = Pedagang Aset Keuangan Digital. Cek ulang daftar resmi di ojk.go.id.

**Batas modal dijaga lintas folder:** bot live mencatat modal terpakai di buku global per akun
bursa (di folder `.komunitech` komputer Anda) dan mengecek saldo koin + order terbuka di bursa sebelum
setiap pembelian. Menyalin/menghapus folder bot tidak menambah jatah modal. Yang **tidak** bisa dicegah:
orang yang menghapus folder `.komunitech` sekaligus data bot, memakai kunci API baru untuk akun yang sama,
atau menjalankan bot di dua komputer sekaligus. Aturan yang disarankan: satu kunci API untuk satu bot, dan isi akun
bursa hanya sebesar modal yang siap Anda pertaruhkan.

## Instalasi singkat
Salin folder `bot-trading-kripto` ke folder skills AI agent Anda (rincian & Windows di
`docs/instalasi.md`, disertakan di paket):

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` (atau `openclaw skills install ./bot-trading-kripto --global`) |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Jadwal otomatis & notifikasi Telegram di OpenClaw (belum diuji langsung): `references/openclaw-jadwal.md`.
Butuh **Python 3** (tanpa paket tambahan). Agar bot berjalan terus, komputer atau server sewaan (VPS) harus menyala;
Komunitech menyediakan **jasa setup berbayar** bila Anda ingin dibantu.

**Hasil uji (angka nyata):** uji independen Claude Code (simulasi agent), Sep 2026 (v1.0.6): simulasi beli rutin (DCA) di Indodax **12/12** transaksi cocok dengan hitungan ulang penguji; pintu pengaman mode live (konfirmasi bertahap) dan penolakan kunci yang punya izin tarik dana lulus; A/B: tanpa skill, AI langsung menulis program trading live (pustaka `ccxt`) tanpa batas risiko; dengan skill mulai dari simulasi dengan 5 batas wajib. Sumber: `examples/HASIL-UJI.md`, `examples/00-pembanding-tanpa-skill.md`.

**Status uji (jujur):** lulus uji independen simulasi agent (Claude Code) setelah perbaikan temuan uji. Harga & data publik kedua bursa diuji langsung; pengiriman order, cek izin kunci, dan pembatalan order baru diuji terhadap **server tiruan** yang meniru dokumentasi resmi bursa, **belum** terhadap akun sungguhan (live maupun testnet; uji testnet menunggu kunci dari pemilik). Pengujian di OpenClaw (sebelum/sesudah, jadwal, dan notifikasi Telegram) ditunda atas keputusan pemilik dan belum dilakukan. Codex/Cursor belum diuji langsung. Karena itu mulai dari simulasi dan nominal kecil.

## FAQ
**1. Apakah bot ini menjamin untung?**
Tidak. Tidak ada yang bisa menjamin. Bot hanya menjalankan aturan Anda dengan disiplin dan
berhenti saat batas rugi tersentuh. Contoh backtest di paket ini justru menunjukkan kerugian.

**2. Apakah dana saya bisa dicuri lewat bot ini?**
Bot hanya memakai kunci **tanpa izin tarik dana**, disimpan di komputer Anda (bukan di chat,
bukan di server Komunitech). Kunci dengan izin withdraw ditolak otomatis (Binance) atau wajib Anda
pastikan mati lewat daftar periksa di layar Indodax sebelum live (bot sengaja tidak menyentuh fitur
withdraw sama sekali). Bot dirancang tidak mengirim kunci ke alamat selain bursa resmi, termasuk saat bursa
mengalihkan alamat. Kunci trading yang bocor tetap bisa dipakai membeli/menjual di akun Anda, sebab itu isi akun sebatas modal yang siap dipertaruhkan. Jika curiga bocor: "stop bot", cabut kunci di bursa, buat baru.

**3. Bagaimana dengan pajaknya?**
Setiap penjualan dihitung PPh final 0,21% (bursa dalam negeri) atau 1% (luar negeri) sesuai
PMK 50/2025 (berlaku 1 Agustus 2025). Untuk pasangan kripto-kripto (mis. BTC/USDT) PPh juga dihitung
di sisi beli, karena menurut PMK itu tukar-menukar kripto dikenai PPh atas nilai masing-masing aset. Bursa dalam negeri memotongnya otomatis; bot mencatatnya
agar untung/rugi Anda bersih. Pembulatan belum dicocokkan dengan Coretax; bukti potong dari
bursa yang berlaku. Untuk kewajiban pajak pribadi, konsultasikan ke konsultan pajak/DJP.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
