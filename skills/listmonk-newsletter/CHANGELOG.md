# Riwayat perubahan — listmonk-newsletter

Catatan teknis per versi.

## Catatan revisi 1.0.6 (2026-10-02)
- Ditambah larangan di SKILL.md: bila pengguna menempel kunci/token/sandi di chat, agent tidak boleh menulis ulang satu karakter pun darinya; cukup menyebut "kunci yang Anda tempel".

## Catatan revisi 1.0.5 (2026-10-02)
- Revisi dari uji OpenClaw: `impor` kini wajib menampilkan pratinjau lebih dulu (jumlah valid, duplikat, tidak valid, tidak setuju, serta contoh kontak dengan email disamarkan) dan baru jalan setelah pengguna setuju.
- Kontak dengan domain salah ketik (mis. gmial.com, yaho.com) ditahan, tidak diimpor otomatis; opsi `--sertakan-typo` hanya bila pengguna memastikan alamat itu benar. Agent tidak boleh memperbaiki alamat sendiri tanpa persetujuan.
- Draf kampanye yang gagal pemeriksaan harus diperbaiki, bukan diganti dengan kampanye baru. Uji regresi menjadi 73 skenario.

## Catatan revisi 1.0.4 (2026-10-01)
- SKILL.md kini menyebut bahwa script ada di subfolder `scripts/` di folder skill, dan agent tidak boleh mencari file ke seluruh disk (mis. `find /`). Logika tidak berubah.

## Catatan revisi 1.0.3 (2026-09-30)
- Ditambah baris "Aturan kerja" di SKILL.md: tidak memasang paket/aplikasi sendiri, tidak membuka file di luar yang diberikan pengguna dan isi folder skill, dan menyebut lokasi file baru. Logika tidak berubah.

## Catatan revisi 1.0.2 (2026-09-29)
- Penyaring sumber kontak diperluas: daftar hasil pembelian, sewa, jual-beli data, perantara/agensi, pihak ketiga, dan "dapat dari teman" ditolak.
- Tag `{{ UnsubscribeURL }}` baru dihitung bila ada di atribut `href` tautan yang terlihat (tidak dihitung di komentar, skrip, gaya, atau tautan tersembunyi).
- Gerbang kirim dikuatkan dengan tanda tangan (HMAC) memakai kunci lokal, dan SKILL.md memuat bagian "Keterbatasan pengaman" yang jujur: pengaman ini melindungi dari kelalaian agent, bukan dari orang atau agent yang punya akses shell ke komputer yang sama. 65 skenario uji.

## Catatan revisi 1.0.1 (2026-09-29)
- Revisi dari uji pertama (gerbang kirim diperketat): sebelum `kirim` atau `jadwal`, pengguna harus menjawab "ya" dan script menolak bila jumlah penerima yang dikonfirmasi tidak sama dengan angka sebenarnya.
- Impor wajib `--sumber-persetujuan` dan `--saya-punya-izin`; sumber seperti grup WhatsApp, vendor, hasil beli, atau scraping ditolak. Kolom persetujuan yang kosong dianggap tidak setuju; awalan `=+-@` pada nama dibersihkan.
- Alamat uji kirim hanya yang didaftarkan sendiri oleh pemilik lewat `simpan-alamat-uji` di terminal (maksimal 3); tautan berhenti harus berada di luar komentar HTML. Catatan UU PDP Pasal 20 ditambahkan. 53 skenario uji.

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): mengelola newsletter email untuk UMKM lewat listmonk milik sendiri (pengganti Mailchimp): periksa dan impor kontak dengan pengingat persetujuan UU PDP, daftar double opt-in dengan tautan berhenti, draf kampanye berbahasa Indonesia, uji kirim, jadwal, dan laporan buka/klik. Diuji dengan listmonk 6.2.0 asli (Docker).
