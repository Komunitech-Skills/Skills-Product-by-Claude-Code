# Uji ulang v1.0.2 — Penguji independen (Akun B), 2026-09-25

Uji ringan sesuai instruksi: perubahan v1.0.2 hanya dokumentasi + 1 baris versi
script + 1 tes regresi baru (lihat `git show a536052`). Tidak ada perubahan logika
pemanggilan API Stirling-PDF, jadi tidak dijalankan ulang skenario 01-05 penuh.

## 1. Periksa setiap kalimat yang berubah

**Klaim "sudah diuji Stirling-PDF v3.0.0" (SKILL.md §Batasan, README §Status pengujian)**
— DIDUKUNG bukti nyata, bukan klaim baru tanpa dasar:
- `examples/HASIL-UJI.md` baris 108-183 ("Uji ulang v1.0.1", 2026-09-24): penguji
  independen ke-2 menjalankan Docker `ghcr.io/stirling-tools/stirling-pdf:3.0.0` DAN
  `:2.14.3` sungguhan, memverifikasi hasil dengan `pdfinfo`/`pdftotext`/`qpdf`/
  `sha256sum` (baris 122-125, 163).
- `references/sumber-api-stirling.md` baris 41-70 mencatat temuan verifikasi kedua
  versi tersebut secara rinci (digest image, endpoint identik).
→ Perubahan teks v1.0.2 hanya **menyamakan** SKILL.md/README dengan fakta yang sudah
  tercatat di HASIL-UJI.md, bukan mengarang klaim kompatibilitas baru. Tidak ada
  temuan.

**Klaim privasi README ("Privasi terjaga")** — sebelumnya generik ("tidak pernah
diunggah ke situs PDF online pihak ketiga"), sekarang dipersempit ke yang benar-benar
mutlak ("script ini hanya bicara ke `localhost`") + menonjolkan pengecualian R3
(dokumen sensitif tidak pernah diarahkan ke upload online). Ini KONSISTEN dengan:
- `SKILL.md` "Cara manual tanpa script" poin 4-5 (dokumen biasa boleh diarahkan ke
  situs resmi Stirling-PDF sebagai jalan terakhir dengan peringatan; dokumen sensitif
  JANGAN PERNAH).
- `docs/panduan-stirling-pdf.md` baris 5 ("file PDF tidak diunggah ke internet") —
  ini soal instalasi Docker lokal itu sendiri, tidak bertentangan dengan pengecualian
  R3 di atas karena konteksnya beda (instalasi vs. jalan pintas manual).
Tidak ditemukan klaim berlebihan ("100% aman", "tidak pernah keluar dari komputer"
tanpa syarat) — judul README "Tanpa Upload" tetap akurat untuk perilaku script,
dan bullet Manfaat sudah menjelaskan nuansa jalan pintas manual. Tidak ada temuan.

## 2. Nomor versi konsisten

| Sumber | Nilai |
|---|---|
| `scripts/pdf.py` (`VERSI = `) | 1.0.2 |
| `catalog.csv` baris `pdf-lokal` | 1.0.2 |
| README riwayat versi | (tidak ada bagian ini di README — tidak berlaku) |

Konsisten. Tes baru `versi-konsisten-di-bantuan` di `tests/uji_regresi.py` mengunci
ini otomatis ke depan (memverifikasi `--help` mencetak versi yang sama dengan
konstanta `VERSI`).

## 3. Jalankan tes

```
$ python3 skills/pdf-lokal/tests/uji_regresi.py
...
16/16 skenario lulus.
$ echo $?
0
```

```
$ python3 scripts/validate.py --skill pdf-lokal
✅ 1 skill valid, 68 baris katalog sesuai.
```

Kedua perintah lulus tanpa error, dijalankan dari root repo `/home/user/Skills`.

## Kesimpulan

Perubahan v1.0.2 adalah housekeeping dokumentasi yang jujur dan berdasar bukti nyata
di `HASIL-UJI.md`/`references/`, bukan klaim baru tanpa dukungan. Tidak ditemukan
inkonsistensi versi maupun klaim privasi yang berlebihan. Tidak ada regresi
fungsional (16/16 tes, validate.py lulus). Lihat skor & rincian di bagian
"Uji ulang v1.0.2 (Akun B)" pada `HASIL-UJI.md`.
