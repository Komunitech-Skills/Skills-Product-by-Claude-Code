# 00 - Uji A/B skenario 1 (impor CSV berpersetujuan), tanpa skill vs dengan skill
Tanpa skill (agen langsung memakai API listmonk 6.2.0 dengan file yang sama, header diubah ke email,name,attributes, `subscription_status=confirmed`, `overwrite=true`):
- Impor "finished 9 dari 10". Masuk berstatus **confirmed**: Eko (`setuju=tidak`), Fajar (kosong), `citra@gmial.com`, nama `=cmd|'/c calc'!A1`; duplikat Budi tertimpa; tak ada catatan asal persetujuan; tak ada ringkasan bagi pemilik, tak ada peringatan UU PDP, tak ada double opt-in.
Dengan skill: valid 7 / buang 3 (tidak valid, duplikat, menolak), typo ditandai, status `unconfirmed` + email konfirmasi, atribut `sumber_persetujuan` & tanggal, ringkasan angka, gerbang `--ya`.
Putusan: skill jelas lebih baik (nilai tambah utama: keamanan persetujuan dan ketelitian angka). Kelemahan skill yang tetap ada dicatat di HASIL-UJI (kolom setuju kosong).
