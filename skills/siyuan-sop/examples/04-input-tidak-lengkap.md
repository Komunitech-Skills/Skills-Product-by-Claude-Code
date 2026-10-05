# Skenario 04 — Input tidak lengkap

**Penguji:** pembuat skill (BUKAN penguji independen), 2026-09-26. Kernel SiYuan resmi v3.8.5 untuk
bagian yang menyentuh API; sisanya perilaku yang diharuskan `SKILL.md` (belum tentu semua sudah
diuji dengan model AI sungguhan, hanya perilaku script yang diverifikasi).

## Kasus A - tidak menyebut mau disimpan di mana
> Pengguna: "Simpan SOP tutup toko ini ke SiYuan ya."

Agent **belum tahu** buku catatan/notebook mana dan path apa. Sesuai `SKILL.md` §Persiapan,
agent menjalankan `daftar-buku` dulu:
```
$ python3 scripts/siyuan.py daftar-buku
Belum ada buku catatan di SiYuan.
```
(Pada workspace baru yang belum dibuatkan buku catatan apa pun.) Agent bertanya **sekali**, dalam
satu pesan:
> "SiYuan Anda belum punya buku catatan sama sekali. Boleh saya buatkan satu (mis. "SOP & FAQ Toko") dulu lewat aplikasi SiYuan Anda (skill ini tidak membuat buku catatan baru), atau sudah ada yang mau dipakai? Judul dokumennya saya beri `/SOP/Tutup Toko` - boleh diganti kalau ada nama folder lain yang biasa dipakai."

Bila ternyata sudah ada buku catatan tapi pengguna hanya lupa menyebut, agent memakai hasil
`daftar-buku` untuk menebak yang paling relevan (jika hanya ada satu) atau bertanya bila lebih dari
satu.

## Kasus B - argumen script tidak lengkap (dicoba langsung, kode keluar 2)
```
$ python3 scripts/siyuan.py buat --path "/FAQ/Tes" --md "isi"
usage: siyuan.py buat [-h] --notebook NOTEBOOK --path PATH [--md MD]
                      [--md-file MD_FILE] [--stdin] [--ya] [--timpa]
siyuan.py buat: error: the following arguments are required: --notebook
```
Agent tidak menampilkan pesan teknis argparse ke pengguna awam; cukup: "Boleh tahu ini mau disimpan di buku catatan yang mana?" (lalu tawarkan hasil `daftar-buku`).

## Kasus C - isi Markdown kosong
> Pengguna: "Buatkan dokumen SOP packing di SiYuan." (tanpa isi apa pun)

Agent **tidak mengarang isi SOP** dari nol tanpa diminta - tawarkan dua pilihan: (1) pengguna
menjelaskan langkah-langkahnya untuk disusun, atau (2) arahkan ke skill `sop-writer` dulu untuk
menyusun SOP-nya, baru disimpan ke sini. Kalau tetap dipaksa memanggil script tanpa isi:
```
$ python3 scripts/siyuan.py buat --notebook 20260926095006-e9vdel5 --path "/SOP/Packing"
GAGAL: Isi Markdown belum diisi. Pakai --md "teks", --md-file file.md, atau --md -.
(kode keluar 2)
```

## Kasus D - angka hari tidak valid untuk `lama`
```
$ python3 scripts/siyuan.py lama --hari 0
GAGAL: --hari harus lebih dari 0.
(kode keluar 2)
```
Agent menanyakan ulang berapa hari yang dimaksud (default yang disarankan: 90 hari).
