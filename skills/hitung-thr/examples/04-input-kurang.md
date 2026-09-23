# 04 — Input tidak lengkap

**Skenario:** S4 — pengguna tidak memberi tanggal hari raya maupun data karyawan.

**Input pengguna (persis):**
> Hitung THR karyawan saya ya, ada 6 orang

**Output (agent bertanya sekali):**
> Siap. Supaya THR-nya pas sesuai aturan, mohon kirim:
> 1. Hari raya yang mana dan tanggal resminya (mis. Idul Fitri 1448 H — tanggal sesuai SKB libur nasional)? Saya tidak menebak tanggal.
> 2. Untuk tiap karyawan: nama, tanggal mulai kerja, gaji pokok + tunjangan tetap (uang makan/transport harian tidak ikut).
> 3. Statusnya: tetap, kontrak, harian lepas, atau borongan/satuan? Untuk harian/borongan, kirim upah per bulan 12 bulan terakhir.
> 4. (Opsional, untuk potongan pajak) status PTKP tiap orang (TK/0, K/1, dst.) dan rencana tanggal bayar.
> 5. Ada yang sudah berhenti/di-PHK sebelum hari raya? Kalau ada, tanggal berhentinya.
>
> Boleh kirim dalam bentuk tabel/Excel. Kalau mau cepat, kirim minimal nomor 1 dan 2 — sisanya saya anggap karyawan tetap, PPh 21 tidak dihitung.

**Catatan penguji:**
- Satu pesan, bernomor, maks. 5 pertanyaan, ada jalur cepat — sesuai SKILL.md dan prinsip produk.
- Tidak menebak tanggal hari raya (sesuai "Kapan TIDAK digunakan").
