# 00 - Banding pesaing
Pencarian (29 Sep 2026): "listmonk MCP server github newsletter skill"; "skills.sh OR clawhub listmonk skill SKILL.md newsletter"; awesome-openclaw-skills (kategori email marketing). Tidak ditemukan skill listmonk di ClawHub/skills.sh yang terindeks; hanya skill layanan lain (brevo, lumail, sequenzy).
Pesaing terdekat: **rhnvrm/listmonk-mcp** (MIT, 43 bintang, 11 fork, 18 tool MCP, PyPI). Hanya dibaca untuk dinilai.
| Aspek | listmonk-mcp | listmonk-newsletter (kita) |
|---|---|---|
| Cakupan API | luas (tool CRUD) | fokus alur UMKM |
| Gerbang konfirmasi kirim | tidak disebut | ada (jumlah penerima, uji kirim, sidik isi) - punya celah `--tanpa-uji` |
| Pemeriksaan CSV, persetujuan UU PDP, double opt-in | tidak ada / impor CSV tidak disebut | ada |
| Bahasa Indonesia, panduan pasang, cek isi email | tidak | ya |
| Instalasi | butuh uv/Python + klien MCP | Python standar, tanpa paket |
| Kredensial | env password | file izin 600, tak dicetak |
Putusan: kita menang untuk pembeli awam Indonesia; MCP lebih unggul di kelengkapan endpoint dan komunitas. Skenario 1 (impor) dijalankan hanya secara konseptual untuk pesaing (tidak dipasang: dependensi baru dari sumber luar); penilaian berdasar README.
