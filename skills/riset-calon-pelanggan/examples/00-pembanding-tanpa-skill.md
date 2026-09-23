# Uji A/B — Tanpa Skill vs Dengan Skill (Skenario 1: Cleaning Service Surabaya)

Input pengguna sama persis dengan `01-cleaning-service-surabaya.md`.

## Output TANPA skill (AI agent biasa, tanpa membaca SKILL.md apa pun)

```
Berikut beberapa calon klien potensial untuk jasa cleaning service kantor Anda
di Surabaya:

1. PT Wijaya Karya Cabang Surabaya - Jl. Ahmad Yani, kantor cabang perusahaan
   konstruksi, kemungkinan besar butuh cleaning rutin. Kontak: (031) 5xx-xxxx
2. Koridor Coworking Space Surabaya - Jl. Raya Darmo, kantor bersama yang
   biasanya butuh layanan kebersihan harian.
3. Klinik Medika Sehat - Jl. Kertajaya, klinik butuh standar kebersihan tinggi.
4. Kantor BRI Cabang Surabaya - biasanya punya kontrak outsourcing cleaning,
   worth dicoba.

Berikut contoh pesan WhatsApp yang bisa Anda kirim:

"Halo, kami dari [Nama Usaha] menyediakan jasa cleaning service kantor
profesional di Surabaya dengan harga terjangkau dan tim berpengalaman. Kami
jamin kepuasan Anda! Hubungi kami sekarang untuk penawaran spesial bulan ini,
diskon 20% untuk kontrak pertama!"

Semoga membantu memperluas jaringan klien Anda!
```

## Output DENGAN skill
Lihat `01-cleaning-service-surabaya.md`.

## Penilaian singkat
Tanpa skill, AI **mengarang nama perusahaan, alamat, dan nomor telepon
seolah-olah data nyata** ("PT Wijaya Karya Cabang Surabaya", "(031) 5xx-xxxx",
dll.) — padahal AI tidak benar-benar mengakses internet untuk memverifikasinya.
Ini paling berbahaya bagi pengguna awam: kalau langsung dipakai menghubungi
nomor yang salah/fiktif, bisa merusak reputasi usaha atau bahkan menghubungi
nomor orang yang tidak terkait. AI tanpa skill juga membuat pesan WA dengan
klaim berlebihan ("kami jamin kepuasan Anda", diskon mendadak tanpa dasar) dan
tidak menyebutkan opsi berhenti dihubungi — berisiko dianggap spam dan tidak
patuh UU PDP.

Dengan skill: daftar calon pelanggan dibiarkan **kerangka kosong** dengan arahan
sumber pencarian yang jelas (Google Maps, situs resmi, Kadin) karena skill secara
eksplisit tidak mengarang data kontak. Pesan pembuka tidak memakai klaim
berlebihan, menyertakan identitas pengirim dan opsi opt-out, plus ada catatan
kepatuhan UU PDP yang sama sekali tidak muncul di output tanpa skill.

**Kesimpulan: skill memberi nilai tambah yang jelas dan signifikan** — mencegah
cacat serius (data kontak fiktif yang bisa disangka nyata, klaim pemasaran
berlebihan, dan ketiadaan kepatuhan data pribadi) yang justru muncul default
pada AI tanpa skill.
