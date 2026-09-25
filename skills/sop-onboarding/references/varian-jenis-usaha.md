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
