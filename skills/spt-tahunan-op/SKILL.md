---
name: spt-tahunan-op
description: Menghitung SPT Tahunan PPh Orang Pribadi Indonesia (formulir tunggal Coretax, pengganti 1770/1770S) untuk karyawan satu/lebih pemberi kerja, karyawan plus usaha/pekerjaan bebas (NPPN atau pembukuan), dan freelancer — penghasilan neto, zakat, PTKP, PKP, PPh terutang tarif Pasal 17 UU HPP, kredit pajak (bukti potong A1/A2, PPh 21 bukan pegawai, PPh 22/23, angsuran PPh 25), kurang/lebih bayar, batas lapor, checklist dokumen; dihitung script. Gunakan saat ditanya "SPT tahunan saya kurang bayar?", "lapor pajak tahunan", "punya 2 A1", "pajak freelancer NPPN". Annual individual income tax return Indonesia, tax refund, underpayment. Tidak mengisi/mengirim SPT ke DJP.
---

# SPT Tahunan PPh Orang Pribadi

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu orang biasa tahu **sebelum membuka Coretax**: berapa PPh terutang setahun, berapa yang sudah dipotong, apakah hasilnya **kurang bayar / lebih bayar / nihil**, dokumen apa yang harus disiapkan, dan angka mana masuk bagian mana di SPT. Semua angka **dihitung script** `scripts/spt_op.py`, bukan dikira.

## Kapan digunakan
- "Saya karyawan, SPT tahunan saya nanti kurang bayar nggak?" · "Tahun lalu pindah kerja, punya 2 bukti potong A1."
- "Saya freelancer desain, penghasilan setahun 240 juta, pajaknya berapa?" (NPPN)
- "Karyawan tapi juga buka praktik/usaha sampingan." · "Zakat bisa mengurangi pajak?"
- "Suami-istri penghasilannya digabung (K/I)."

## Kapan TIDAK digunakan
- PPh 21 bulanan karyawan (pemotong) → skill `pph21-ter`. Setoran PPh final 0,5% bulanan → `pph-final-umkm`. Jadwal tenggat → `kalender-pajak`.
- SPT Badan (PT/CV), pisah harta (PH) / memilih terpisah (MT), penghasilan luar negeri (PPh 24), rugi usaha & kompensasi kerugian, WNA/WP yang datang/pergi di tengah tahun, warisan belum terbagi → **di luar cakupan**, arahkan ke konsultan pajak / Kring Pajak 1500200.
- Mengisi, menandatangani, atau mengirim SPT ke DJP atas nama pengguna → **tolak dengan sopan**; skill hanya menghitung & menyiapkan checklist. Jangan meminta password/kode otorisasi Coretax.

## Input
| Info | Wajib? | Default / cara tanya |
|---|---|---|
| Status PTKP per **1 Januari** tahun pajak (TK/K/K-I + jumlah tanggungan) | Ya | Tanyakan; anak/tanggungan > 3 → pakai 3 |
| Tahun pajak | Tidak | Tahun lalu (sebutkan asumsi) |
| Tiap bukti potong A1/A2: **penghasilan neto** & PPh 21 dipotong | Bila karyawan | Bila hanya tahu bruto → `--a1-bruto` (sebut: kurang tepat) |
| Usaha/pekerjaan bebas: peredaran bruto setahun + persen norma (NPPN), **atau** neto dari pembukuan | Bila ada | Persen norma: minta pengguna cek lampiran PER-17/PJ/2015 (KLU + kota); jangan menebak |
| Sudah kirim pemberitahuan NPPN ke DJP (paling lambat 31 Maret tahun itu)? | Bila NPPN | Tanyakan |
| Omzet & PPh final 0,5% (PP 55) setahun | Bila ada | Hanya dicatat. **Hanya untuk usaha** (dagang/produksi/jasa biasa) — penghasilan **pekerjaan bebas** (dokter, pengacara, notaris, akuntan, arsitek, konsultan, seniman/influencer, penceramah, penulis, agen/perantara) tidak boleh 0,5%, wajib NPPN/pembukuan (PP 55/2022 Ps. 56 s.t.d.d. PP 20/2026) |
| Zakat mandiri ke BAZNAS/LAZ resmi (bukan yang dipotong kantor) | Tidak | 0 |
| PPh 21 bukan pegawai, PPh 22, PPh 23, angsuran PPh 25 yang sudah dibayar | Tidak | 0. **Jasa/fee yang diterima orang pribadi** (konsultan, freelancer, tenaga ahli) dipotong klien dengan **PPh 21 bukan pegawai** (bukti potong BP21; PMK 168/2023) → `--pph21-lain`, **bukan PPh 23**. PPh 23 hanya untuk jenis lain (mis. sewa alat, royalti, bunga, hadiah). Saat bertanya, tulis "PPh 21 yang dipotong klien (bukti potong BP21)" |
| PPh final 0,5% yang terlanjur disetor atas penghasilan **pekerjaan bebas** | Bila ada | `--final-salah-skema` (tidak dikreditkan, tidak masuk Lampiran 2) |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan) + jalur cepat ("kalau mau cepat, sebutkan status & angka di bukti potong, sisanya saya anggap 0"). Contoh: `examples/04-input-kurang.md`.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. Petakan cerita pengguna ke input di atas. Satu pemberi kerja = satu `--a1`. Istri yang hanya bekerja di 1 kantor biasanya **tidak** digabung (pakai K/.., bukan K/I).
2. Jalankan script (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/spt_op.py --status K/1 --tahun 2025 --a1 90jt 1.350.000 --a1 60jt 0
   ```
   Opsi lain (bisa digabung):
   - `--a1-bruto BRUTO PPH21 [BULAN] [IURAN]` — bila neto bukti potong tidak diketahui.
   - `--nppn BRUTO PERSEN` (ulang per jenis usaha) + `--nppn-diberitahukan ya|tidak`.
   - `--pembukuan-neto NETO` · `--lain-neto NETO` · `--omzet-final OMZET --pph-final PPH`.
   - `--zakat` · `--pph21-lain` (termasuk PPh 21 bukan pegawai yang dipotong klien atas jasa orang pribadi) · `--pph22` · `--pph23` · `--pph25` · `--final-salah-skema`.
   - `--hari-ini YYYY-MM-DD` · `--format json`.
   **Selalu isi `--hari-ini` dengan tanggal hari ini** (dari percakapan/sistem). Jangan mengira-ngira apakah tenggat sudah lewat.
   Angka: format Indonesia (`1.250.000`, `2,5jt`, `500rb`, `1,2 miliar`). Angka ambigu (`1,500`, `2.5jt`, `5m`, `114,000,000`) **ditolak** — tanyakan ulang ke pengguna, jangan menebak.
3. **Salin baris "⏰ Status tenggat lapor" + saran + konsekuensinya dari script apa adanya, di bagian paling atas jawaban** (JSON: `status_tenggat`). Jangan pernah menulis "Batas lapor: 31 Maret …" saja tanpa status itu. Bila status `TERLAMBAT` atau `LEWAT_MASA_BEBAS_SANKSI`: katakan jelas batasnya **sudah lewat**, sarankan **segera lapor (dan bayar bila kurang bayar) setelah konsultasi singkat** ke Kring Pajak 1500200/KPP/konsultan; **jangan** menulis "jangan buru-buru lapor", "masih ada waktu", atau tanggal yang sudah lewat sebagai rencana. Tarif bunga per bulan **jangan dikarang** — sebut cara cek (KMK tarif bunga bulan berjalan, fiskal.kemenkeu.go.id / pajak.go.id / Kring Pajak).
   Lalu salin tabel & angka dari output script **apa adanya**. Lalu tulis penjelasan bahasa awam 3–5 kalimat: kenapa kurang/lebih bayar (mis. "dua kantor sama-sama memakai PTKP penuh, jadi saat digabung ada pajak yang belum terpotong").
   **Karyawan 1 pemberi kerja tapi hasilnya kurang/lebih bayar** (script memberi peringatan "CEK ULANG bukti potong A1"): jangan langsung suruh bayar. Jelaskan dengan bahasa awam: "Kantor biasanya sudah menghitung ulang pajak setahun di gaji bulan terakhir, jadi kalau hanya satu kantor hasilnya umumnya nihil. Selisih ini tanda ada yang perlu dicek dulu." Sarankan cek dengan HRD/bagian gaji: status PTKP di A1 (menikah/anak sudah diperbarui?), angka neto & PPh 21 yang diketik sama persis dengan A1, dan tidak ada A1 lain/pembetulan. Bila A1 memang benar, hasil script yang dipakai.
4. Tambahkan **peta ke Coretax** (tabel di bawah) dan **langkah berikutnya** sesuai hasil (KB: bayar dulu lewat kode billing; LB: pilih restitusi/kompensasi; nihil: tinggal lapor).
5. Sertakan peringatan, catatan, checklist dokumen, dan disclaimer dari output.
6. **Fallback tanpa Python:** hitung manual dengan rumus di bawah, tunjukkan setiap langkah, dan tulis "dihitung manual — cek ulang".

## Rumus (untuk hitung manual)
Dasar & sumber: `references/regulasi.md` (dicek 2026-09-30).
```
neto_pekerjaan = Σ "penghasilan neto" tiap bukti potong A1/A2
  (dari bruto: bruto − min(5% bruto; Rp500.000 × bulan) − iuran pensiun/JHT/JP pegawai)
neto_NPPN      = peredaran bruto × persen norma (dibulatkan ke rupiah terdekat)
neto           = neto_pekerjaan + neto_usaha + neto_lain − zakat (maks. sebesar jumlah neto)
PTKP           = 54 jt + 4,5 jt (kawin) + 54 jt (istri digabung, K/I) + 4,5 jt × tanggungan (maks 3)
PKP            = neto − PTKP, dibulatkan KE BAWAH ke ribuan (min 0)
PPh terutang   = 5% × s.d. 60 jt + 15% × 60–250 jt + 25% × 250–500 jt + 30% × 500 jt–5 M + 35% × > 5 M
selisih        = PPh terutang − (PPh 21 semua bukti potong + PPh 22 + PPh 23 + PPh 25 dibayar)
  > 0 kurang bayar (PPh 29) · < 0 lebih bayar · 0 nihil
PPh 25 tahun depan (bila ada usaha/pekerjaan bebas) = (PPh terutang − PPh 21/22/23) ÷ 12
```
Omzet PPh final 0,5% **tidak** masuk rumus di atas (dilaporkan terpisah). Beda dua jalur ini:
- **PPh final 0,5%** (PP 55/2022 s.t.d.d. PP 20/2026): untuk **usaha** OP dengan peredaran bruto ≤ Rp4,8 M; omzet s.d. Rp500 jt pertama setahun tidak kena; pajak = 0,5% × omzet (bukan laba), sudah lunas saat disetor, tidak dikreditkan.
- **Pekerjaan bebas** (profesi/keahlian: dokter, pengacara, notaris, akuntan, arsitek, konsultan, seniman/influencer, penceramah, penulis, perantara, dll.): **tidak boleh** 0,5%; neto dihitung NPPN/pembukuan lalu tarif Pasal 17. Bila pengguna mencampur keduanya, pisahkan dulu; ragu termasuk pekerjaan bebas atau tidak → tanyakan/arahkan ke Kring Pajak.
- **Pekerjaan bebas yang terlanjur setor 0,5%:** hitung penghasilannya dengan `--nppn`/`--pembukuan-neto` dan isi setoran itu di `--final-salah-skema` (BUKAN `--omzet-final`/`--pph-final`). Setoran itu **tidak dikreditkan** dan **tidak dilaporkan di Lampiran 2**; arahkan ke permohonan **pengembalian pajak yang seharusnya tidak terutang** lewat Coretax (menu Pembayaran, formulir restitusi). Pemindahbukuan umumnya tidak bisa karena setoran PPh final UMKM dianggap penyampaian SPT Masa (PMK 81/2024 Ps. 109 ayat (3)). Wajib sarankan konfirmasi ke KPP/Kring Pajak 1500200 atau konsultan pajak (⚠️ PERLU REVIEW konsultan pajak).

## Peta ke SPT Coretax (tahun pajak 2025 dst.)
Formulir 1770/1770S/1770SS **sudah dihapus**; sekarang satu SPT Tahunan PPh OP dinamis (PER-11/PJ/2025). Kode lampiran bisa berubah — cocokkan di layar Coretax.

| Angka dari script | Bagian di Coretax |
|---|---|
| Neto pekerjaan, daftar bukti potong, harta, utang, tanggungan | Lampiran 1 (bukti potong dari pemotong biasanya sudah terisi otomatis) |
| Omzet & PPh final 0,5% (**hanya usaha**, bukan setoran salah skema pekerjaan bebas) | Lampiran 2 (penghasilan final) & L-3B (rekap peredaran bruto) |
| Neto usaha/pekerjaan bebas (NPPN/pembukuan) | Lampiran 3 (L-3A-4 / L-3A-1..3) |
| Zakat | Pengurang penghasilan (Lampiran 5 / Bagian B) |
| Neto, PTKP, PKP, PPh terutang | Induk Bagian B & C |
| Kredit pajak, KB/LB | Induk Bagian D & E (LB: Bagian G) |
| PPh 25 tahun depan | Induk Bagian H / Lampiran 4 |

## Format output
```
## Hitungan SPT Tahunan PPh OP — Tahun Pajak <tahun> (status <PTKP>)
1. Penghasilan neto (tabel)   2. PTKP & PKP   3. PPh terutang per lapisan
4. Kredit pajak               5. Hasil: KURANG BAYAR / LEBIH BAYAR / NIHIL (+ PPh 25 depan)
(di awal) ⏰ Status tenggat lapor + saran + konsekuensi       ← dari script, wajib
Batas lapor · ⚠️ Peringatan · Catatan · Checklist dokumen      ← dari script
Penjelasan bahasa awam · Peta ke Coretax · Langkah berikutnya   ← dari agent
_Disclaimer_
```

## Contoh
**Input:** "Tahun 2025 saya pindah kerja. Kantor lama A1 neto 90 juta PPh 21 1.350.000, kantor baru neto 60 juta PPh 21 nol. Status K/1."

**Perintah:** `python3 <folder-skill-ini>/scripts/spt_op.py --status K/1 --tahun 2025 --a1 90jt 1.350.000 --a1 60jt 0`

**Inti output:** neto Rp150.000.000 − PTKP Rp63.000.000 = PKP Rp87.000.000 → PPh Rp3.000.000 + Rp4.050.000 = **Rp7.050.000**; kredit Rp1.350.000 → **KURANG BAYAR Rp5.700.000**. Penjelasan: masing-masing kantor memakai PTKP penuh dan tarif terendah, padahal setelah digabung sebagian penghasilan masuk lapisan 15%. Contoh lengkap: `examples/01-dua-pemberi-kerja.md`.

## Checklist sebelum mengirim hasil
- [ ] Status PTKP sesuai keadaan 1 Januari; asumsi (tahun, status, nilai 0) disebutkan.
- [ ] Angka neto diambil dari bukti potong (bukan bruto) bila tersedia; semua bukti potong ikut.
- [ ] Persen NPPN berasal dari pengguna/lampiran PER-17/PJ/2015, bukan tebakan; status pemberitahuan NPPN ditanyakan.
- [ ] Zakat lewat kantor tidak dihitung dua kali; omzet final tidak masuk tarif Pasal 17.
- [ ] Status tenggat (`--hari-ini` = hari ini) disalin di awal; bila terlambat: "sudah lewat" + segera lapor setelah konsultasi, tanpa tarif bunga karangan.
- [ ] Angka disalin dari script; penjelasan awam + peta Coretax + langkah berikutnya ada.
- [ ] Disclaimer ada: bukan konsultan pajak, pembulatan belum dicocokkan dengan Coretax, tidak mengirim SPT.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` untuk: status tidak dikenal/tanggungan > 3, angka ambigu/negatif, persen norma di luar 0–100, NPPN dengan peredaran bruto ≥ Rp4,8 M, tanpa penghasilan. Jelaskan dengan bahasa sederhana dan minta data yang benar.
- Neto usaha negatif (rugi) ditolak → arahkan ke konsultan (kompensasi kerugian di luar cakupan).
- NPPN tanpa pemberitahuan: hasil hanya simulasi — menurut DJP WP dianggap memilih pembukuan (⚠️ PERLU REVIEW nomor pasal & konsekuensi jangka panjang).
- **Tenggat wajib dibandingkan dengan tanggal hari ini.** Jangan pernah menyarankan langkah dengan tanggal yang sudah lewat. Pemberitahuan NPPN = paling lambat **31 Maret tahun pajak yang bersangkutan** (UU PPh Ps. 14 ayat (2); PMK 81/2024 Ps. 450 ayat (2)); script mencetak `nppn_tahun_berjalan` (sudah lewat/belum, per `--hari-ini`) — salin apa adanya. Bila sudah lewat: katakan jelas tahun pajak berjalan **dianggap memilih pembukuan** (UU PPh Ps. 14 ayat (5)) → mulai catat pembukuan sekarang; pemberitahuan berikutnya baru untuk tahun pajak berikutnya (s.d. 31 Maret tahun itu), dengan catatan DJP menyatakan WP yang sudah menyelenggarakan pembukuan tidak dapat kembali ke NPPN (PMK 81/2024 Ps. 463 s.t.d.d. PMK 1/2026) → konfirmasi KPP/konsultan (⚠️ PERLU REVIEW konsultan pajak).
- **Batas lapor:** paling lambat 3 bulan setelah akhir tahun pajak → **31 Maret** tahun berikutnya (UU KUP Ps. 3). TP 2025: jatuh tempo **tetap 31 Maret 2026**; KEP-55/PJ/2026 **bukan perpanjangan**, hanya menghapus sanksi (denda & bunga) bila lapor/bayar s.d. 30 April 2026. Bila 31 Maret jatuh pada Sabtu/Minggu/libur, cek pengumuman DJP terbaru (⚠️ PERLU REVIEW: belum terverifikasi apakah aturan "hari kerja berikutnya" PMK 81/2024 berlaku untuk SPT Tahunan) — sarankan lapor lebih awal.
- Angka negatif ditolak dengan pesan ramah (isi angka positif). "5,054 miliar" diterima; "5,054 M"/"5m" ditolak (M = juta atau miliar?) → minta ditulis "miliar" atau angka penuh.
- Sanksi: denda telat lapor SPT Tahunan OP Rp100.000 (UU KUP Ps. 7 ayat (1)); bunga kurang bayar yang telat disetor (UU KUP Ps. 9 s.t.d.t.d. UU HPP; tarif KMK per bulan, bagian bulan = 1 bulan, maks. 24 bulan) **tidak dihitung** karena tarifnya berubah tiap bulan — script mencetak jumlah bulan terlambat & cara cek tarif.
- Jangan mengklaim hasil pasti sama dengan Coretax; Coretax yang final. Selalu sarankan cek ulang ke DJP/konsultan untuk kasus besar atau tidak biasa.
