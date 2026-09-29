# Bot Trading Kripto: Aturan Anda, Dijalankan Disiplin

**Tagline:** Tulis aturan trading Anda sekali; bot menjalankannya 24 jam dengan rem darurat,
batas rugi, dan catatan lengkap, mulai dari simulasi tanpa uang asli.

---

> ## ⚠️ PERINGATAN RISIKO — WAJIB DIBACA
> - **Ini bukan nasihat investasi dan bukan sinyal trading.** Komunitech tidak memilih koin,
>   tidak memberi angka "yang menguntungkan", dan tidak menjanjikan keuntungan apa pun.
> - **Aset kripto sangat berisiko.** Harga bisa jatuh puluhan persen dalam hitungan hari.
>   Anda bisa kehilangan **seluruh** modal. Contoh nyata di `examples/contoh-01`: aturan DCA
>   contoh pada data setahun terakhir berakhir **rugi 32,76%** dan berhenti oleh stop-loss.
> - **Bot hanya sebaik aturan Anda.** Aturan yang buruk dijalankan dengan disiplin tetap
>   menghasilkan kerugian. Hasil uji masa lalu tidak menjamin hasil masa depan.
> - **Mode live memakai uang asli** dan order yang sudah terjadi tidak bisa dibatalkan.
>   Mulai dari simulasi, lalu nominal kecil.
> - Gunakan bursa **berizin OJK** (cek daftar di ojk.go.id). Janji "untung pasti" = tanda
>   penipuan; laporkan ke OJK 157 / Satgas PASTI.
> - Keputusan dan risiko **sepenuhnya milik Anda**.

---

## Manfaat
1. **Disiplin tanpa emosi**: beli rutin (DCA), grid, ambil untung/batasi rugi, atau jaga porsi
   aset persis seperti aturan yang Anda tulis, tanpa panik atau serakah.
2. **Rem berlapis bawaan**: batas modal per order & total, stop-loss, batas rugi harian, batas
   order terbuka, dan **tombol berhenti** ("stop bot" dari Telegram). Bot berhenti sendiri saat
   batas tersentuh.
3. **Coba dulu tanpa risiko**: uji mundur (backtest) pada data setahun + simulasi dengan harga
   asli, sebelum menyentuh uang sungguhan.
4. **Kunci API aman**: hanya kunci *tanpa izin tarik dana*, disimpan di komputer Anda sendiri,
   tidak pernah ditampilkan atau dicatat.
5. **Catatan rapi & pajak terhitung**: setiap transaksi tercatat (CSV + log audit), lengkap
   dengan fee dan PPh final 0,21% (PMK 50/2025), siap direkap per bulan.

## Cocok untuk siapa
- Pemilik usaha/profesional yang sudah punya **aturan investasi kripto sendiri** (mis. nabung
  BTC rutin) dan ingin itu berjalan otomatis dan tercatat.
- Trader yang ingin **grid atau TP/SL** berjalan saat ia sibuk, dengan batas rugi yang tegas.
- **Tidak cocok** untuk yang mencari "bot pasti cuan", sinyal, futures/leverage, atau
  mengelola dana orang lain.

## Sebelum / sesudah
| Tanpa skill | Dengan skill |
|---|---|
| Buka aplikasi tiap Senin untuk beli rutin, kadang lupa, kadang ragu. | Bot membeli sesuai jadwal Anda; notifikasi Telegram tiap transaksi. |
| Tidak ada batas rugi tertulis; saat harga jatuh, keputusan diambil dalam panik. | Stop-loss & batas rugi harian ditulis di awal; bot berhenti otomatis dan memberi tahu alasannya. |
| Untung/rugi, fee, dan pajak dihitung kira-kira. | Semua angka dihitung script (Decimal), PPh dibulatkan sesuai aturan, rekap bulanan tersedia. |
| "Bot trading" dari internet minta API key lengkap (termasuk tarik dana). | Kunci **trade-only** saja; kunci ber-izin withdraw **ditolak** (Binance) atau wajib dipastikan manual (Indodax). |

## Cara pakai (kalimat biasa ke agen AI Anda)
- "Buat bot beli BTC Rp100 ribu tiap minggu di Indodax, modal maks Rp2 juta, stop-loss 25%."
- "Backtest aturan itu pakai data setahun."
- "Jalankan simulasinya tiap jam dan kabari saya di Telegram."
- "Status bot?" · "Stop bot sekarang!"

Urutan aman: **backtest → simulasi (paper) → testnet (opsional) → live** dengan konfirmasi
bertahap (Anda sendiri mengetik kalimat persetujuan berisi kode unik).

## Bursa yang didukung (v1.0.4)
| Bursa | Simulasi | Testnet/demo | Live |
|---|---|---|---|
| Indodax (PAKD berizin OJK*) | Ya (harga asli, teruji) | demo-indodax.com (belum teruji) | Ya |
| Binance Spot | Ya (harga asli, teruji) | Spot Testnet | Ya, dengan pernyataan khusus (bukan PAKD berizin OJK*) |
\*Cek ulang daftar resmi di ojk.go.id.

**Batas modal dijaga lintas folder:** bot live mencatat modal terpakai di buku global per akun
bursa (di folder `.komunitech` komputer Anda) dan mengecek saldo koin + order terbuka di bursa sebelum
setiap pembelian. Menyalin/menghapus folder bot tidak menambah jatah modal. Yang **tidak** bisa dicegah:
orang yang menghapus folder `.komunitech` sekaligus data bot, memakai kunci API baru untuk akun yang sama,
atau menjalankan bot di dua komputer sekaligus. Aturan aman: satu kunci API untuk satu bot, dan isi akun
bursa hanya sebesar modal yang siap Anda pertaruhkan.

**Kejujuran status uji:** harga & data publik kedua bursa diuji langsung. Pengiriman order,
cek izin kunci, dan pembatalan order diuji terhadap **server tiruan** yang meniru dokumentasi
resmi bursa, **belum** terhadap akun sungguhan. Karena itu mulai dari simulasi dan nominal kecil.

## Instalasi singkat
Salin folder `bot-trading-kripto` ke folder skills AI agent Anda (rincian & Windows di
`docs/instalasi.md`, disertakan di paket):

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` (atau `openclaw skills install ./bot-trading-kripto --global`) |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Jadwal otomatis & notifikasi Telegram di OpenClaw: `references/openclaw-jadwal.md`.
Butuh **Python 3** (tanpa paket tambahan). Agar bot berjalan terus, komputer/VPS harus menyala;
Komunitech menyediakan **jasa setup berbayar** bila Anda ingin dibantu.

## FAQ
**1. Apakah bot ini menjamin untung?**
Tidak. Tidak ada yang bisa menjamin. Bot hanya menjalankan aturan Anda dengan disiplin dan
berhenti saat batas rugi tersentuh. Contoh backtest di paket ini justru menunjukkan kerugian.

**2. Apakah dana saya bisa dicuri lewat bot ini?**
Bot hanya memakai kunci **tanpa izin tarik dana**, disimpan di komputer Anda (bukan di chat,
bukan di server Komunitech). Kunci dengan izin withdraw ditolak otomatis (Binance) atau wajib Anda
pastikan mati lewat daftar periksa di layar Indodax sebelum live (bot sengaja tidak menyentuh fitur
withdraw sama sekali). Kunci tidak pernah dikirim ke alamat selain bursa resmi, termasuk saat bursa
mengalihkan alamat. Jika curiga bocor: "stop bot", cabut kunci di bursa, buat baru.

**3. Bagaimana dengan pajaknya?**
Setiap penjualan dihitung PPh final 0,21% (bursa dalam negeri) atau 1% (luar negeri) sesuai
PMK 50/2025 (berlaku 1 Agustus 2025). Untuk pasangan kripto-kripto (mis. BTC/USDT) PPh juga dihitung
di sisi beli, karena menurut PMK itu tukar-menukar kripto dikenai PPh atas nilai masing-masing aset. Bursa dalam negeri memotongnya otomatis; bot mencatatnya
agar untung/rugi Anda bersih. Pembulatan belum dicocokkan dengan Coretax; bukti potong dari
bursa yang berlaku. Untuk kewajiban pajak pribadi, konsultasikan ke konsultan pajak/DJP.
