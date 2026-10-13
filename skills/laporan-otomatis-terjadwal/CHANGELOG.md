# Riwayat perubahan — laporan-otomatis-terjadwal

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.1.9 (2026-10-13)
- Uji bot Telegram asli: balasan untuk pengguna awam masih memuat kata internal (token, Gateway, nama perintah mentah). Kini ada aturan bahasa di Format output SKILL.md: pakai "kunci akses", "bot", "jadwal", "pengaturan"; perintah teknis hanya bila diminta. Logika dan script tidak berubah.

## Catatan revisi 1.1.8 (2026-10-12)
- Uji Telegram: file CSV ada di folder pribadi pengguna (`~/laporan/masuk/...`) tetapi agent hanya mencari di folder kerja agent lalu menolak. Kini pencarian berurutan: folder yang disebut pengguna, folder kerja agent, lalu folder pribadi (`laporan/masuk`, `Dokumen/Laporan-AI/masuk`, Documents, Downloads). Bila tetap tidak ketemu, agent menampilkan contoh laporan (berlabel CONTOH) dan bertanya satu kali di mana filenya, bukan menolak.
- SKILL.md dirampingkan (checklist & batasan diringkas) agar tetap di bawah 300 baris; logika script tidak berubah.

## Catatan revisi 1.1.7 (2026-10-01)
- Uji ulang OpenClaw 2026-10-01: satu sesi mencoba kirim pesan uji Telegram tanpa "ya" lalu kehabisan waktu; sesi lain mengintip secrets/database OpenClaw. Kini ada **Aturan aksi** di awal SKILL.md: tidak ada kirim pesan (termasuk uji kirim) dan tidak ada jadwal sebelum "ya" atas ringkasan rencana (isi laporan, jam, kanal tujuan, plus satu uji kirim).
- Cek kanal hanya lewat `openclaw channels status` (perintah resmi, tidak menampilkan kredensial) atau bertanya ke pemilik; dilarang membaca file kredensial/secrets/token/`openclaw.json`/database/log OpenClaw.
- Kanal belum siap atau perintah ditolak → panduan singkat lalu berhenti, tanpa mencoba-coba; maksimal satu cek kanal per giliran agar alur ringkas dan tidak kehabisan waktu.

## Catatan revisi 1.1.6 (2026-10-01)
- Uji OpenClaw 2026-10-01: agent sempat langsung memanggil `cron.add`. Kini urutan wajib sebelum membuat jadwal (CLI maupun tool `cron.add`): cek kanal tujuan tersedia (`openclaw channels status`), tampilkan ringkasan jadwal, tunggu "ya" — "lanjut" sebelum ringkasan bukan persetujuan.
- Label hitungan penjualan diperbaiki: "57 nota / 110 pcs" (atau "N baris penjualan" bila tidak ada kolom nota), bukan "57 item". Total pcs dihitung dengan script dari hasil `rekap-penjualan-csv` (`--top 1000`).
