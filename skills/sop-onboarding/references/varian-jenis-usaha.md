# Varian Onboarding per Jenis Usaha

Dipakai untuk menyesuaikan checklist, buku saku, dan jadwal di langkah kerja SKILL.md. Sesuaikan pos yang
relevan, hapus yang tidak berlaku, dan tandai `[isi: ...]` untuk hal yang khusus usaha pengguna.

## Toko / retail
- Dokumen tambahan: pelatihan mesin kasir/aplikasi kasir, SOP retur & tukar barang.
- Buku saku: aturan seragam & tanda pengenal, jam buka-tutup toko, prosedur hitung kas awal/akhir shift.
- Shift: umumnya 1-2 shift, penanggung jawab per shift = kepala toko/supervisor shift.
- Buddy: kasir/pramuniaga senior.

## Kafe / restoran
- Dokumen tambahan: sertifikat kesehatan/food handler bila disyaratkan daerah, pelatihan HACCP dasar
  (rujuk `sop-writer` untuk SOP kebersihan dapur bila belum ada).
- Buku saku: standar kebersihan & higiene, aturan cicip menu, penanganan alergi pelanggan, jam sibuk.
- Shift: 2-3 shift umum (pagi/siang/malam); penanggung jawab = kepala shift/supervisor.
- Buddy: staf dapur/pelayan senior sesuai posisi.

## Bengkel
- Dokumen tambahan: pelatihan K3 dasar (alat pelindung diri, penanganan bahan kimia/oli), asuransi
  tambahan bila ada risiko kerja tinggi (⚠️ K3 teknis di luar cakupan, rujuk ahli K3/Disnaker).
  Perangkat kerja termasuk alat servis, seragam kerja, sepatu safety.
- Buku saku: SOP keselamatan kerja dasar, prosedur klaim garansi, aturan penanganan keluhan pelanggan.
- Shift: umumnya jam kerja tetap (bukan shift); penanggung jawab = kepala mekanik/pemilik.
- Buddy: mekanik senior.

### Contoh lengkap: bengkel
**Input pengguna:** "Bengkel motor saya di Solo terima mekanik baru namanya Budi, kontrak PKWT 6 bulan,
mulai kerja Jumat 25 Desember 2026, kerja 6 hari seminggu (jam kerja tetap, bukan shift)."

Tanggal mulai (25 Desember 2026) kebetulan **Hari Natal** — jatuh di hari libur nasional bawaan.
Hasil nyata `python3 scripts/jadwal_onboarding.py --mulai "25 Desember 2026" --hari-kerja 6 --jenis pkwt
--nama "Budi, Mekanik"`:
```
> ⚠️ Tanggal mulai 25 Desember 2026 jatuh di hari libur/akhir pekan (bukan hari kerja). H1 TIDAK otomatis
  digeser -- konfirmasi ke pengguna, saran: geser ke hari kerja berikutnya, 26 Desember 2026.

| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
|---|---|---|---|---|---|
| Hari pertama (H1) | 25 Desember 2026 | 25 Desember 2026 | Tidak | Pemilik/Atasan langsung | ... |
| Akhir minggu 1 | 31 Desember 2026 | 31 Desember 2026 | Tidak | Buddy/rekan pendamping | ... |
| Checkpoint 30 hari | 23 Januari 2027 | 23 Januari 2027 | Tidak | Atasan langsung | ... |
| Checkpoint 60 hari | 22 Februari 2027 | 22 Februari 2027 | Tidak | Atasan langsung | ... |
| Checkpoint 90 hari | 24 Maret 2027 | 24 Maret 2027 | Tidak | Pemilik/Atasan | Evaluasi akhir orientasi |
| Masa percobaan | - | - | Tidak | - | Tidak berlaku untuk PKWT |
```
Karena **PKWT**, tidak ada baris batas hukum/evaluasi masa percobaan — PKWT dilarang mensyaratkan masa
percobaan (UU 13/2003 Pasal 58 jo. UU 6/2023; PP 35/2021 Pasal 12), checkpoint 30/60/90 di atas hanya
pemantauan kinerja biasa. Agent **tidak boleh menggeser H1 sendiri**: sampaikan peringatan apa adanya ke
pengguna dan tanyakan apakah tetap 25 Desember (bengkel buka Natal) atau digeser ke 26 Desember. Varian
bengkel: buku saku memuat SOP keselamatan kerja & prosedur klaim garansi; buddy = mekanik senior; formulir
evaluasi pakai versi PKWT (`templates/formulir-evaluasi-orientasi-pkwt.md`).

## Klinik / layanan kesehatan
- Dokumen tambahan: STR/SIP untuk tenaga medis (dokter, perawat, bidan — **wajib**, di luar cakupan skill
  ini, arahkan ke bagian legal/Dinkes), sertifikat vaksinasi/kesehatan staf non-medis.
- Buku saku: SOP alur pasien (rujuk `sop-writer`), kerahasiaan rekam medis (UU 27/2022 PDP + etika
  profesi — **jangan buat materi diagnosis/skrining medis**, itu di luar cakupan skill ini dan skill
  `edukasi-pasien-klinik`).
- Shift: umumnya 2-3 shift; penanggung jawab = kepala klinik/dokter penanggung jawab.
- Buddy: staf administrasi/perawat senior.
- Catatan: onboarding untuk staf **non-medis** (admin, kasir, resepsionis) memakai template standar
  skill ini. Untuk kompetensi tenaga medis (sertifikasi, hak praktik), arahkan ke bagian legal/HR klinik.

## Kantor jasa (konsultan, agensi, kantor administrasi)
- Dokumen tambahan: perjanjian kerahasiaan (NDA) bila menangani data klien sensitif, akun email/tools
  kerja (mis. Google Workspace, Slack, aplikasi proyek).
- Buku saku: jam kerja fleksibel/WFH bila ada, aturan penggunaan data klien, kode etik komunikasi klien.
- Shift: umumnya jam kantor tetap (mis. 08.00-17.00); penanggung jawab = manajer langsung.
- Buddy: rekan satu tim/divisi.

## Gudang / logistik
- Dokumen tambahan: pelatihan penggunaan alat (forklift/hand pallet bila ada — sertifikasi operator alat
  berat di luar cakupan, rujuk penyedia pelatihan bersertifikat), APD (sepatu safety, sarung tangan).
- Buku saku: SOP terima & kirim barang (rujuk `sop-writer`), aturan keselamatan gudang, prosedur barang
  rusak/hilang.
- Shift: umumnya 2 shift atau shift malam untuk gudang 24 jam; penanggung jawab = kepala gudang/supervisor
  shift.
- Buddy: staf gudang senior.

## Semua jenis usaha dengan shift
- Jadwal onboarding (H1, minggu 1, 30/60/90 hari) tetap sama; sesuaikan **penanggung jawab per shift**
  bila karyawan baru masuk di shift tertentu — buddy sebaiknya di shift yang sama minimal 2 minggu pertama.
- Bila hari kerja 6 hari/minggu, pakai `--hari-kerja 6` di script `jadwal_onboarding.py` agar Sabtu
  dihitung hari kerja.
- Cuti bersama (SKB 3 Menteri) bersifat **fakultatif** bagi pekerja swasta — bila usaha pengguna tetap
  buka/kerja saat cuti bersama, tambahkan `--cuti-bersama-hari-kerja` supaya tanggal itu dihitung sebagai
  hari kerja biasa; default-nya tetap dihitung libur (lihat SKILL.md langkah 3).

## Target per jabatan (contoh, untuk `templates/panduan-buddy.md` bagian C)
Contoh realistis, bukan patokan wajib — sesuaikan dengan kondisi usaha pengguna dan tanyakan bila target
spesifik (angka omzet/unit) belum disebutkan; jangan mengarang angka.

| Jabatan | Target 30 hari | Target 60 hari | Target 90 hari |
|---|---|---|---|
| Kasir/pramuniaga toko | Hafal SOP kasir & retur, transaksi tanpa dampingan | Rata-rata waktu layani sesuai standar toko, tidak ada selisih kas berulang | Bisa menangani shift sendiri tanpa supervisi langsung |
| Barista/staf kafe | Hafal menu & SOP kebersihan, buat pesanan standar tanpa dampingan | Konsisten rasa/tampilan sesuai standar, tangani jam sibuk dengan bantuan | Bisa memimpin shift kecil/tanpa dampingan langsung |
| Mekanik/teknisi bengkel | Paham SOP keselamatan dasar & alur servis, kerjakan servis ringan didampingi | Kerjakan servis ringan-menengah mandiri, sedikit revisi | Tangani antrian servis harian dengan supervisi minimal |
| Admin/resepsionis klinik | Paham alur pendaftaran pasien & rekam medis dasar (non-diagnosis) | Layani pendaftaran & jadwal mandiri, minim kesalahan input | Bantu proses klaim/administrasi lanjutan dengan supervisi minimal |
| Staf admin kantor jasa | Paham SOP dokumen & tools kerja tim, selesaikan tugas terstruktur dengan arahan | Selesaikan tugas rutin mandiri, komunikasi klien dasar terpantau | Pegang sebagian tugas/klien dengan supervisi ringan |
| Staf gudang | Paham SOP terima/kirim barang & K3 dasar, kerja didampingi | Kerja mandiri untuk tugas rutin, minim selisih stok | Bisa menangani proses gudang harian tanpa dampingan langsung |
