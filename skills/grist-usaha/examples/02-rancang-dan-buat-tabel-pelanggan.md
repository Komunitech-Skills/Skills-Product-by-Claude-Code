# Contoh 2 — Merancang & membuat tabel dari kalimat bebas (lewat REST API)

**Konteks uji:** REST API dipanggil ke **server Grist TIRUAN** (`tests/uji_regresi.py`,
`ServerGristTiruan` — meniru bentuk respons resmi `app/gen-server/ApiServer.ts` &
`app/server/lib/DocApi.ts`). **Belum diuji ke server `grist-core`/Docker yang sungguhan
menyala** — dicatat apa adanya di `README.md`.

## Percakapan

> **Pengguna:** "Aku baru pasang Grist Docker di rumah, dokumennya namanya 'Data Usaha Saya'.
> Tolong buatkan tabel pelanggan dong, standar aja."

Agent mencocokkan permintaan ke pola **Daftar Pelanggan** (`references/pola-tabel-umkm.md`),
menunjukkan pratinjau dulu:

```
$ python3 grist.py buat-tabel pelanggan --dokumen "Data Usaha Saya"
PRATINJAU — buat tabel 'Pelanggan' di dokumen (docId: docABC123):
  + kolom Nama [Text] (Nama)
  + kolom Telepon [Text] (No. WA/Telepon)
  + kolom Kota [Text] (Kota)
  + kolom Sumber [Text] (Sumber)
  + kolom Catatan [Text] (Catatan)
  + kolom TanggalDaftar [Date] (Tgl Daftar)
  Kolom rumus berikut TIDAK dibuat otomatis (isi manual di Grist setelah tabel jadi,
  tempel rumusnya dari references/rumus-umum.md - lihat SKILL.md kenapa):
    - TeleponRapi -> rumus_wa_rapi (references/rumus-umum.md #1)

Belum dibuat. Jalankan ulang dengan --ya setelah pengguna menjawab 'ya'.
```

**Balasan agent:**

> Saya usulkan tabel **Pelanggan** dengan 6 kolom biasa (Nama, Telepon, Kota, Sumber, Catatan,
> Tgl Daftar) + 1 kolom rumus **WA Rapi** (merapikan nomor WA jadi format `62...` otomatis, akan
> saya bantu tempel rumusnya setelah tabel jadi). Lanjut buat di Grist? (ya/tidak)

> **Pengguna:** "ya"

```
$ python3 grist.py buat-tabel pelanggan --dokumen "Data Usaha Saya" --ya
PRATINJAU — buat tabel 'Pelanggan' di dokumen (docId: docABC123):
  ... (sama seperti di atas) ...
BERHASIL: tabel 'Pelanggan' dibuat di Grist.
Langkah selanjutnya (manual, di layar Grist): tambah kolom rumus di atas lewat
'+ Add Column' > pilih 'Formula' > tempel rumus dari references/rumus-umum.md.
```

**Balasan agent:**

> Tabel **Pelanggan** sudah dibuat di dokumen Anda. Satu langkah manual tersisa: buka Grist →
> klik **+ Add Column** di tabel Pelanggan → pilih **Formula** → beri nama `TeleponRapi` → tempel
> kode ini di kotak formula:
> ```python
> angka = "".join(c for c in str($Telepon) if c.isdigit())
> if angka.startswith("62"):
>     hasil = angka
> elif angka.startswith("0"):
>     hasil = "62" + angka[1:]
> elif angka:
>     hasil = "62" + angka
> else:
>     hasil = ""
> hasil
> ```
> Grist langsung menghitungnya untuk semua baris begitu disimpan.

## Catatan uji
- Endpoint yang dipanggil: `POST /api/docs/{docId}/tables` dengan body
  `{"tables":[{"id":"Pelanggan","columns":[...]}]}` — bentuk ini diambil dari kode sumber
  `app/server/lib/DocApi.ts` (route `POST /api/docs/:docId/tables`).
- Kolom rumus **sengaja tidak dibuat otomatis lewat API** meski secara teknis bisa (field
  `isFormula`+`formula` ada di `_grist_Tables_column`) — karena rumus di `rumus-umum.md` belum
  pernah dijalankan di Grist sungguhan (lihat kejujuran metodologi), jadi lebih aman diserahkan
  ke pengguna/agent untuk ditempel & dicek langsung di kotak formula Grist (yang akan langsung
  menampilkan galat bila ada yang salah).
