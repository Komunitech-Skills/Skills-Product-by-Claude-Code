# Uji 04 — Input tidak lengkap, tanggal ambigu, data rusak

- **Penguji:** agent independen Akun B. Acuan 26 Sep 2026 (WIB). Data rekaan.

## A. Permintaan tidak lengkap
**Pengguna (DB TB Kokoh Jaya dari uji 03):** "Catat bon Pak Joko yang kemarin ya."

Script:
```
catat --pelanggan "Pak Joko" --tanggal kemarin
GAGAL: Nominal tagihan belum disebut (--nominal, mis. 2,5jt).
catat --pelanggan "Pak Joko" --tanggal kemarin --nominal "1,2 jt"
GAGAL: Pelanggan 'Pak Joko' tidak ada yang persis sama, tapi ada yang mirip: P0001 Pak Joko Mandor. Tanyakan ke pengguna ...
```
Balasan agent yang sesuai SKILL.md (sekali, bernomor):
> Siap, sebelum saya catat:
> 1. Berapa nominal bonnya?
> 2. Pak Joko yang dimaksud **Pak Joko Mandor (P0001)**, atau orang lain?
> 3. Nomor notanya ada? (kalau tidak, saya beri nomor otomatis PB-xxxx)
> 4. Temponya berapa hari? (kalau tidak disebut, saya pakai 30 hari)

Jawaban "1,2 juta, iya Joko Mandor, nota nggak ada" → `catat --pelanggan P0001 --tanggal kemarin --nominal "1,2 jt"`:
```
Tercatat nota PB-0001 untuk Pak Joko Mandor (P0001): Rp 1.200.000 | tanggal 25 Sep 2026 | jatuh tempo Minggu, 25 Oktober 2026 (30 hari)
Catatan: Jatuh tempo belum disebut; dipakai termin 30 hari dari tanggal nota.
Catatan: Nomor nota tidak disebut; diberi nomor otomatis PB-0001.
```
Asumsi disebut oleh script ✅. Catatan: script memeriksa nominal sebelum kemiripan nama, jadi agent yang hanya mengandalkan pesan error akan bertanya dua kali. SKILL.md (tabel Input + "tanyakan sekali") cukup untuk mencegahnya bila agent mengecek `saldo --pelanggan` dulu (P3).

Database belum ada: `saldo` → `GAGAL: Database piutang belum ada di ... Jalankan dulu: piutang.py init` ✅ (agent lalu menanyakan nama usaha/pengirim/rekening/termin sekali).

## B. Tanggal ambigu & ngawur (`catat --tanggal ...`)
| Input | Hasil |
|---|---|
| `03/04/2026`, `03-04-2026`, `3.4.2026` | 3 Apr 2026 (hari/bulan Indonesia, tanpa catatan) |
| `3 Apr 26`, `3/4/26` | 3 Apr 2026 + "Tahun ... ditulis 2 angka; dibaca 2026" |
| `3 Apr` | 3 Apr 2026 + "(tahun tidak disebut)" (176 hari ke belakang) |
| `20 Mar` | TOLAK: tanpa tahun tidak jelas (190 hari) |
| `26/9`, `kemarin`, `3 hari lalu`, `2026-09-01`, `3 April 2026`, kosong | benar; kosong → hari ini + catatan |
| `10/25/2026` | TOLAK + "Sepertinya ditulis bulan/hari ... maksudnya 25/10/2026?" |
| `31/09/2026`, `29/02/2026` | TOLAK: tidak ada di kalender |
| `46291` | TOLAK: angka seri Excel + cara memperbaiki |
| `27/09/2026` (besok) | TOLAK: masa depan |
| `1/1/1999` | TOLAK: tahun tidak wajar |
| `April 3, 2026`, `Agustus 2026` | TOLAK: tidak dikenali + contoh format |
| `--jatuh-tempo 30` | TOLAK: tanggal atau jumlah hari? |
| JT sebelum tanggal nota | TOLAK |

## C. Nominal rusak
`4,5`, `12.50`, `1.500 jt`, `5m` → TOLAK ambigu dengan contoh; `0` → harus > 0; `--nominal=-100rb` → tidak boleh negatif (arahkan ke `potong`); `1 triliun`, `abc` → TOLAK. `1,3jt`, `Rp 1.250.000,-`, `2 jt 500 rb` → benar. `--nominal -100rb` (tanpa `=`) gagal di argparse: kode keluar 2 **tanpa JSON** walau `--json` (P3, sudah didokumentasikan sebagai "2 = perintah salah tulis").

## D. CSV rusak (`impor kotor.csv`, Windows-1252, CRLF, judul kolom Inggris)
```
Kolom dikenali: pelanggan='Nama Pelanggan', nota='No Invoice', tanggal='Tgl', jatuh_tempo='Due Date', nominal='Total', dibayar='Paid', status='Status'
Akan dicatat: 3 nota ... BARIS BERMASALAH, TIDAK DIIMPOR (6):
- baris 3: nama pelanggan '=HYPERLINK("x")' berisi rumus Excel
- baris 4: Tanggal '31/09/2026' tidak ada di kalender.
- baris 5: Nominal 'abc' tidak dikenali.
- baris 6: dibayar Rp 400.000 melebihi nominal Rp 300.000
- baris 8: jatuh tempo 1 Sep 2026 sebelum tanggal nota 7 Sep 2026
- baris 11: nomor nota INV-1 sudah muncul di baris 2 ... --gabung-baris
Catatan: File bukan UTF-8; dibaca sebagai Windows-1252 (ANSI). ...
Catatan: Lebih dari separuh baris bermasalah; periksa dulu ...
```
Baris kosong dilewati, `Café` terbaca benar, `lunas` dilewati. Format Amerika (`09/25/2026`) → seluruh impor ditolak dengan penjelasan ✅. File tanpa kolom wajib, file biner, file tidak ada → pesan jelas ✅.
**Temuan (P3):** status `??` (hanya tanda baca) **diimpor sebagai piutang**, padahal `references/perintah.md` menyebut status lain → baris bermasalah (`done`, `-`, `dibayar` memang ditolak). `sebagian`/`Belum Lunas` diimpor, `Settled`/`sudah bayar`/`LUNAS ` dilewati ✅.

## E. Database rusak — backup/restore
| Kerusakan (disengaja) | Perilaku | Nilai |
|---|---|---|
| Header 16 byte ditimpa + 1 halaman | Semua perintah: "rusak atau bukan database ... Jangan hapus ... backup --daftar ... restore" → `restore` pratinjau ("Database saat ini RUSAK; dipindah") → `--ya` → pulih; `saldo --semua` identik dengan sebelum rusak (diff kosong); file rusak di `backup-piutang/rusak-piutang-<waktu>.db` | ✅ |
| File dipotong 20 KB | ditolak + petunjuk restore | ✅ |
| Header b-tree satu halaman data (hal. 2, 4, 5, 7, 10) | "Database rusak (malformed)" → restore berhasil | ✅ |
| Restore dari file cadangan rusak / CSV / file tidak ada | ditolak, DB tidak disentuh | ✅ |
| **Halaman 3 (indeks otomatis tabel `meta`)** | Semua perintah: "**bukan database buku-piutang. File itu tidak diubah; periksa --db.**" `restore --dari <cadangan sah> --ya` → "restore dibatalkan agar file itu tidak tertimpa"; `init --mulai-baru` → "sudah ada dan bukan database buku-piutang; tidak ditimpa". | ❌ **P2** |

Pada kasus terakhir pengguna terkunci: pesan mengarah ke "periksa --db" (salah arah), restore & mulai-baru sama-sama menolak, padahal SKILL.md Langkah G menjanjikan restore "bisa walau database rusak total". Jalan keluar hanya memindahkan file secara manual — yang dilarang SKILL.md ("jangan hapus atau timpa file database sendiri"). Saran: bedakan "tabel meta tidak terbaca/SQLite malformed" dari "database aplikasi lain" (mis. cek `sqlite_master` berisi tabel `meta` + `nota` + `pelanggan`), dan izinkan `restore` memindahkan file seperti kasus rusak lain.

**Nilai skenario: lulus dengan 1 temuan P2** (penanganan input buruk sangat baik; satu jalur pemulihan buntu).
