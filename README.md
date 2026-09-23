# Komunitech Skills

Koleksi skill siap pakai untuk AI agent, dioptimalkan untuk **OpenClaw**, oleh [komunitech.com](https://komunitech.com).

> ⚠️ **Repo ini PRIVATE dan berisi produk berbayar.** Jangan ubah visibilitas repo menjadi publik
> dan jangan bagikan isi repo di luar tim internal.

## Model distribusi

| Kanal | Akses |
|---|---|
| **Member VIP** | Semua skill (termasuk yang `vip_eksklusif`) + update berkala |
| **Pembelian ecer** | Per skill, hanya skill dengan `tersedia_ecer: true` di `catalog.json` |

Setiap paket yang dikirim ke pembeli diberi **watermark lisensi** (nama/ID pembeli + kode lisensi unik)
agar kebocoran bisa dilacak. Lihat bagian [Build paket](#build-paket).

## Struktur repo

```
skills/
  <id-skill>/
    SKILL.md          # instruksi utama + frontmatter (wajib)
    scripts/          # script pendukung (opsional)
    references/       # dokumen referensi tambahan (opsional)
templates/
  SKILL.template.md   # template untuk skill baru
scripts/
  validate.py         # cek format semua skill & katalog
  build.py            # buat paket ZIP ber-watermark untuk pembeli
catalog.json          # katalog produk: harga, versi, tier
LICENSE               # lisensi komersial (DRAFT)
CONTRIBUTING.md       # panduan membuat skill baru
```

## Daftar skill

Sumber kebenaran daftar skill adalah [`catalog.json`](catalog.json).

| ID | Kategori | Ecer | VIP eksklusif |
|---|---|---|---|
| `caption-sosmed-umkm` | Marketing | ✅ | – |
| `rekap-penjualan-csv` | Bisnis & Data | ✅ | – |

## Instalasi di OpenClaw (untuk pembeli)

1. Ekstrak ZIP yang diterima.
2. Salin folder skill ke direktori skills OpenClaw, misalnya `~/.openclaw/skills/<id-skill>/`
   (atau folder `skills/` di workspace agent).
3. Mulai sesi baru atau restart gateway agar skill terbaca.

> Lokasi folder skill bisa berbeda antar versi OpenClaw. Cek dokumentasi OpenClaw terbaru.

## Build paket

Butuh Python 3.9+ (tanpa dependensi tambahan).

```bash
# Validasi semua skill & katalog
python3 scripts/validate.py

# Paket ecer: satu skill untuk satu pembeli
python3 scripts/build.py --pembeli "Budi Santoso <budi@contoh.com>" --skill caption-sosmed-umkm

# Paket VIP: semua skill untuk satu member
python3 scripts/build.py --pembeli "Member VIP #0123" --vip
```

Hasil ada di folder `dist/` (tidak ikut di-commit). Kode lisensi yang dicetak di terminal
sebaiknya dicatat di sistem penjualan untuk pelacakan.

## Kontribusi

Baca [CONTRIBUTING.md](CONTRIBUTING.md) sebelum menambah atau mengubah skill.
