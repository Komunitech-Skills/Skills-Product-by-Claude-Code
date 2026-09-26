# Skenario 01 (uji Akun B, independen) — SOP toko kelontong: buat + cari (normal)

**Penguji:** Akun B (independen dari pembuat), 2026-09-26. **Kernel:** server tiruan buatan sendiri
(`mock_kernel.py`, http.server standar, tidak menyalin `tests/test_siyuan.py` pembuat) di
`127.0.0.1:16806` — lihat catatan di `00-catatan-metodologi-uji-akun-b.md` untuk alasan tidak
memakai kernel SiYuan asli.

## Permintaan pengguna
> "Simpan SOP buka toko pagi ke SiYuan, buku catatan SOP Toko Kelontong."

## Perintah & hasil nyata
```
$ python3 scripts/siyuan.py --url http://127.0.0.1:16806 --kunci-file kunci-b.txt buat \
    --notebook 20260101000000-tokobox1 --path "/SOP/Buka Toko Pagi" --md "1. Buka gerbang..."
PRATINJAU BUAT DOKUMEN
...
Simpan ke SiYuan? Jalankan ulang dengan --ya.
```
Diulang dengan `--ya`:
```
TERSIMPAN: dokumen '/SOP/Buka Toko Pagi' dibuat di SiYuan (id 2026092609000200-mock002).
```
```
$ python3 scripts/siyuan.py ... cari "kasir"
HASIL PENCARIAN 'kasir' (1 dokumen)
- Buka Toko Pagi  [/SOP/Buka Toko Pagi]
    ......isi ulang bila < 5 botol per rasa. 3. Nyalakan mesin kasir...
```

## Verifikasi independen
- Alur pratinjau → konfirmasi eksplisit ("ya") → `--ya` bekerja persis seperti didokumentasikan di SKILL.md §D.
- Dokumen langsung ditemukan `cari` pada percobaan pertama (tidak ada jeda pada server tiruan ini — jeda indeks di SKILL.md khusus perilaku kernel asli, wajar tidak muncul di tiruan).
- Kode keluar 0, output teks dan `--json` konsisten satu sama lain (dicek terpisah).

## Kesimpulan
Sesuai dokumentasi. Tidak ada temuan baru pada skenario ini.
