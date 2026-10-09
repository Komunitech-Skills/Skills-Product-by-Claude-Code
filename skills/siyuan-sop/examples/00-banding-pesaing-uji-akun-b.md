# Banding pesaing (uji Akun B) — skill/MCP SiYuan publik

Dicari lewat WebSearch (bukan ClawHub/skills.sh langsung — akses dibatasi jaringan sesi; dipakai
hasil mesin pencari yang menunjuk ke ClawHub, mcpmarket, lobehub, GitHub). Ditemukan beberapa
pesaing relevan, **hanya dibaca cuplikan hasil pencarian untuk dinilai**, tidak disalin:
- ClawHub: `dazexcl/siyuan-skill` (clawhub.ai/dazexcl/siyuan-skill) — pakai perintah Node.js,
  cek-eksis-lalu-buat/timpa (tanya pengguna soal timpa), curl langsung ke kernel API.
- `unclemicdo/siyuan-mcp-server` (GitHub) — MCP server 22 tools, mendukung "complex SQL queries"
  bebas dari agent, bukan templat tetap.
- `NousResearch/hermes-agent` `optional-skills/productivity/siyuan` — skill produktivitas umum,
  tidak spesifik SOP/FAQ toko.
- `siyuan-note-api` (getclaudeskills.com, NousResearch) — deskripsi "perform complex SQL queries"
  langsung dari instruksi natural language ke SQL.

## Penilaian berdampingan (kriteria: keamanan, lokalisasi, kesiapan pembeli awam Indonesia)
| Kriteria | Pesaing (ClawHub/MCP di atas) | `siyuan-sop` (Komunitech) |
|---|---|---|
| SQL | Beberapa mengizinkan "complex SQL queries" bebas dari agent → celah injeksi bila agent salah susun | Hanya templat SELECT tetap, kata kunci di-escape (diverifikasi §05 Kasus B) |
| Proteksi timpa | Sebagian tanya konfirmasi, tidak semua eksplisit menahan lewat kode keluar terpisah | Kode keluar 7 + `--timpa` wajib eksplisit + `--ya` (diverifikasi §02) |
| Lokalisasi Indonesia | Tidak ada (Inggris, tanpa konteks toko/klinik UMKM) | Bahasa Indonesia penuh, contoh toko/klinik lokal, serah-terima ke `agen-cs-toko`/`balas-chat-cs` |
| Batasan alamat/localhost | Tidak disebut eksplisit di deskripsi hasil pencarian | Ditolak default + wajib https utk jarak jauh (diverifikasi §05 Kasus A) |
| Tanpa setup paket | MCP server perlu instalasi Node/proses MCP terpisah | Python standar saja, tanpa instalasi apa pun |

## Kesimpulan
Untuk target pembeli (pengusaha awam Indonesia, butuh "instan tapi aman"), `siyuan-sop` unggul di
keamanan (SQL templat tetap vs beberapa pesaing mengekspos "complex SQL queries" bebas) dan
lokalisasi penuh — dua hal yang tidak dimiliki pesaing yang ditemukan. Tidak di bawah skor 6 pada
kriteria banding pesaing. **Kata kunci & sumber dicatat sesuai instruksi Tahap 6 poin 5.**
