# Analisis Excel Tanpa Rumus, Tinggal Tanya

**Kirim file Excel/CSV, tanya pakai bahasa biasa, dapat tabel + temuan + saran grafik — angkanya
dihitung komputer, bukan dikira-kira AI.**

## Manfaat
- ✅ **Jawaban langsung dari file Anda:** "total per kategori", "bulan mana paling tinggi",
  "September naik berapa dibanding Agustus", "10 pelanggan terbesar" — tanpa bikin PivotTable
  atau rumus SUMIFS sendiri.
- ✅ **Angka bisa dipercaya:** semua dihitung script (presisi penuh untuk rupiah), baris "TOTAL"
  di bawah tabel otomatis tidak dihitung dua kali, nilai yang aneh dilaporkan lengkap dengan nomor
  barisnya — bukan ditebak diam-diam.
- ✅ **Tahan file berantakan:** judul laporan di atas tabel, sel gabungan (merge), angka
  "Rp 1.234.567,89", tanggal campur "25/09/2026" / "25 Sep 2026" / "2026-09-25", "kopi susu" vs
  "Kopi Susu ", file CSV dari Excel Windows lama — semua ditangani.
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
**Sebelum (AI tanpa skill):** AI membaca sebagian isi file lalu *mengira-ngira* total; baris
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
⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 18).
```
(Contoh lengkap: `examples/uji-pembuat-01-biaya-operasional-xlsx.md`.)

## Cara pakai
Kirim/sebutkan lokasi file ke AI agent Anda, lalu tanya seperti biasa:
- "Tolong analisis file Excel ini, ada yang aneh nggak?"
- "Total pengeluaran per divisi berapa? Simpan tabelnya jadi file."
- "Bandingkan omzet cabang bulan Agustus dan September."
- "Rapikan data ini supaya bisa dipakai di Excel."

Tips: tabel yang paling mudah dianalisis punya **satu baris judul kolom** dan **satu baris per
kejadian** (lihat `templates/contoh-tabel-rapi.csv`). Tapi file yang berantakan pun tetap dicoba.

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

## FAQ
**Apakah data saya dikirim ke internet?**
Tidak oleh skill ini. Perhitungan berjalan di komputer Anda lewat script Python. Bila file berisi
data pribadi (NIK, No HP, gaji), skill akan mengingatkan dan hanya menampilkan ringkasan.

**Bisa membaca file Excel dengan banyak sheet?**
Bisa. Skill menyebutkan sheet apa saja yang ada dan sheet mana yang dianalisis; Anda tinggal
bilang "pakai sheet Rekap". Bila datanya dipecah satu sheet per bulan/kuartal, bilang saja
"gabungkan semua sheet" — total Januari–September dihitung sekaligus, baris TOTAL tiap sheet dibuang.

**Apakah bisa memprediksi penjualan bulan depan atau analisis statistik rumit?**
Tidak. Skill ini fokus menjawab pertanyaan dari data yang sudah terjadi (total, rata-rata, tren,
perbandingan). Untuk prediksi/statistik lanjut, gunakan jasa analis data.

## Riwayat versi
| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.0.1 | 2026-09-25 | Revisi hasil uji independen: gabung beberapa sheet (`--sheet semua` / `"Q1,Q2,Q3"`, kolom `Sheet`, TOTAL per sheet dibuang, beda kolom diperingatkan); CSV bertanda kutip tak tertutup kini GAGAL dengan nomor baris (sebelumnya diam-diam menelan baris); kolom "Nilai terisi" + peringatan sel kosong di `pivot`/`top`; NIK/No HP/email/rekening disamarkan di tabel (opsi `--tampilkan-pribadi`) + peringatan gaji per orang; kategori "4 A" = "4A" digabung & dilaporkan; peringatan duplikat di semua subperintah; nama bulan diurut kronologis; label `banding` dua sheet = nama sheet; pesan-pesan kecil diperhalus. Angka skenario uji 01–03 tidak berubah (dikunci tes). |
| 1.0.0 | 2026-09-25 | Rilis draft pertama. |
