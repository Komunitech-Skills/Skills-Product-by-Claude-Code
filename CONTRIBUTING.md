# Panduan Membuat Skill

## Langkah

1. Salin template:
   ```bash
   mkdir skills/<id-skill>
   cp templates/SKILL.template.md skills/<id-skill>/SKILL.md
   ```
   `id-skill` memakai huruf kecil, angka, dan tanda hubung (contoh: `caption-sosmed-umkm`).
2. Isi `SKILL.md`. Kolom `name` di frontmatter **harus sama** dengan nama folder.
3. Tambahkan entri di `catalog.json`.
4. Jalankan `python3 scripts/validate.py` sampai lolos.
5. Uji di OpenClaw (lihat checklist QA di bawah).
6. Buat Pull Request ke `main`.

## Menulis `description` yang baik

`description` menentukan **kapan agent memakai skill ini**. Agent hanya melihat nama dan
deskripsi sebelum memutuskan memuat skill, jadi:

- Sebutkan **apa** yang dikerjakan dan **kapan** dipakai.
- Cantumkan kata kunci yang mungkin diketik pengguna (bahasa Indonesia *dan* Inggris).
- Maksimal ±1024 karakter, satu baris.

## Prinsip isi skill

- **Ringkas.** Agent sudah pintar; tulis hanya yang tidak ia ketahui: alur kerja, format
  output, aturan bisnis, dan jebakan umum.
- **Instruksi yang bisa dijalankan**, bukan teori.
- **Contoh input → output** untuk hasil yang harus konsisten.
- Detail panjang taruh di `references/` dan rujuk dari `SKILL.md`.
- Script harus jalan dengan **Python standar** atau tool yang dideklarasikan di
  `metadata.openclaw.requires`.
- Jangan pernah menyimpan API key, token, atau data pribadi di skill.

## Checklist QA sebelum rilis

- [ ] `validate.py` lolos
- [ ] Skill terdeteksi oleh OpenClaw (muncul di daftar skill)
- [ ] Agent memuat skill secara otomatis untuk minimal 3 contoh permintaan yang relevan
- [ ] Agent **tidak** memuat skill untuk permintaan yang tidak relevan
- [ ] Output sesuai format yang dijanjikan
- [ ] Script (jika ada) diuji dengan data contoh dan data rusak
- [ ] `versi` di `catalog.json` dinaikkan bila ini update

## Versi

Gunakan semantic versioning di `catalog.json`:
- `PATCH` (1.0.1): perbaikan kecil/typo
- `MINOR` (1.1.0): fitur baru, kompatibel
- `MAJOR` (2.0.0): perubahan besar pada cara pakai
