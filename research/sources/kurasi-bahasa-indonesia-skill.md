# Kurasi: ajipurn/bahasa-indonesia-skill

Tanggal tinjau: 2026-09-23 · Peninjau: agent kurator · Status: **menunggu keputusan koordinator/pemilik**

## 1. Identitas

| Item | Isi |
|---|---|
| Nama | bahasa-indonesia (1 skill untuk coding agent) |
| URL | https://github.com/ajipurn/bahasa-indonesia-skill (terdaftar di skills.sh: `ajipurn/bahasa-indonesia-skill`) |
| Ditemukan lewat | Pencarian web "SKILL.md agent skills Indonesia" |
| Pembuat | Aji Purnomo (ajipurn), dengan kontributor "Netta"/ddettaa |
| Update terakhir | 2026-08-23 |
| **Lisensi** | **TIDAK ADA.** Tidak ada file LICENSE, dan README tidak menyebut lisensi. |

### Ringkasan isi
Membuat agent coding membalas dalam bahasa Indonesia yang natural: ragam netral/profesional, profil gaya regional (Jakarta, Jaksel, Bandung, Surabaya, Medan, Makassar, Jawa alus, Banyumasan, dan lain-lain), tingkat tutur, prosa puitis, serta registri 718 bahasa daerah (`languages.json`, 11.822 baris, disinkronkan dari Peta Bahasa Kemendikdasmen). Ada script Node untuk validasi dan evaluasi.

## 2. Audit keamanan (Tahap 3)

| Pemeriksaan | Hasil |
|---|---|
| `scripts/sync-language-registry.mjs` | `fetch("https://petabahasa.kemendikdasmen.go.id/databahasa.php")` lalu menulis `languages.json`. Ini alat pemelihara untuk mengambil data resmi pemerintah, tidak dipanggil oleh SKILL.md, dan tidak mengirim data pengguna. Tidak berbahaya. |
| Script lain | Validasi dan evaluasi lokal. Tidak ada `child_process` atau kredensial. |
| Prompt injection | Tidak ada. SKILL.md justru melarang gaya mengubah instruksi keamanan atau keputusan izin. |
| Karakter tersembunyi | Tidak ada. |

**Hasil: LULUS.**

## 3. Penilaian
- **Kualitas: 7/10** untuk tujuannya (komunikasi coding agent). **Relevansi untuk pengusaha/profesional awam: rendah.** Sasarannya developer.
- **Tumpang tindih:** tidak langsung. Ide "profil gaya regional" bisa menarik untuk caption lokal (misalnya sapaan khas Medan/Makassar), tetapi tetap berisiko stereotip.
- **Keputusan: INSPIRASI SAJA** (tanpa lisensi, dilarang disalin/dijual), dengan prioritas rendah.

## 4. Catatan inspirasi
- Prinsip yang layak diadopsi (sebagai gagasan): "jangan menebak wilayah/suku/tingkat tutur dari nama atau lokasi pengguna" dan "mengenali nama bahasa daerah ≠ mampu menuturkannya; jangan mengarang". Keduanya berguna jika kelak ada skill caption bernuansa daerah.
- Data Peta Bahasa adalah data publik pemerintah. Jika dibutuhkan, ambil langsung dari sumber resmi, bukan dari repo ini.
