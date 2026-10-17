# Riwayat perubahan — laporan-iklan-mingguan

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.12 (2026-10-17)
Dari pra-cek di bot Telegram asli (konteks kanal Telegram, skor 7,0 "tidak siap"; semua angka benar):
1. **Kata "hasilnya itu chat WA masuk" disalahartikan sebagai perintah menyambungkan WhatsApp.** Jawaban
   bot dibuka dengan "gateway", "pairing", "script resmi" dan menawarkan menyambungkan WhatsApp, padahal
   maksud pengguna: hasil kampanye = chat WA yang masuk. `SKILL.md` kini punya bagian **Aturan bicara ke
   pengguna**: "chat WA masuk / pesan WA / klik ke WA" adalah metrik hasil iklan Click-to-WhatsApp (dipakai
   sebagai `--nama-hasil`), skill tidak pernah menawarkan menyambungkan WhatsApp/gateway/pairing, balasan
   dibuka dengan isi laporan, dan kata proses (script, gateway, pairing, JSON, nama file, path, nama
   opsi) tidak boleh muncul di chat. Pertanyaan balik: satu pesan, maksimal 3 pertanyaan pendek.
2. **Baris teknis "Kolom dibaca: nama='Campaign name' ..." ikut ditampilkan ke pengguna.** Baris itu
   dihapus dari teks laporan (`teks` pada `--json` dan keluaran biasa). Pemetaan tetap ada di JSON
   (`kolom_dipakai`) dan bisa dicetak hanya dengan opsi teknisi `--tampilkan-kolom` (diberi tanda "jangan
   diteruskan ke pengguna"). Bila ada dua kolom yang sama-sama mungkin (mis. `Link clicks` dan `Clicks
   (all)`), Catatan menyebutnya dalam satu kalimat awam ("Saya membaca kolom 'Link clicks' sebagai jumlah
   klik. Ada kolom lain yang mirip ('Clicks (all)'); kalau yang Anda maksud kolom itu, kabari saya.");
   daftar kolom pesaing juga ada di JSON (`kolom_meragukan`). Angka tidak berubah.
3. **Pindai teks lain yang tampil ke pengguna:** peringatan/catatan tidak lagi menyuruh "jalankan ulang"
   atau menyebut `--kolom-nama` / `--mata-uang IDR` (diganti "kirim ulang ke saya", "bilang saja 'rinci
   per kampanye'", "sesuai konfirmasi Anda bahwa angkanya sudah Rupiah"); "sampel kecil" diganti "datanya
   masih sedikit"; satu baris **Arti istilah** di ujung Catatan menjelaskan CPC, CPM, CTR (dan ROAS bila
   ada). Pesan error script sengaja tetap teknis (untuk agen); `SKILL.md` menyuruh agen mengubahnya ke
   kalimat biasa.
Mode `gabung` ikut meneruskan kalimat kolom per platform. Tes regresi 108 (10 tes baru `UjiV1012BotTelegram`). Perhitungan tidak berubah.

## Catatan revisi 1.0.11 (2026-10-13)
Rujukan ke aturan kerja internal di `SKILL.md` (bagian Pembulatan) dan `references/sumber-kolom.md` diganti kalimat yang berdiri sendiri; pembulatan dan cara kerja tidak berubah.

## Catatan revisi 1.0.10 (2026-10-01)
Dari uji sebelum/sesudah OpenClaw: laporan sempat menyarankan mematikan kampanye *Traffic* dan
*Awareness* hanya karena "0 pesan WA", padahal tujuannya memang bukan pesan. Kini tiap kampanye
dinilai terhadap **tujuannya** (dari kolom Objective/Result indicator, atau dari nama kampanye):
kampanye Traffic/Awareness/Reach/Video views/Engagement tampil di bagian **TUJUAN BERBEDA** dengan
CPC, CTR, dan CPM, tidak lagi masuk daftar "matikan". Catatan juga menyebut biaya per pesan khusus
kampanye bertujuan pesan. Baris **"Kolom dibaca"** dipindah ke baris ke-3 laporan supaya selalu
ikut terkirim, tidak terpotong. (Sejak 1.0.12 baris itu tidak lagi ikut laporan; lihat di atas.)

## Riwayat versi lama (dipindah dari `SKILL.md` pada 1.0.12)
- **1.0.10** (2026-10-01): dari uji OpenClaw: kampanye Traffic/Awareness/Reach/Video views/Engagement tanpa pesan tidak lagi disarankan dimatikan — dinilai terhadap tujuannya (bagian `TUJUAN BERBEDA` berisi CPC/CTR/CPM; Catatan menyebut biaya per hasil khusus kampanye hasil). Baris "Kolom dibaca" dipindah ke atas (baris ke-3) agar tidak terpotong; Langkah 4 menegaskan blok dikirim utuh. Tes regresi 98.
- **1.0.8** (2026-09-29): aturan kerja standar library: tidak menginstal paket, tidak membuka/mencari file di luar yang diberikan, lokasi file baru disebut, hasil di folder kerja yang disepakati (bukan /tmp).
- **1.0.7** (2026-09-29): pada file bertingkat (kampanye > grup iklan), baris yang kolom grup iklannya kosong padahal kampanye itu punya baris grup iklan bernama diperiksa: bila biaya, tayangan & kliknya sama dengan jumlah baris grup iklan (total kampanye tanpa label) baris itu tidak dihitung dua kali dan diberi ⚠️; bila tidak sama tetap dihitung dengan ⚠️ "mohon cek". Baris Performance Max tanpa saudara tidak terkena. Tes regresi 94.
- **1.0.5** (2026-09-29): baris Google Performance Max tanpa grup iklan tidak lagi tampil
  "(tanpa nama, baris N)", melainkan memakai nama grup aset (bila ada kolom "Asset group") atau nama
  kampanye + "(tanpa grup iklan)" (P-3); ⚠️ subtotal/total yang meragukan kini menyebut total belanja
  sekarang dan total alternatif bila baris itu dihitung/tidak dihitung (P-4). Tes regresi 91.
- **1.0.4** (2026-09-28): subtotal buatan admin di kolom nama ("Subtotal: Retarget Video",
  "Retarget Video Total", "Jumlah sementara") tidak lagi terhitung dua kali dan selalu diberi ⚠️
  nama + biaya (N3); kalimat ⚠️ "biaya hampir sama dengan jumlah baris lain" dilunakkan. Tes regresi
  bertambah jadi 87.
- **1.0.3** (2026-09-26): nama kampanye berawalan "Total"/"Jumlah" tidak lagi dibuang; setiap baris
  total yang dikecualikan diberi ⚠️; ⚠️ ±5% (M2); subtotal dengan kolom nama kosong (M3).
- **1.0.2** (2026-09-26): ekspor bertingkat dirinci per iklan (N1); label total umum + cek silang (N2).
- **1.0.1** (2026-09-26): sel kosong, baris total varian, pemilihan kolom Google Ads, mata uang non-IDR.
- **1.0.0**: rilis draf pertama.
