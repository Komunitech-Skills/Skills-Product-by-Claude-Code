# Uji ulang 05 — Kalender pajak Oktober, info kurang (kalender-pajak 1.0.7)

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech` (jawaban dilayani `claude-sonnet-5`). Home baru `sol2-konsultan` (paket skill solusi, dibuat ulang lewat script reset sebelum skenario). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama ([05-kalender-pajak-info-kurang.md](05-kalender-pajak-info-kurang.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran).

## Pesan member (giliran 1)
```
kapan aja saya harus bayar sama lapor pajak bulan oktober ini? biar ga kena denda
```
## Pesan member (giliran 2, sama dengan uji pertama)
```
saya freelancer konsultan, orang pribadi. pakai yang 0,5% itu, belum PKP, nggak punya karyawan. omzet setahun kira2 600 juta.
```

## Giliran 1 — alat `read, tool_search, exec, memory_search, tool_call` (23 dtk)
> Belum ada data profil usaha kamu tersimpan di sistem saya, jadi saya perlu konfirmasi dulu biar kalender pajaknya pas (bukan asal tebak):
>
> 1. Kamu orang pribadi atau badan usaha (PT/CV/koperasi)?
> 2. Pakai PPh final 0,5% (omzet usaha) atau pembukuan/tarif umum?
> 3. Sudah PKP (pungut PPN) atau belum?
> 4. Punya karyawan yang digaji, atau pernah bayar jasa/sewa yang kena potong PPh 23/4(2)?
>
> Jawab nomornya aja boleh singkat (misal: "1 OP, 2 final 0,5%, 3 belum, 4 nggak ada karyawan") — nanti langsung saya buatkan jadwal setor & lapor bulan Oktober ini lengkap dengan tanggal pastinya.

## Giliran 2 — alat `exec` (38 dtk)
> Profil kamu: **orang pribadi, PPh final 0,5% (PP 55/2022), belum PKP, tanpa karyawan**, omzet ±Rp600 juta/tahun.
>
> **Kabar baik untuk Oktober ini: kemungkinan besar belum ada yang perlu disetor.**
>
> Kenapa: PPh final 0,5% untuk orang pribadi baru mulai dipungut setelah omzet kumulatif tahun berjalan **melewati Rp500 juta**. Kalau omzet Rp600 juta kamu dibagi rata per bulan (±Rp50 juta/bulan):
>
> | Bulan | Omzet | Kumulatif |
> |---|---|---|
> | Jan–Sep 2026 | 50jt/bln | sampai Sep = Rp450 juta |
> | Okt 2026 | 50jt | kumulatif Rp500 juta (pas, belum lewat) |
> | **Nov 2026** | 50jt | kumulatif **Rp550 juta → LEWAT Rp500 juta** |
> | Des 2026 | 50jt | Rp600 juta |
>
> → Setoran pertama baru untuk **masa November 2026**, paling lambat **Selasa, 15 Desember 2026** (hanya dari porsi omzet November yang melebihi Rp500 juta, yaitu Rp50 juta).
>
> **Jadi untuk bulan Oktober 2026 ini: tidak ada tenggat setor/lapor** (asumsi omzet rata per bulan). Karena belum PKP dan tanpa karyawan, juga tidak ada PPN atau PPh 21 yang perlu dipikirkan.
>
> ⚠️ Catatan penting:
> - Ini hitungan **asumsi omzet rata per bulan**. Kalau omzet kamu tidak rata (misal September kemarin dapat proyek besar), bulan "lewat Rp500 juta"-nya bisa maju — kalau mau, kasih tahu saya omzet riil per bulan sejak Januari dan saya hitung ulang persis.
> - Besaran pajaknya (0,5% dari porsi yang kena) tidak saya hitung di sini — kalau mau dihitungkan, bilang saja.
> - Kode billing dibuat sendiri di Coretax (menu Pembayaran) saat sudah waktunya setor.
> - Ini bukan nasihat pajak resmi — kalau ragu, cek juga ke AR/KPP atau Kring Pajak 1500200.
>
> Mau saya buatkan juga kalender sampai akhir tahun (Okt–Des) atau pengingat otomatis ke Telegram menjelang 15 Desember nanti?

## Verifikasi independen
Penguji menjalankan `kalender_pajak.py --profil op-umkm --tahun 2026 --bulan-mulai 10 --jumlah-bulan 1 --omzet-setahun 600000000`: kumulatif Okt = 500.000.000 (belum lewat), Nov = 550.000.000 → masa pertama wajib setor November 2026, batas **Selasa, 15 Desember 2026** (Python: 15-12-2026 = Selasa ✔). Omzet Nov yang kena = 50 jt ✔. Tenggat 15 Okt 2026 (masa Sep) di script bertanda "hanya bila ada PPh terutang"; dengan asumsi rata, Sep kumulatif 450 jt → tidak terutang, jadi "Oktober tidak ada tenggat" konsisten ✔.

## Penilaian
- **Cacat lama hilang: YA.** (1) Kesimpulan ambang tidak lagi ditebak: dulu *"kemungkinan besar sudah melewati ambang Rp500 juta sebelum September"* (salah), kini dihitung script: *"Okt … Rp500 juta (pas, belum lewat) … Nov … LEWAT … paling lambat Selasa, 15 Desember 2026"*. (2) Tidak ada kode KAP karangan; hanya *"Kode billing dibuat sendiri di Coretax"*. (3) Tidak ada rujukan ke skill yang tidak terpasang.
- **Regresi:** tidak ada. Kekurangan kecil yang tersisa: batas 7 tahun tarif 0,5% untuk OP tidak disinggung (versi tanpa skill di uji pertama menyebutnya); asumsi omzet rata dinyatakan jelas dan member diminta omzet riil — baik.
- **Skor: 8,5/10** (uji pertama SESUDAH: 7).
