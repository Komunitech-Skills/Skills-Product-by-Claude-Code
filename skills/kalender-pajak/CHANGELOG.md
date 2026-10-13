# Riwayat perubahan — kalender-pajak

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi
- **1.0.7** (1 Okt 2026) — revisi temuan uji OpenClaw: opsi `--omzet-bulanan`/`--omzet-setahun` menghitung kapan omzet kumulatif orang pribadi melewati Rp500 juta dan tanggal setoran pertamanya (tidak lagi ditebak AI); AI dilarang menyebut kode setor (KAP-KJS) selain deposit pajak 411618-100; rujukan ke skill hitung lain kini bersyarat ("bila terpasang"); script dijalankan dari subfolder `scripts/` di folder skill. 67 uji otomatis lulus (5 baru).
- **1.0.6** (30 Sep 2026) — koreksi keterangan kebijakan khusus tahun pajak 2025: KEP-55/PJ/2026 **bukan** perpanjangan. Jatuh tempo SPT Tahunan orang pribadi tetap 31 Mar 2026; yang dihapus hanya sanksi denda/bunga bila lapor/bayar s.d. 30 Apr 2026. Badan diberi catatan KEP-71/PJ/2026 (jatuh tempo tetap, sanksi dihapus s.d. 1 bulan setelah jatuh tempo). Rujukan diganti ke sumber resmi DJP (pajak.go.id). Tidak ada tanggal tenggat yang berubah.
- **1.0.3** (26 Sep 2026) — SPT Tahunan disesuaikan dengan naskah resmi PMK 81/2024: batasnya diatur Ps. 169 dan tidak bergeser meski hari libur, jadi kini hanya satu tanggal yang ditampilkan (tampilan "dua kemungkinan tanggal" dihapus) dengan catatan "lapor lebih awal". Rujukan pasal diperbaiki (Ps. 172/173 bukan dasar SPT Tahunan); label PERLU REVIEW dihapus untuk butir yang kini terverifikasi (mis. PPh 25 dianggap lapor saat setor, Ps. 171 ayat 10). Tidak ada tanggal tenggat yang berubah.
- **1.0.2** (25 Sep 2026) — perbaikan kecil dari uji ulang: batas unggah faktur (tgl 20) atau tenggat lain yang tidak bergeser dan jatuh di hari libur kini menyebut hari kerja sebelumnya (mis. 20 Mei 2027 → unggah paling aman Jumat 14 Mei 2027); SPT Tahunan yang jatuh di hari libur menampilkan dua kemungkinan tanggal (dasar Ps. 173 ayat 1 masih PERLU REVIEW); file libur buatan sendiri dilabeli "data libur dari pengguna" dan peringatan tahun tanpa data resmi tetap tampil. Tidak ada tanggal tenggat yang berubah.
- **1.0.1** (25 Sep 2026) — revisi temuan uji independen: tambah batas unggah faktur pajak keluaran tgl 20 untuk PKP (PER-11/PJ/2025); klaim pengingat Google Calendar & impor ulang diluruskan + opsi acara pengingat terpisah; keterangan libur berkoma tidak terpotong; mode "N hari ke depan" menyebut tenggat berikutnya; label alasan geser lebih jelas; output menyebut cakupan periode & sumber data libur; dasar pasal pergeseran setor diperbaiki (Ps. 100 PMK 81/2024).
- **1.0.0** (25 Sep 2026) — versi awal.

_Bukan nasihat pajak. Hasil adalah alat bantu jadwal; setoran dan pelaporan tetap lewat Coretax/DJP._

## Catatan revisi 1.0.7 (2026-10-01)
- Kapan omzet kumulatif melewati Rp500 juta kini **dihitung script** dari omzet per bulan atau perkiraan setahun (contoh: omzet 600 juta setahun merata → kumulatif Oktober tepat Rp500 juta, baru melewati di November; setoran pertama Selasa 15 Desember 2026).
- AI tidak boleh menyebut kode setor (KAP-KJS) selain deposit pajak 411618-100 (temuan uji: model mengarang "KAP 411125", padahal itu PPh 25/29).
- Rujukan ke `pph-final-umkm`/`pph21-ter`/`hitung-ppn` ditulis "bila terpasang".
