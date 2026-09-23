# Kurasi: copyku (ClawHub, @khamalismadie)

Tanggal tinjau: 2026-09-23 · Peninjau: agent kurator · Status: **TUNDA — tidak dapat diaudit**

## 1. Identitas

| Item | Isi |
|---|---|
| Nama | copyku ("AI Copywriting Expert berbahasa Indonesia") |
| URL | https://clawskills.sh/skills/khamalismadie-copyku (tercantum di https://github.com/VoltAgent/awesome-openclaw-skills, kategori `git-and-github`, yang tampaknya salah kategori) |
| Ditemukan lewat | Pencarian "awesome-openclaw-skills Indonesia". Dari sekitar 28 file kategori awesome-openclaw-skills yang di-grep untuk kata "Indonesia/bahasa/UMKM/rupiah/Shopee/Tokopedia/QRIS/BPJS", hanya ini yang relevan untuk bisnis. (Temuan lain: `jadwal-sholat` oleh banghasan, bergantung pada API luar dan tidak relevan untuk bisnis.) |
| Pembuat | @khamalismadie |
| Update terakhir | **Tidak dapat diverifikasi** |
| **Lisensi** | **Tidak dapat diverifikasi.** File LICENSE tidak bisa dibaca. |

### Ringkasan (dari cuplikan hasil pencarian, BUKAN dari membaca file)
Asisten copywriting berbahasa Indonesia dengan tiga mode input (satu kalimat, dipandu langkah demi langkah, atau parameter lengkap). Formula dipilih otomatis per platform (AIDA untuk Instagram, PAS untuk landing page, SSC untuk sales page).

## 2. Audit keamanan (Tahap 3)

**Tidak dapat dilakukan.** Semua jalur baca diblokir proxy egress sesi ini:
- `clawhub.ai` → EGRESS_BLOCKED
- `clawskills.sh` → EGRESS_BLOCKED
- `skills.lc` (mirror) → EGRESS_BLOCKED
- Mirror GitHub `openclaw/skills` (raw) → 404/tidak dapat diakses. `panlm/awesome-skills-deepdive` hanya berisi daftar, bukan isi skill.

Sesuai CLAUDE.md, skill pihak ketiga dianggap **tidak tepercaya** sampai seluruh isinya dibaca. Ekosistem ClawHub juga pernah memuat skill berbahaya.

## 3. Penilaian
- **Kualitas:** tidak dapat dinilai.
- **Tumpang tindih (dari deskripsi):** tinggi dengan `caption-sosmed-umkm`, `broadcast-wa`, dan `listing-marketplace`. Kita juga sudah punya kandidat copywriting berlisensi jelas dan teraudit (`rama-copywriting`, Apache-2.0).
- **Keputusan: TUNDA (anggap TOLAK untuk batch 2026-09-24).** Alasannya: lisensi dan isi tidak terverifikasi, audit keamanan tidak bisa dilakukan, dan nilai tambahnya rendah karena sudah ada alternatif teraudit.
- Tidak dimasukkan ke `rejected/` karena **tidak gagal** audit. Audit hanya belum bisa dilakukan.

## 4. Tindak lanjut (opsional)
Jika pemilik tetap tertarik: buka halaman ClawHub dari jaringan yang tidak diblokir, unduh paketnya untuk **dibaca saja**, periksa file LICENSE (ClawHub dilaporkan memakai MIT-0 untuk skill yang dipublikasikan, tetapi **belum diverifikasi**), lalu audit ulang dengan checklist Tahap 3.
