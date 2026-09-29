# Uji banding pesaing (penguji independen Akun B, 26 September 2026)

Kata kunci dicari: "Actual Budget MCP server", "actualbudget agent skill SKILL.md", "clawhub actual budget skill".
Pesaing hanya **dibaca untuk dinilai** (dokumentasi publik); tidak disalin dan **tidak dijalankan** (keduanya butuh
server Actual + kata sandi + paket npm; menjalankan kode pihak ketiga di luar cakupan uji ini).

| Pesaing | Sumber | Sinyal |
|---|---|---|
| `actual-budget` (thisisjeron) | ClawHub https://clawhub.ai/thisisjeron/skills/actual-budget , ringkasan https://clawskills.sh/skills/thisisjeron-actual-budget | ±3.000 unduhan, v1.0.2 (Feb 2026), berstatus "Suspicious" di OpenClaw |
| `actual-mcp` (s-stefanov) | https://github.com/s-stefanov/actual-mcp | ±238 bintang, MIT, server MCP |

## Skenario normal pertama: "Ini mutasi BCA Agustus, masukin ke Actual ya."
| Kriteria | thisisjeron/actual-budget | actual-mcp | **actual-budget-usaha** |
|---|---|---|---|
| Setup | Server Actual + URL + password + sync ID + `npm install @actual-app/api` | Node.js + server/password atau data dir; `--enable-write` untuk menulis | Python standar saja, tanpa akun/jaringan |
| Mutasi CSV bank Indonesia (`'01/08`, CR/DB, `1.500.000,00`, PEND, saldo awal/akhir, cp1252) | Tidak dibahas; agent harus menulis sendiri | Tidak ada impor file CSV | Ya, teruji 4 pola bank + cek saldo |
| Kategori usulan & baris ragu (tarik tunai, top up, marketplace, dobel, pinjaman) | Aturan payee Actual (harus dibuat dulu) | Tidak | Ya, bahasa Indonesia, ditanyakan sekali |
| Ringkasan sisa anggaran & jebol | Lewat API (angka Actual sendiri) | Tool `monthly-summary`/budget vs actual | Dari db.sqlite read-only, sama persis dengan `getBudgetMonth` (diuji) |
| Keamanan | Menulis ke budget lewat API/bank sync; flag "Suspicious" | Bisa menulis bila diaktifkan | Hanya baca; impor diklik pengguna |
| Bahasa & konteks lokal | Inggris | Inggris | Indonesia, Rupiah, bank lokal, Telegram pemilik |
| Actual desktop tanpa server | Tidak | Sebagian (data dir) | Ya (tujuan utama) |

## Penilaian
- **Kelebihan pesaing:** membaca angka langsung dari mesin Actual (tidak perlu meniru rumus), bisa menulis
  (buat transaksi/aturan/jadwal), bank sync, mendukung Actual versi server/browser. Skill kita tidak bisa membaca
  Actual versi web kecuali lewat Export.
- **Untuk pembeli sasaran (awam, UMKM Indonesia, mutasi BCA/BRI/Mandiri/BNI):** skill kita unggul jelas pada tugas
  skenario ini — pesaing tidak punya pengurai mutasi lokal sama sekali dan butuh setup server yang berat.
- Tidak ada bukti skill kita kalah. Catatan jujur: perbandingan berbasis dokumentasi, bukan eksekusi berdampingan.

Pelajaran (ditulis dengan cara sendiri, bukan disalin): pertimbangkan dukungan membaca file Export (.zip)
langsung dan/atau jalur opsional untuk Actual server, karena pesaing melayani segmen itu.
