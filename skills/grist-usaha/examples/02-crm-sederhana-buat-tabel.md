# Skenario 2 (normal) — Rancang & buat tabel CRM/Pelanggan lewat REST API

**Penguji:** Akun B (independen). Server REST Grist **tiruan** ditulis sendiri oleh penguji
(`ujiku/server_tiruan_independen.py`, bukan menyalin `tests/uji_regresi.py`), meniru bentuk
respons resmi grist-core (endpoint `/api/orgs`, `/api/orgs/{id}/workspaces`,
`POST /api/docs/{docId}/tables`).

## Permintaan pengguna
> "Buatkan tabel pelanggan sederhana buat CRM toko saya di dokumen 'Toko Berkah'."

## Alur
```bash
python3 scripts/grist.py cek
python3 scripts/grist.py pola tampilkan pelanggan
python3 scripts/grist.py buat-tabel pelanggan --dokumen "Toko Berkah" --tabel Pelanggan
# (pratinjau ditunjukkan ke pengguna, pengguna jawab "ya")
python3 scripts/grist.py buat-tabel pelanggan --dokumen "Toko Berkah" --tabel Pelanggan --ya
```

## Keluaran nyata (ringkas)
- `cek` → menampilkan dokumen "Toko Berkah Jaya" (docId `docTOKOB1`) yang bisa diakses kunci.
- `pola tampilkan pelanggan` → 6 kolom biasa + 1 kolom rumus (`TeleponRapi`, disebut TIDAK
  dibuat otomatis, diarahkan ke `references/rumus-umum.md`).
- **Tanpa `--ya`**: mencetak PRATINJAU, tidak memanggil server sama sekali (dicek: log server
  tiruan kosong sebelum `--ya`), lalu berhenti dengan pesan "Belum dibuat".
- **Dengan `--ya`**: memanggil `POST /api/docs/docTOKOB1/tables`, server tiruan membalas
  `{"tables":[{"id":"Pelanggan"}]}`, script mencetak `BERHASIL: tabel 'Pelanggan' dibuat di
  Grist.` + arahan manual menambah kolom rumus.

## Temuan
- Pola konfirmasi dua tahap (pratinjau → `--ya`) benar-benar mencegah tulis tidak sengaja: sudah
  diverifikasi tidak ada request POST terkirim sebelum `--ya` diberikan.
- Kolom rumus sengaja tidak dibuat otomatis lewat API (didokumentasikan jelas alasannya di
  SKILL.md: tipe kolom formula lewat REST API grist-core belum diverifikasi pembuat terhadap
  server sungguhan) — pilihan yang jujur dan aman, meski berarti pengguna masih perlu 1 langkah
  manual di Grist untuk tiap kolom rumus.

## Hasil
Sesuai harapan.
