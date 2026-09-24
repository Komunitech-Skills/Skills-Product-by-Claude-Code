# 04 — Input tidak lengkap: "ingetin nagih si Budi ya"

**Skenario:** Pemilik warung mengetik permintaan super singkat. Nama ada, tetapi tanggal (wajib) dan
nominal/nota (disarankan untuk piutang) tidak ada. Hari acuan: Kamis, 1 Oktober 2026.

## Input pengguna (persis)
> ingetin nagih si Budi ya

## Output (balasan agent, satu pesan, sesuai SKILL.md "tanyakan sekali, maks. 5 pertanyaan bernomor")
```
Siap, saya catat pengingat tagih Budi. Biar pengingatnya pas, boleh dijawab sekaligus:
1. Kapan jatuh temponya / kapan mau ditagih? (mis. "tgl 10", "Jumat", "besok")
2. Berapa nominalnya? (mis. "2,5 jt")
3. Nomor nota/invoice atau untuk barang apa? (opsional, masuk ke draf pesan)

Kalau mau cepat, balas "hari ini aja" — saya catat jatuh tempo hari ini tanpa nominal, dan draf pesannya
tanpa angka.
```

*(pengguna: "tgl 10, 2,5jt, nota 0415")*

```bash
S="python3 <folder-skill>/scripts/cek_jatuh_tempo.py --hari-ini 2026-10-01"
$S --teks tambah --jenis piutang --nama "Budi" --tanggal "tgl 10" --nominal "2,5jt" --perihal "nota 0415"
```
```
Tersimpan #1: piutang - Budi, Sabtu, 10 Oktober 2026, Rp 2.500.000 (nota 0415).
Catatan: Bulan tidak disebut; dipakai 10 Okt 2026 (tanggal 10 terdekat ke depan). Ubah bila maksudnya lain.
```
Saya akan menampilkannya di rekap tanggal 9 Okt (H-1) dan 10 Okt, lengkap dengan draf pesan siap kirim.

### Jalur "hari ini aja" (default + asumsi disebutkan)
```bash
$S --teks tambah --jenis piutang --nama "Budi"
```
```
Tersimpan #2: piutang - Budi, Kamis, 1 Oktober 2026.
Catatan: Tanggal tidak disebut; dipakai hari ini.
Catatan: Nominal piutang belum diisi; draf pesan akan tanpa angka.
```

### Temuan saat uji: `draf --id` untuk item yang masih jauh
Pengguna langsung minta "coba liat drafnya" pada 1 Okt (item jatuh tempo 10 Okt):
```bash
$S --teks draf --id 1
```
```
#1 untuk Budi:
Selamat pagi Budi, izin mengingatkan pembayaran nota 0415 sebesar Rp 2.500.000 yang jatuh tempo besok, 10 Okt 2026. Pembayaran bisa melalui [rekening]. Abaikan pesan ini jika sudah membayar. Terima kasih.
```
**Salah:** 10 Okt adalah 9 hari lagi, bukan "besok". Jika pemilik menyalin dan mengirim hari ini, pelanggan
menerima informasi keliru. Agent seharusnya mengoreksi (atau script membuat varian "jatuh tempo pada {tanggal}"
untuk selisih > 1 hari).

## Catatan penguji
- Bagus: SKILL.md cukup jelas untuk bertanya **sekali** dengan daftar bernomor; script memberi `Catatan:`
  asumsi (hari ini, tanpa nominal) sehingga jalur cepat tetap jujur. Sapaan "si Budi" disimpan sebagai "Budi".
- Kurang: tabel Input menandai "Kapan" sebagai **Wajib** tetapi juga punya default "Hari ini". Agent lain bisa
  langsung menyimpan tanpa bertanya. Sebaiknya tegaskan: untuk piutang tanpa tanggal, tanyakan dulu; default
  hanya bila pengguna minta cepat.
- Cacat SEDANG: `draf --id` untuk item > 1 hari ke depan menulis "besok".

---
## Uji ulang v1.0.1 (2026-09-24)
`draf --id 1` (Budi, jatuh tempo 10 Okt) pada 1 Okt kini: "... sebesar Rp 2.500.000 yang jatuh tempo **pada 10 Okt 2026**."
Cacat "besok" sudah diperbaiki. SKILL.md tabel Input kini menegaskan: piutang tanpa tanggal → tanya dulu.
