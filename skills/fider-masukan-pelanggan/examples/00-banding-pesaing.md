# 00 - Uji banding pesaing (penguji independen, 2026-09-29)

Kata kunci dicari: "Fider MCP server feedback board agent skill"; "Canny MCP server OpenClaw skill customer feedback ClawHub"; "skills.sh OR clawhub feedback feature requests SKILL.md canny fider productboard"; "Canny API MCP server github". Sumber: skills.sh/ClawHub (lewat hasil pencarian umum, katalog tidak bisa ditanyai langsung), GitHub, Glama.

## Temuan
| Pesaing | Jenis | Catatan |
|---|---|---|
| ringostat/fider-mcp (github.com/ringostat/fider-mcp, glama.ai) | MCP server untuk Fider, MIT, 19 alat: pos (list/get/create/edit/**delete**/respond), komentar (termasuk **delete**), tag (termasuk **delete**) | 1 bintang, 4 commit. Hanya alat mentah: tanpa pratinjau/izin, tanpa penyamaran data pribadi, tanpa pengecekan duplikat, tanpa ringkasan mingguan, tanpa draf balasan, tanpa bahasa Indonesia; bisa menghapus pos (risiko "sembunyikan keluhan"). Butuh Node/MCP client. |
| opensourceops/canny-mcp-server, mailerlite/canny-mcp-server | MCP untuk Canny (SaaS berbayar) | Bukan Fider; 37 alat, mode baca-saja bawaan (praktik bagus yang layak ditiru), bisa memberi suara. Produk berbeda (berlangganan). |
| Skill SKILL.md khusus Fider di ClawHub/skills.sh | tidak ditemukan | Tidak ada skill Fider atau Canny yang terlihat di hasil pencarian. |

## Perbandingan skenario normal 1 (impor catatan WA)
fider-mcp tidak dijalankan (butuh instalasi paket pihak luar; dinilai dari dokumentasi/README, tidak disalin). Secara fungsi ia setara dengan hasil "tanpa skill" di `00-pembanding-tanpa-skill.md`: satu panggilan create per butir, tanpa perlindungan. Skill Komunitech unggul pada: gerbang pratinjau, penyamaran HP/email, deteksi duplikat, ringkasan mingguan, draf balasan, panduan pasang Fider, konteks Indonesia, Python standar tanpa instalasi. Pesaing unggul pada: cakupan alat luas (edit/hapus, sebagian memang sengaja tidak ada di skill), dan mode baca-saja bawaan pada MCP Canny.

Putusan: **skill menang**; tidak ada pengurangan skor. Catatan pelajaran: pertimbangkan `--baca-saja` global.
