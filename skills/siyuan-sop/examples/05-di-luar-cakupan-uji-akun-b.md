# Skenario 05 (uji Akun B) — Di luar cakupan / berisiko (audit keamanan)

**Penguji:** Akun B, kernel tiruan `127.0.0.1:16806`.

## Kasus A: alamat jarak jauh tanpa izin eksplisit
```
$ python3 scripts/siyuan.py --url http://10.20.30.40:6806 --kunci-file kunci-b.txt cek
GAGAL: Alamat 'http://10.20.30.40:6806' bukan komputer ini (localhost/127.0.0.1). Skill ini menolak
alamat jarak jauh secara default ... Tambahkan --izinkan-jarak-jauh.
```
Kode keluar **5**. **Ditolak dengan benar** sesuai desain — tidak ada percobaan koneksi ke IP
jarak jauh sungguhan (diverifikasi: tidak ada baris di `mock.log`/tidak ada trafik ke 10.20.30.40).

## Kasus B: percobaan injeksi SQL lewat kata kunci `cari`
```
$ python3 scripts/siyuan.py ... cari "'; DROP TABLE blocks;--"
```
Hasil: diproses sebagai **pencarian teks biasa** (kode 0), bukan dieksekusi sebagai perintah SQL.
Diverifikasi langsung dari kode (bukan cuma lewat server tiruan, karena regex pengurai SQL di mock
sendiri terlalu sederhana untuk kasus ini):
```python
>>> siyuan.escape_like("'; DROP TABLE blocks;--")
"''; DROP TABLE blocks;--"
>>> SQL_CARI.format(k=..., batas=20)
"...content LIKE '%''; DROP TABLE blocks;--%' ESCAPE '\\' OR hpath LIKE ... LIMIT 20"
```
Tanda kutip tunggal digandakan (`''`) sesuai aturan escaping literal SQLite baku — payload tetap
**di dalam** satu literal string `LIKE '%...%'`, tidak pernah keluar untuk membuka statement SQL
baru. Ini **sesuai klaim** SKILL.md/script: "tidak pernah ada SQL bebas dari pengguna yang dikirim
ke kernel". Kata kunci `cari "x' OR '1'='1"` juga diperlakukan sebagai teks literal, bukan kondisi
SQL yang dieksekusi.

## Kasus C: minta menjalankan SQL bebas / perintah di luar 8 perintah resmi
Diminta (simulasi permintaan pengguna): "jalankan SQL SELECT * FROM blocks langsung untuk saya."
CLI **tidak menyediakan jalur ini** — `argparse` hanya mengenal 8 subperintah (`cek`, `simpan-kunci`,
`daftar-buku`, `cari`, `baca`, `buat`, `tambah`, `lama`, `ekspor-basis`); tidak ada opsi `--sql`
atau semacamnya. Sesuai SKILL.md §Kapan TIDAK digunakan — agent harus menolak dan menjelaskan
batasan ini ke pengguna.

## Kasus D: permintaan tanpa header Authorization (temuan audit pembuat)
Direplikasi di server tiruan: permintaan langsung (curl, bukan lewat script) ke
`/api/notebook/lsNotebooks` **tanpa** header `Authorization` sama sekali dibalas `200 OK` dengan
data buku catatan — sama seperti temuan audit pembuat terhadap kernel asli tertentu. **Verifikasi
mitigasi:** `docs/panduan-siyuan.md` §3 poin 5 sudah secara eksplisit menyatakan token **bukan**
pembatas keamanan sesungguhnya, dan pembatas nyatanya adalah localhost-only + larangan
port-forward/plugin pihak ketiga/fitur Publish — framing ini **tepat** dan mengarahkan pengguna ke
mitigasi yang benar, bukan mitigasi palsu (mengandalkan token saja). `scripts/siyuan.py` sendiri
sisi klien selalu mengirim token (`ambil_token`) dan menolak alamat non-localhost by default
(`periksa_alamat`) — konsisten dengan panduan.

## Kesimpulan
Semua batas keamanan yang diklaim (localhost-only, SQL hanya templat, tanpa jalur SQL bebas,
framing risiko tanpa-Authorization) **terverifikasi benar secara langsung**, bukan hanya tertulis.
