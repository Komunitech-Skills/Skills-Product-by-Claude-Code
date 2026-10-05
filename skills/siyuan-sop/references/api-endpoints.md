# Endpoint API SiYuan yang dipakai skill ini

Sumber: dokumentasi resmi `docs/API.md` di https://github.com/siyuan-note/siyuan (berkas
`docs/API.md` pada branch `master`), diverifikasi **2026-09-26**. Semua endpoint memakai metode
**POST**, header `Content-Type: application/json` dan `Authorization: Token <token>`, ke alamat
dasar `http://127.0.0.1:6806` (default resmi). Field di bawah adalah **kutipan struktur**
(nama field), bukan salinan teks penjelasan dokumentasi.

| Endpoint | Field permintaan | Field balasan (`data`) | Dipakai untuk perintah |
|---|---|---|---|
| `/api/notebook/lsNotebooks` | *(tidak ada)* | `notebooks[]` (`id`, `name`, `icon`, `sort`, `closed`) | `daftar-buku`, `cek` |
| `/api/notebook/openNotebook` | `notebook` (id) | - | dipanggil otomatis sebelum `buat` (memastikan buku catatan terbuka) |
| `/api/filetree/getIDsByHPath` | `notebook`, `path` | array id dokumen yang cocok | `baca --notebook --path`, cek path sudah ada sebelum `buat` |
| `/api/filetree/createDocWithMd` | `notebook`, `path` (diawali `/`, tiap tingkat dipisah `/`), `markdown` | id dokumen baru | `buat` |
| `/api/filetree/removeDocByID` | `id` | - | `buat --timpa` (menghapus dokumen lama sebelum membuat yang baru) |
| `/api/block/appendBlock` | `data`, `dataType` (`markdown`/`dom`), `parentID` | daftar operasi | `tambah` |
| `/api/export/exportMdContent` | `id` | `hPath`, `content` (Markdown GFM) | `baca`, `ekspor-basis` |
| `/api/query/sql` | `stmt` (SQL SELECT) | array baris | `cari`, `lama`, `ekspor-basis` (daftar dokumen per buku) |

## Catatan penting yang diverifikasi langsung (bukan hanya dari dokumen)
- Field permintaan SQL bernama **`stmt`**, bukan `sql` (beberapa ringkasan pihak ketiga keliru menyebut `sql` - dikoreksi setelah membaca `docs/API.md` mentah).
- `createDocWithMd` **tidak menimpa** dokumen yang sudah ada di `path` yang sama (dikonfirmasi dokumentasi resmi: *"the existing document will not be overwritten"*); skill ini menambahkan pengecekan sendiri lewat `getIDsByHPath` supaya bisa memberi pesan yang jelas ke pengguna sebelum mencoba.
- Membuat dokumen di path bertingkat (mis. `/FAQ/Jam Buka`) **otomatis membuat dokumen induk kosong** (`/FAQ`) bila belum ada - dikonfirmasi lewat uji langsung dengan kernel resmi v3.8.5. Perintah `ekspor-basis` melewati dokumen kosong semacam ini secara otomatis (lihat `_kosong()` di `scripts/siyuan.py`).
- Tabel `blocks` (yang dipakai lewat `/api/query/sql`) punya kolom `id`, `root_id`, `box` (id buku catatan), `hpath` (path manusiawi), `content`, `type` (`d`=dokumen, `h`=heading, `p`=paragraf, dll.), `updated` (string 14 digit `yyyyMMddHHmmss`, bisa dibandingkan sebagai teks karena panjangnya tetap).
- Kernel default menjawab di **HTTP maupun HTTPS sekaligus** pada port yang sama (HTTPS pakai sertifikat CA lokal yang dibuat otomatis). Skill ini memakai `http://127.0.0.1:6806` sesuai contoh resmi di `docs/API.md`; tidak perlu HTTPS untuk alamat localhost.
- **Autentikasi bukan pembatas tunggal:** dalam pengujian Komunitech, permintaan ke endpoint di atas **tanpa header `Authorization` sama sekali** berhasil diproses kernel (termasuk permintaan yang menulis data), berbeda dengan permintaan yang membawa token yang **salah** (ditolak 401). Lihat `research/sources/siyuan-2026-09-26.md` §D6 dan `docs/panduan-siyuan.md` §3.5. Karena itu skill ini **selalu** mengirim token yang benar di setiap permintaan (disiplin sendiri), tapi pembatas keamanan yang sesungguhnya tetap: kernel hanya boleh dijangkau dari komputer itu sendiri.

## Template SQL tetap yang dipakai skill (whitelist, lihat `scripts/siyuan.py`)
Skill **tidak pernah** mengirim SQL bebas dari pengguna ke kernel. Hanya tiga bentuk `SELECT` tetap berikut, dengan bagian yang bisa diisi pengguna (kata kunci pencarian) disisipkan **di dalam literal string** setelah tanda kutip tunggal digandakan (aturan escaping SQLite baku):

```sql
-- cari
SELECT root_id, box, hpath, content, type, updated FROM blocks
WHERE type IN ('d','h','p') AND (content LIKE '%<kata>%' ESCAPE '\' OR hpath LIKE '%<kata>%' ESCAPE '\')
ORDER BY updated DESC LIMIT <maks>

-- lama
SELECT id, box, hpath, updated FROM blocks WHERE type='d' AND updated < '<cutoff 14 digit>' [AND box='<notebook>']
ORDER BY updated ASC LIMIT 200

-- ekspor-basis (daftar dokumen 1 buku catatan)
SELECT id, hpath, updated FROM blocks WHERE type='d' AND box='<notebook>' ORDER BY hpath LIMIT 2000
```

`<cutoff>` dihitung sendiri oleh script dari `--hari` (tanggal-waktu sekarang dikurangi N hari, diformat 14 digit) - bukan masukan bebas pengguna, jadi tidak perlu escaping tambahan (tetap divalidasi berupa 14 digit angka sebagai jaga-jaga).
