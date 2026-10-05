# Uji banding pesaing (uji independen Akun B)

**Kata kunci dicari:** "vikunja MCP server claude skill agent task manager 2026",
"mcpmarket.com Vikunja Task Management Claude Code Skill features description" (web search, 2026-09-26).

**Kandidat ditemukan (dibaca hanya untuk dinilai, TIDAK disalin):**
- Beberapa **MCP server** Vikunja (crosbyh/vikunja-mcp, Jacob-Tate/vikunja-mcp, 0xK3vin/vikunja-mcp,
  democratize-technology/vikunja-mcp) — ini server MCP (butuh instalasi/konfigurasi koneksi terpisah,
  bukan skill portabel SKILL.md), jadi bukan pembanding format yang sama.
- **"Vikunja Task Management Claude Code Skill"** (mcpmarket.com) — inilah pembanding paling sepadan:
  skill Claude Code untuk Vikunja dengan "intelligent filtering" (quick wins, peringatan tugas
  multi-hari, item pemblokir), manajemen label prioritas/durasi, dan skrip API helper.

## Penilaian berdampingan (skenario: "tugas apa yang telat/perlu perhatian?")

| Aspek | Pesaing (mcpmarket, deskripsi publik) | Skill Komunitech (diuji nyata) |
|---|---|---|
| Bahasa & tanggal Indonesia | Tidak disebutkan; berbasis label Vikunja (durasi/prioritas), bukan parser tanggal bahasa Indonesia | "besok/lusa/Jumat depan/25/10/dst" dihitung otomatis, teruji benar (lihat examples 01-03) |
| Notulen/rangkuman WA → draf tugas | Tidak ada fitur ini disebutkan | Ada (`dari-teks`), diuji 2 skenario berbeda, hasil benar, selalu berstatus DRAF |
| Konfirmasi sebelum menulis | Tidak dijelaskan publik apakah ada gerbang konfirmasi eksplisit | Wajib pratinjau + "ya" tertulis untuk SETIAP tulis (tambah/selesai/tugaskan), diverifikasi nyata di 01/02/05 |
| Keamanan alamat server | Tidak disebutkan pembatasan localhost/HTTPS | Menolak IP publik tanpa flag, menolak domain publik non-HTTPS bahkan dengan flag — diuji nyata (05a/05b) |
| Ringkasan per anggota tim | Tidak disebutkan (fokusnya per-pengguna tunggal, label prioritas/durasi) | `ringkasan` mengelompokkan per PIC + daftar "belum ada PIC" — diuji nyata (01) |
| Uji nyata vs server sungguhan | Deskripsi publik tidak menyebut versi Vikunja yang diuji | Diuji langsung ke Vikunja v2.6.0 asli (SHA-256 dicocokkan), termasuk oleh penguji independen ini |
| Ketergantungan | Tidak jelas dari deskripsi (kemungkinan butuh dependency Python tambahan seperti skill MCP-based lain) | Python standar saja, nol instalasi paket (diverifikasi: `import` hanya modul stdlib) |

## Kesimpulan
Skill Komunitech **unggul untuk target pasar UMKM/profesional Indonesia**: lokalisasi bahasa &
tanggal, mode notulen-WA-ke-draf, dan gerbang konfirmasi/keamanan yang terverifikasi konkret adalah
nilai tambah nyata yang tidak disebutkan pesaing publik yang ditemukan. Pesaing tampak lebih fokus ke
fitur "quick wins"/label durasi ala produktivitas personal (bahasa Inggris), bukan koordinasi tim
kecil Indonesia. Tidak ada indikasi pesaing lebih unggul pada aspek yang diuji di sini → skor tidak
dibatasi maksimal 6 oleh kriteria ini.

Sumber (dibaca untuk dinilai, tidak dikutip/disalin ke materi jualan):
- https://mcpmarket.com/tools/skills/vikunja-task-management
- https://github.com/crosbyh/vikunja-mcp
- https://github.com/Jacob-Tate/vikunja-mcp
- https://github.com/0xK3vin/vikunja-mcp
- https://github.com/democratize-technology/vikunja-mcp
