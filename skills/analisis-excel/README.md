# Analisis Excel Tanpa Rumus, Tinggal Tanya

**Kirim file Excel atau CSV (file tabel sederhana yang bisa dibuka di Excel), tanya pakai bahasa biasa, dapat tabel + temuan + saran grafik — angkanya
dihitung komputer, bukan dikira-kira AI.**

*Diuji AI penguji independen: 7,25 → 8,75 dari 10 (semua persen diambil dari skrip hitung, tanpa memasang paket tambahan diam-diam, dan data pribadi di file gaji diingatkan).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Jawaban langsung dari file Anda:** "total per kategori", "bulan mana paling tinggi",
  "September naik berapa dibanding Agustus", "10 pelanggan terbesar" — tanpa bikin tabel ringkasan
  (PivotTable) atau rumus rumit sendiri.
- ✅ **Angka dihitung komputer, bukan dikira:** persen dan total dihitung skrip (presisi penuh untuk rupiah),
  baris "TOTAL" yang jelas di bawah tabel tidak dihitung dua kali (yang meragukan ditanyakan ke Anda),
  dan nilai yang aneh dilaporkan lengkap dengan nomor barisnya — bukan ditebak diam-diam.
- ✅ **Tahan file berantakan:** judul laporan di atas tabel, sel gabungan (merge), angka
  "Rp 1.234.567,89", tanggal campur "25/09/2026" / "25 Sep 2026" / "2026-09-25", "kopi susu" vs
  "Kopi Susu ", file CSV dari Excel Windows lama — umumnya terbaca; bila ragu, AI bertanya atau
  menolak dengan alasan jelas, bukan menebak.
- ✅ **Siap pakai:** tabel siap tempel ke WA/laporan, file CSV hasil yang bisa dibuka di Excel,
  narasi temuan bahasa awam, dan saran grafik yang cocok.
- ✅ **Merapikan data:** satu perintah menghasilkan salinan data yang bersih (file asli tidak
  diubah).

## Cocok untuk siapa
- Pemilik usaha & admin kantor yang punya data di Excel (biaya operasional, stok, pelanggan,
  piutang, absensi) tapi tidak sempat/tidak bisa bikin PivotTable
- Profesional (HR, keuangan, guru, pengurus koperasi/yayasan) yang butuh ringkasan cepat untuk
  rapat atau laporan ke atasan
- Siapa pun yang sering ditanya "totalnya berapa?" dan harus menghitung manual

## Contoh sebelum & sesudah
**Sebelum (AI tanpa skill, risiko yang bisa muncul):** AI membaca sebagian isi file lalu *mengira-ngira* total; baris
"TOTAL" di bawah tabel ikut terjumlah (hasilnya jadi dobel), "LISTRIK & AIR" dan "listrik & air"
dihitung sebagai dua kategori, dan sel yang isinya rumus kosong tidak disadari.

**Sesudah (dengan skill):** "Ini file biaya operasional, pengeluaran paling besar di mana dan
September naik berapa dari Agustus?"
```
| Kategori      | Baris | Jumlah Nominal | % dari total |
| Sewa          | 3     | Rp 13.500.000  | 48,9%        |
| Transport     | 5     | Rp 8.995.000   | 32,6%        |
| Listrik & Air | 3     | Rp 4.140.000   | 15,0%        |
...
Jumlah Nominal: naik 73,5% (Rp 7.555.000 → Rp 13.110.000).
Naik paling besar: Transport — naik 310,7% (Rp 1.595.000 → Rp 6.550.000).
⚠️ 1 sel berisi rumus tanpa nilai tersimpan (E16) sehingga dianggap kosong ...
⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 18: TOTAL | … ).
```
(Cuplikan diringkas; contoh lengkap: `examples/uji-pembuat-01-biaya-operasional-xlsx.md`.)

## Cara pakai
Kirim/sebutkan lokasi file ke AI agent Anda, lalu tanya seperti biasa:
- "Tolong analisis file Excel ini, ada yang aneh nggak?"
- "Total pengeluaran per divisi berapa? Simpan tabelnya jadi file."
- "Bandingkan omzet cabang bulan Agustus dan September."
- "Rapikan data ini supaya bisa dipakai di Excel."

Tips: skill ini **paling andal untuk tabel rapi** — **satu baris judul kolom** dan **satu baris per
kejadian/transaksi** (lihat `templates/contoh-tabel-rapi.csv`). File berantakan tetap dicoba, tetapi untuk
**laporan berformat** (ada subtotal per kelompok, baris Total/rekap di tengah, rincian Tunai/QRIS di bawah
total, dua tabel dalam satu sheet, cetakan bank multi-halaman) AI diarahkan **meminta konfirmasi Anda**
sebelum memberi angka final — tata letak laporan sangat beragam, jadi pengecekan singkat oleh Anda tetap perlu.

## Syarat
- File `.xlsx` atau `.csv` (≤ 50 MB). File `.xls` lama: buka di Excel lalu *Save As → .xlsx*.
- Python 3 di komputer (biasanya sudah ada di Mac/Linux; Windows: pasang gratis dari python.org).
  Tidak perlu paket tambahan, akun, atau API key. Tanpa Python pun skill tetap memandu langkah
  manual dengan rumus Excel yang setara.

## Instalasi singkat
Salin folder `analisis-excel` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (jujur):**
- **Uji OpenClaw, v1.0.17** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 7,25 tanpa skill menjadi 8,75 dengan skill (skala 10), pada dua skenario (laporan biaya `.xlsx` dan CSV gaji yang berisi baris subtotal serta data pribadi). Pembeda: semua persen diambil dari skrip hitung (bukan dikira AI), bagian "Perlu dicek" ikut dilaporkan, dan data pribadi diingatkan. Tanpa skill, agent memasang paket tambahan tanpa bertanya dan tidak mengingatkan soal data pribadi di file gaji.
- Catatan jujur: AI tanpa skill di uji ini juga menghitung total dengan benar. Pada uji pertama, AI dengan skill sempat menulis dua persen hasil hitungannya sendiri yang salah; perbaikannya (semua persen wajib dari skrip) lulus di uji ulang.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah data saya dikirim ke internet?**
Tidak oleh skill ini. Perhitungan berjalan di komputer Anda lewat skrip Python. Bila file berisi
data pribadi (NIK, No HP, gaji), skill akan mengingatkan dan hanya menampilkan ringkasan. Isi yang
Anda tanyakan ke AI tetap diproses layanan AI yang Anda pakai, seperti biasa.

**Bisa membaca file Excel dengan banyak sheet?**
Bisa. Skill menyebutkan sheet apa saja yang ada dan sheet mana yang dianalisis; Anda tinggal
bilang "pakai sheet Rekap". Bila datanya dipecah satu sheet per bulan/kuartal, bilang saja
"gabungkan semua sheet" — total Januari–September dihitung sekaligus, baris TOTAL tiap sheet dibuang.

**Kenapa file CSV saya ditolak "Jumlah kolom tidak cocok"?**
Aturannya sederhana: setiap baris harus punya kolom sebanyak judul kolom. Bila satu baris kolomnya
kurang (ada sel terlewat) atau lebih (ada koma di dalam teks tanpa tanda kutip), angkanya bisa masuk
ke kolom yang salah dan totalnya keliru. Daripada memberi angka salah diam-diam, skill menyebut nomor
baris dan isinya agar Anda bisa membetulkannya. Kolom kosong di ujung kanan dan alamat/catatan yang
ditulis beberapa baris dalam satu sel tetap boleh, begitu juga kolom paling kanan yang sering
dikosongkan (mis. "Catatan") walau komanya tidak diketik — selama isi baris tidak bergeser. Pesan
galat menyebut kemungkinan penyebab (sel terlewat di tengah, koma tanpa tanda kutip, tanda kutip
nyasar, catatan di tengah tabel) dan langkah memperbaikinya.

**File ekspor Shopee/Tokopedia/mutasi bank saya ada baris Total, saldo, dan "Dicetak oleh…" di bawahnya. Bisa dibaca?**
Umumnya bisa. Baris yang **jelas** bukan data — Total/Grand Total/Rata-rata/Saldo Akhir dan catatan di bawah
tabel, Saldo Awal di atas tabel, sel berumus SUM/AVERAGE di Excel — tidak dihitung, dan skill menyebutkan
baris mana saja beserta isinya. Baris yang **mungkin** total (mis. angka tanpa keterangan yang kebetulan
sama dengan jumlah di atasnya) tidak dibuang diam-diam: skill tetap menghitungnya, memberi peringatan
tegas, menunjukkan total DENGAN dan TANPA baris itu, lalu menanyakannya kepada Anda. Ini
juga berlaku untuk baris "Jakarta Total" hasil Excel *Data › Subtotal* yang disimpan sebagai CSV dan
rincian pembayaran (Tunai/QRIS) di bawah "Total Penjualan". Judul kolom yang berulang tiap halaman dan
"Halaman 1 dari 2" dilewati; bila ada **tabel kedua** dengan judul kolom berbeda, skill berhenti dan
menyebut baris awalnya agar kedua tabel tidak tercampur. Juga baris subtotal/total yang
**terisi lengkap** (mis. "Subtotal Cabang Bekasi" dengan tanggal, qty, dan omzet), hasil PivotTable (tabel ringkasan Excel) yang disalin
sebagai nilai, dan tabel **tanpa baris judul kolom** (baris pertama tidak lagi hilang diam-diam).
Ada juga **pengaman silang**: bila file Anda punya baris Total/Grand Total, skill mencocokkan
angkanya dengan hasil hitungan. Cocok → disebutkan (lebih yakin). Beda (mis. hasil tepat 2× Grand Total
karena subtotal ikut terhitung) → peringatan tegas di atas hasil beserta kedua angkanya. Bila justru **Total di file Anda yang keliru** (mis. angka yang tersimpan sebagai teks tidak ikut dijumlah
Excel), skill memberi tahu baris mana penyebabnya dan tidak menyodorkan angka file yang salah.

**Apakah bisa memprediksi penjualan bulan depan atau analisis statistik rumit?**
Tidak. Skill ini fokus menjawab pertanyaan dari data yang sudah terjadi (total, rata-rata, tren,
perbandingan). Untuk prediksi/statistik lanjut, gunakan jasa analis data.

## Riwayat perubahan

Versi terkini: **1.0.17**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
