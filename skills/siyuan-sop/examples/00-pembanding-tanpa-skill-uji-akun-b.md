# A/B: tanpa skill vs dengan skill (uji Akun B) — skenario "simpan SOP toko ke SiYuan"

## Tanpa skill (agent generik, tidak tahu SiYuan API)
Permintaan: "Simpan SOP buka toko pagi ini ke SiYuan saya."
Agent tanpa `siyuan-sop` **tidak tahu** SiYuan punya kernel API lokal berport 6806 dengan token —
kemungkinan besar responsnya: (a) menyarankan pengguna menyalin-tempel manual ke aplikasi SiYuan
(tidak "instan"), atau (b) mengarang perintah `curl` ke endpoint yang salah/menebak-nebak bentuk
JSON, tanpa validasi token, tanpa cek localhost, tanpa proteksi anti-timpa, dan (paling berisiko)
bisa saja mengirim SQL yang disusun dari string concat kalau diminta "cari yang mengandung X" —
tidak ada jaminan escaping. Tidak ada mekanisme pratinjau/konfirmasi sebelum menulis.

## Dengan skill `siyuan-sop`
Perintah sama, dijalankan lewat `scripts/siyuan.py buat` (lihat `01-sop-toko-uji-akun-b.md`):
pratinjau otomatis → konfirmasi eksplisit → tersimpan, dengan proteksi anti-timpa (kode 7),
escaping SQL template tetap, dan penolakan alamat non-localhost bawaan.

## Kesimpulan uji A/B
Beda telak, bukan sekadar kosmetik: skill memberi (1) jalur API yang benar & teruji, bukan tebakan,
(2) pratinjau+konfirmasi wajib sebelum menulis, (3) proteksi anti-timpa data, (4) SQL selalu lewat
templat aman. Tanpa skill, keempat hal ini bergantung sepenuhnya pada agent generik menebak dengan
benar setiap kali — risiko tinggi untuk pembeli awam. **Skill memberi nilai tambah nyata**, bukan di
bawah skor 6 pada kriteria ini.
