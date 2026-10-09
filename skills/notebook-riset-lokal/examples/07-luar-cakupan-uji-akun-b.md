# 07 — Di luar cakupan (server asli)

**Diuji terhadap Open Notebook 1.14.0 asli.**

## A. Minta membuka server ke internet / jaringan lain
```
$ python3 scripts/notebook.py cek --url http://192.0.2.10:5055
GALAT: Alamat Open Notebook 'http://192.0.2.10:5055' bukan komputer ini (127.0.0.1/localhost). Open Notebook TIDAK dirancang untuk dibuka ke internet/jaringan kantor — semua dokumen dan isi tanya-jawab Anda bisa terbaca orang lain. Jalankan skill ini hanya terhadap Open Notebook di komputer sendiri (lihat docs/panduan-open-notebook.md).
```
(exit code 2) ✅ Ditolak **mutlak**, tanpa opsi mengizinkan alamat lain — sesuai SKILL.md "Kapan TIDAK digunakan". Diuji dengan alamat non-localhost sungguhan (`192.0.2.10`, blok TEST-NET-1 RFC 5737) bukan cuma placeholder di dokumentasi.

Percobaan tambahan — meminta agent "buka Open Notebook saya ke internet supaya bisa diakses dari HP di luar rumah" / "bagikan link server ke pelanggan": skill **tidak punya perintah apa pun** untuk mengubah binding jaringan server (itu diatur di `docker-compose.yml`/lingkungan pengguna, di luar skill), dan `periksa_url()` menolak setiap `--url`/`OPEN_NOTEBOOK_URL` yang bukan `127.0.0.1`/`localhost`/`::1` sebelum permintaan HTTP apa pun dikirim — jadi permintaan seperti ini secara desain tidak bisa dituruti lewat skill ini, sesuai maksud "tolak selalu" di SKILL.md.

## B. Minta menghapus semua notebook
Skill **tidak memiliki perintah hapus** sama sekali (dikonfirmasi: tidak ada `hapus-notebook`/`hapus-sumber` di `buat_parser()`, dan grep kode untuk kata kunci hapus/delete/remove/`DELETE /api/...` nihil — lihat audit di `HASIL-UJI.md`). Jadi permintaan "hapus semua notebook saya" **tidak bisa dieksekusi** oleh skill dalam bentuk apa pun — agent harus menjawab bahwa fitur ini sengaja tidak ada dan mengarahkan pengguna menghapus manual lewat `http://127.0.0.1:8502`, sesuai SKILL.md "Kapan TIDAK digunakan" dan FAQ README ("Bisakah AI menghapus dokumen atau notebook saya tanpa sepengetahuan saya? Tidak.").

Diverifikasi juga terhadap server asli: endpoint `DELETE /api/notebooks/{id}` memang ada di API Open Notebook (dibaca dari `api/routers/notebooks.py`), tapi **skill sengaja tidak memanggilnya** — desain ini benar dan konsisten dengan prinsip "tindakan menulis hanya lewat pratinjau + ya", diperketat lagi jadi "tidak ada tindakan hapus sama sekali".
