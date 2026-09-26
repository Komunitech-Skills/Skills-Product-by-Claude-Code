# 06 — Uji ulang v1.0.1 (penguji independen, Tahap 6 butir 7)

- **Tanggal:** 2026-09-25
- **Penguji:** agent terpisah dari pembuat & perevisi skill. Hanya membaca folder `skills/pesan-prospek-wa/` (plus deskripsi `riset-calon-pelanggan` untuk cek batas cakupan).
- **Lingkungan:** salinan di scratchpad `.../scratchpad/uji2-ppw/pesan-prospek-wa/` (tanpa `__pycache__`), Python 3.11, Linux. Tidak dipasang ke `.claude/skills`.
- **Verifikasi independen:** hitung karakter/kata dengan `wc -m` / `wc -w` (bukan Python); tautan wa.me di-decode dengan **Perl** (regex `%XX`) dan **Node.js** (`URL.searchParams`), bukan `urllib`.
- **Platform teruji:** `claude-code (simulasi agent)` saja.

## 1. Tes bawaan
`python3 tests/uji_regresi.py` → **66 tes, semua OK** (naik dari 43). `python3 scripts/validate.py` → 62 skill valid. SKILL.md **100 baris** (< 300).

## 2. Temuan lama → status

| # | Temuan uji pertama | Status v1.0.1 | Bukti uji ulang |
|---|---|---|---|
| B1 | Asal kontak tidak dikenali untuk 4/5 pola `pola-pembuka.md`; "dari ibu" salah-positif | ✅ **Diperbaiki (inti)** · ⚠️ sisa heuristik longgar (N2) | Keenam kutipan `> "..."` di `pola-pembuka.md` diekstrak otomatis dan dicek: **6/6 terdeteksi**. "Resep kue ini warisan dari ibu saya" → tidak terdeteksi (benar). Tapi contoh asli B1 "bertemu **Ibu** di Jakarta Food & Franchise Expo" **masih tidak terdeteksi**, dan ada salah-positif baru (lihat N2). |
| B2 | "+62 0812…", "0062…", 14 digit, telepon rumah, digit non-ASCII | ✅ Diperbaiki | `+62 0812-3456-7890`, `+6208123456789`, `0062 0812 3456 7890`, `+0062812345678` → `62812…` benar. `08123456789012` (14 digit), `021-5551234`, `+62 21 5551234` → ditolak dengan pesan jelas ("bukan nomor seluler, mis. telepon rumah"). Full-width `０８１２…` & Arab-Indik `٠٨١٢…` → ditolak, pesan kini benar ("harus angka biasa 0-9"). Berspasi/strip/titik/kurung → benar. |
| B3 | HRD/PPN/SPT/BPJS dsb. dianggap "teriak" | ✅ Diperbaiki · ⚠️ N4 | HRD, PPN, SPT, BPJS, SOP, HIPMI, KADIN → [OK]. "PROMO BESAR HARI INI SAJA" tetap tertangkap. Sisa: **WIB/WITA/WIT** tertandai (N4). |
| B4 | `--jam-kirim` menolak `19.30`; makna jam ambigu | ✅ Diperbaiki | `19.30`, `19:30`, `1930`, ` 19.30 ` diterima; `7.30`/`0730` → di luar jam wajar; `730`, `24.00`, `19,30`, `19:30:00`, `19.30 WIB`, `ab.cd`, `1930x` → error jelas, exit 1. `--zona WITA/wita/WIT/WIB` diterima; `GMT`/`WITa` ditolak argparse (exit 2, pesan jelas). Help, output script & SKILL.md Langkah 6/8 menyebut "waktu SETEMPAT PENERIMA" + WITA=WIB+1, WIT=WIB+2. Jam tanpa zona → peringatan zona. |
| B5 | Tumpang tindih dengan `riset-calon-pelanggan` | ✅ Diperjelas di sisi skill ini | SKILL.md baris 20: riset = cari & saring daftar (pesan hanya bonus); skill ini = satu prospek jelas, 3 varian + script + wa.me. Deskripsi `riset-calon-pelanggan` masih menyebut "menyusun pesan pembuka personal WA" (tidak diubah) → keputusan katalog tetap untuk pemilik, risiko kecil. |
| B6 | Presisi pasal | ✅ Diperbaiki | Lihat §5. |
| B7 | Emoji tidak dicek | ✅ Diperbaiki · ⚠️ N3 | 1 & 3 emoji → tanpa peringatan; 4 → peringatan. Tapi ambang **3** bertentangan dengan `checklist-anti-blokir.md` "**Maksimal 1 emoji**" (N3). |
| B8 | Baris baru tidak memisah kalimat | ✅ Diperbaiki | Daftar poin ✅ 4 baris tanpa titik (38 kata total) → tidak ada peringatan kalimat panjang. |
| B9 | V3 rutin > 500 karakter | ✅ Diperbaiki | Target ≤ 500 di template & SKILL.md. Skenario ulang: V3 = 445 & 434 karakter. |
| B10 | Label "Singkat (1-2 kalimat)" | ✅ Diperbaiki | "± 2-3 kalimat, target ≤ 300 karakter". |
| B11 | Detail layanan boleh diasumsikan? | ✅ Diperbaiki | Langkah 5 + template: detail tak diberikan → `[isi: ...]` atau Asumsi. |
| B12 | V3 mendaftar fitur | ✅ Diperbaiki | Template V3: satu kalimat akibat/masalah bagi penerima, lalu manfaat. Dipakai di skenario ulang. |

## 3. Bug / temuan BARU

| # | Prioritas | Temuan | Usulan |
|---|---|---|---|
| **N1** | Sedang | `cek --file` dengan file **bukan UTF-8** (mis. Latin-1 `é`, atau file biner) → **traceback `UnicodeDecodeError`**. Hanya `OSError` yang ditangkap (`main()`, baris ± 424). Pengguna awam Windows sering menyimpan .txt ANSI/Latin-1. | Tangkap `UnicodeDecodeError` → pesan "simpan file sebagai UTF-8", atau baca dengan `encoding="utf-8-sig", errors="replace"` + peringatan. Tambah tes. |
| **N2** | Sedang | Heuristik asal kontak masih longgar dua arah. **Salah-negatif** (frasa wajar): "bertemu **Ibu** di … Expo" (contoh B1 sendiri), "ngobrol di … Expo", "follow IG Kakak", "Nomor Bapak saya peroleh dari Pak Budi", "Pak Andi … merekomendasikan Ibu", "Kita satu grup di HIPMI", "Kartu nama Bapak saya terima saat seminar", "lihat di LinkedIn/Tokopedia". **Salah-positif** (tidak menyebut asal kontak, tapi dianggap "Ya"): "dari teman-teman petani", "diproses di acara roasting", "Ada kontak dari kami", "Harga kami lihat dari kualitas", "unggahan bukti transfer", "grup whatsapp khusus pelanggan", "ketemu di jalan masalah". Salah-positif lebih berbahaya: pesan tanpa asal kontak lolos diam-diam. SKILL.md Langkah 6 sudah menyuruh penilaian manual, jadi dampak terbatas. | Kata kunci generik ("dari teman", "kontak dari", "di acara", "lihat dari", "unggahan", "grup whatsapp", "ketemu di", "bertemu di") diganti regex berjangkar (mis. `(nomor|kontak)\s+(bapak|ibu|kakak|anda)\b.{0,40}\b(dari|di)\b`, `(bertemu|ketemu|ngobrol|mengobrol)\b.{0,25}\bdi\s+(pameran|expo|bazar|acara|seminar)`, `merekomendasikan`, `\b(linkedin|tokopedia|shopee)\b`, `kartu nama`, `(satu|sesama) grup`). Tambah tes salah-positif & salah-negatif di atas. |
| N3 | Rendah | Ambang emoji tidak konsisten: script & SKILL.md = maks **3**, `checklist-anti-blokir.md` = maks **1**. | Samakan (mis. checklist "idealnya 1, maks 3", atau script ambang 1). |
| N4 | Rendah | `WIB`, `WITA`, `WIT` tertandai "huruf kapital (teriak)", padahal skill sendiri menganjurkan menyebut zona. Juga `ABC` di "PT ABC", `KPR`, `BTN`, `RSUD`, `POS`, `ERP`, `CRM`, `HPP`. | Tambah WIB/WITA/WIT (+ beberapa istilah umum) ke `SINGKATAN_AMAN`; pertimbangkan hanya memperingatkan bila ≥ 2 kata kapital beruntun atau kata ≥ 5 huruf. |
| N5 | Rendah | Hitung emoji kurang akurat: 👍🏽 dihitung 2 (modifier warna kulit), keluarga ZWJ 👨‍👩‍👧 = 3, bendera 🇮🇩 = 0, ⭐ (U+2B50) = 0. | Buang modifier U+1F3FB–1F3FF & ZWJ sebelum hitung; tambah rentang U+1F1E6–1F1FF (bendera, bagi 2) dan U+2B00–2BFF. |
| N6 | Rendah | Nomor dengan **en-dash** "0812–3456–7890" (hasil autocorrect Word/WA) atau garis bawah ditolak; link tanpa skema (`bit.ly/xyz`, `toko.id/katalog`) tidak dihitung sebagai link. | Tambah `–—_` ke karakter yang dibuang; regex link tambah pola domain `\b[\w-]+\.(id|com|ly|co|me)/\S*`. |
| N7 | Rendah | Jam **tepat 20.00** dinilai "di luar rentang 08.00–20.00" — teks rentang terbaca inklusif. File ber-BOM dihitung +1 karakter. | Tulis "08.00–19.59" atau terima 20.00; baca file dengan `utf-8-sig`. |
| N8 | Rendah | Tes B1 menyalin kalimat pola secara manual (pola #6 "kontak lama" tidak dites); jika `pola-pembuka.md` diubah, tes tidak ikut. | Tes membaca semua baris `> "..."` dari `pola-pembuka.md` secara otomatis (seperti yang dilakukan penguji). |
| N9 | Rendah (hukum) | `dasar-hukum-wa.md` menulis hak "menarik persetujuan/keberatan" di bawah "Pasal 5–8 dst."; hak menarik persetujuan ada di **Pasal 9** (keberatan atas keputusan otomatis Pasal 10). Tertolong oleh "dst.", tapi bisa ditulis "Pasal 5–10". Pasal 65 ditulis "sehingga merugikan", teks aslinya "yang dapat mengakibatkan kerugian". | Presisi kecil, tidak salah arah. |

Data rusak yang **ditangani dengan baik** (baru dicoba): pesan kosong, file = direktori, CRLF (dihitung 2 baris, benar), teks 25.000 karakter (peringatan >700, tanpa crash), `--pesan "   "` pada `wa` (tautan tanpa `?text=`), nomor `620`, `00`, `+62 +812`, `tel:+62…`, `0812 3456 7890 ext 1`, campuran digit ASCII+full-width → ditolak dengan pesan jelas; `0 0 6 2 8 1 2 …` → dinormalisasi benar.

## 4. Skenario ulang (mengikuti SKILL.md v1.0.1)

### Skenario 02 — Roastery → kafe dari Google Maps (santai, "Kak")
Input sama dengan `02-supplier-kopi-ke-kafe-google-maps.md` (Bima, Lereng Arjuno Roastery, Malang → Kopi Senja Dago, Bandung; nomor `+62 857-2211-3344` dari listing Maps; single origin Arjuno/Ijen/Dampit, min 5 kg, kirim maks 3 hari setelah sangrai, 2 sampel 100 gr gratis).

Langkah: cakupan OK (pesan pertama, satu kafe) → sumber sah (listing bisnis publik, `dasar-hukum-wa.md` §1) → pola #3 **dipakai hampir persis** ("Saya melihat … di Google Maps saat mencari kafe specialty di area Dago") → **script kini mendeteksi asal kontak tanpa perlu menulis ulang** (B1 tertutup untuk kasus ini).

**Varian 1 — Singkat**
```
Selamat pagi, Kak. Saya Bima dari Lereng Arjuno Roastery, Malang. Saya melihat Kopi Senja Dago di Google Maps saat mencari kafe specialty di area Dago. Boleh saya kirim daftar biji single origin kami? Boleh diabaikan bila belum relevan ya, Kak.
```
Script (`--jam-kirim 09.30 --zona WIB`): 244 kar., 40 kata, asal kontak Ya, opsi keluar Ya, jam wajar → **[OK]**. Independen `wc`: 244 / 40 ✔.

**Varian 2 — Sedang**
```
Selamat pagi, Kak. Perkenalkan saya Bima dari Lereng Arjuno Roastery di Malang. Saya melihat Kopi Senja Dago di Google Maps saat mencari kafe specialty di area Dago, dan dari foto menunya sepertinya banyak manual brew. Kami menyangrai biji single origin Jawa Timur (Arjuno, Ijen, Dampit). Boleh saya kirim daftar harganya? Boleh diabaikan bila belum relevan ya, Kak.
```
Script: 366 kar., 57 kata → **[OK]**. `wc`: 366 / 57 ✔.

**Varian 3 — Dengan nilai tambah**
```
Selamat pagi, Kak. Saya Bima dari Lereng Arjuno Roastery, Malang, menemukan Kopi Senja Dago di Google Maps saat mencari kafe specialty di Dago. Untuk menu manual brew, biji yang terlalu lama setelah sangrai bisa membuat rasa cepat datar. Kami kirim single origin Jatim (Arjuno, Ijen, Dampit) maks. 3 hari setelah sangrai, min. order 5 kg. Kalau Kakak berkenan, boleh saya kirim 2 sampel 100 gr gratis? Boleh diabaikan bila belum relevan ya, Kak.
```
Script: **445 kar.** (≤ 500 ✔), 73 kata → **[OK]**. `wc`: 445 / 73 ✔. Kalimat akibat/masalah (B12) ada; semua detail layanan berasal dari pengguna (tidak ada harga, testimoni, atau jumlah pelanggan yang dikarang). Kata "gratis" tanpa tanda seru tidak memicu peringatan spam (benar).

**Tautan wa.me (V3):** `https://wa.me/6285722113344?text=Selamat%20pagi%2C%20Kak.%20…` — nomor benar; decode Perl → teks **identik** byte demi byte dengan draf.
**Saran jam kirim:** 08.00–20.00 WIB (Bandung); hindari jam sibuk kafe (buka/jam makan siang) — mis. 09.30 atau 14.30 WIB.
**Asumsi:** tidak ada.

### Skenario 03 — Konsultan pajak, referral, formal, penerima di Makassar (WITA)
Input sama dengan `03-konsultan-pajak-referral-formal.md` (Dewi Anggraini, Brevet A & B; referral Pak Hendra Wijaya yang mengizinkan namanya disebut; Pak Surya, CV Surya Bahari, Makassar; nomor `62 811-4455-6677`; rencana kirim 19.30).

Langkah: cakupan OK → referral dengan izin → pola #1 → formal ("Bapak", "berkenan", tanpa "ya/Kak") → domain pajak: murni perkenalan, tanpa janji hasil/hitungan → **zona waktu (Langkah 6/8):** penerima WITA; 19.30 WIB = **20.30 WITA**. Script `--jam-kirim 20.30 --zona WITA` → "di luar rentang wajar … waktu SETEMPAT PENERIMA" → sarankan besok **09.00 WITA (= 08.00 WIB)**. Format titik `20.30` & `0900` kini diterima (B4 tertutup). PPN/SPT tidak dipakai di draf, tapi diuji terpisah → tidak tertandai (B3 tertutup).

**Varian 1 — Singkat**
```
Selamat pagi, Bapak Surya. Saya Dewi Anggraini, konsultan pajak independen. Saya mendapat nomor Bapak dari Bapak Hendra Wijaya, yang menyarankan saya menghubungi Bapak. Apakah Bapak berkenan saya kirimkan ringkasan layanan saya? Mohon maaf mengganggu, pesan ini boleh diabaikan bila belum relevan.
```
Draf pertama 308 kar. (> target 300) → dipangkas ("di Jakarta" dibuang). Script (`--jam-kirim 09.00 --zona WITA`): **297 kar.**, 41 kata → **[OK]**. `wc`: 297 / 41 ✔.

**Varian 2 — Sedang**
```
Selamat pagi, Bapak Surya. Perkenalkan, saya Dewi Anggraini, konsultan pajak independen di Jakarta (Brevet A & B). Saya mendapat nomor Bapak dari Bapak Hendra Wijaya, yang menyampaikan bahwa CV Surya Bahari sedang mencari pendamping pajak bulanan dan SPT Tahunan badan. Apakah Bapak berkenan saya kirimkan ringkasan layanan saya? Mohon maaf mengganggu, pesan ini boleh diabaikan bila belum relevan.
```
Script: 398 kar. (≤ 400 ✔), 58 kata → **[OK]**. `wc`: 398 / 58 ✔.

**Varian 3 — Dengan nilai tambah**
```
Selamat pagi, Bapak Surya. Saya Dewi Anggraini, konsultan pajak independen (Brevet A & B), mendapat nomor Bapak dari Bapak Hendra Wijaya. Menjelang Coretax, pelaporan bulanan dan SPT Tahunan badan sering menyita waktu pemilik usaha. Saya dapat mendampingi CV Surya Bahari untuk kedua hal tersebut. Bila Bapak berkenan, bolehkah saya kirimkan ringkasan layanan saya? Mohon maaf mengganggu, pesan ini boleh diabaikan bila belum relevan.
```
Script: **434 kar.** (≤ 500 ✔), 63 kata → **[OK]**. `wc`: 434 / 63 ✔. Tidak mengarang: tidak ada tarif, jumlah klien, "dijamin lancar/bebas denda"; kredensial hanya Brevet A & B (dari pengguna); kalimat masalah umum dan wajar, bukan klaim hasil.

**Tautan wa.me (V3):** `https://wa.me/6281144556677?text=Selamat%20pagi%2C%20Bapak%20Surya.%20…` — decode Perl → **identik**. Uji tambahan karakter khusus (`& # + = % ? " / é`, emoji, baris baru, nomor `0062 0857 …`) → decode Node `URL.searchParams` **identik**.
**Saran jam kirim:** jangan malam ini (20.30 WITA). Kirim besok 09.00–11.00 WITA (= 08.00–10.00 WIB).
**Asumsi:** Pak Hendra sudah mengizinkan namanya disebut (dinyatakan pengguna).

**Kesimpulan skenario:** kedua skenario berjalan lancar mengikuti SKILL.md tanpa jalan memutar; semua varian lolos script dan target panjang per varian; tidak ada detail dikarang.

## 5. Cek `references/dasar-hukum-wa.md` (verifikasi web search 2026-09-25)

| Klaim | Hasil verifikasi | Status |
|---|---|---|
| UU PDP Pasal 20 (dasar pemrosesan); ayat (2) huruf f "kepentingan yang sah lainnya" + penyeimbangan | Sesuai: huruf f "pemenuhan kepentingan yang sah lainnya dengan memperhatikan tujuan, kebutuhan, dan keseimbangan kepentingan Pengendali dan hak Subjek Data" | ✅ |
| Pasal 65 (larangan memperoleh/mengumpulkan/menggunakan data bukan miliknya secara melawan hukum) & Pasal 67 (pidana) | Sesuai: 65(1) memperoleh/mengumpulkan, 65(3) menggunakan; 67(1) penjara ≤ 5 th dan/atau denda ≤ Rp5 miliar. (MK menolak uji materi 65(2)/67(2) perkara 135/PUU-XXIII/2025 — tidak mengubah isi.) | ✅ (N9: "sehingga merugikan" vs "dapat mengakibatkan kerugian") |
| Hak subjek data "Pasal 5–8 dst." | Pasal 5 hak informasi identitas & dasar pemrosesan; Pasal 8 mengakhiri pemrosesan/menghapus; Pasal 9 menarik persetujuan | ✅ dengan catatan N9 |
| UU 8/1999 Pasal 9–10 (penawaran/promosi/iklan tidak benar/menyesatkan) | Sesuai; sanksi Pasal 62 (≤ 5 th / ≤ Rp2 miliar) | ✅ |
| UU ITE "11/2008 jo. 19/2016 jo. 1/2024", Pasal 28 ayat (1) & Pasal 35 | Penulisan benar; Pasal 28(1) (versi UU 1/2024) = pemberitahuan bohong/informasi menyesatkan yang merugikan konsumen dalam transaksi elektronik; Pasal 35 = manipulasi agar dianggap otentik | ✅ |
| Wajib vs praktik baik | Dipisah jelas: "WAJIB menurut UU (Pasal 65 & 67)" vs "Praktik baik … bukan kewajiban literal UU PDP atas isi pesan" | ✅ |
| Disclaimer & tanggal | "Bukan nasihat hukum … dicek terakhir 2026-09-25" + saran konsultan untuk kasus berisiko | ✅ |

Sumber: [JDIH BPK UU 27/2022](https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022), [uupdp-info.id Pasal 65](https://uupdp-info.id/pasal-65/), [uupdp-info.id Pasal 67](https://uupdp-info.id/pasal-67/), [hukumonline — sanksi UU PDP](https://www.hukumonline.com/berita/a/ancaman-sanksi-administratif-hingga-pidana-dalam-uu-pelindungan-data-pribadi-lt633c69ce2de5c/), [jogloabang — hak subjek data](https://www.jogloabang.com/pustaka/uu-27-2022-pelindungan-data-pribadi), [MKRI — uji materi Pasal 65(2)](https://www.mkri.id/berita/larangan-ungkap-data-pribadi-dalam-uu-pdp-perlu-tafsir-ketat-dan-tegas-23882), [JDIH BPK UU 8/1999](https://peraturan.bpk.go.id/Details/45288/uu-no-8-tahun-1999), [JDIH BPK UU 1/2024](https://peraturan.bpk.go.id/details/274494/uu-no-1-tahun-2024). (pasal.id & abnrlaw.com diblokir proxy.)

## 6. Kepatuhan
- ✅ Tidak ada blast/otomasi kirim; WA mode copilot; batas `riset-calon-pelanggan`/`broadcast-wa`/`follow-up-prospek` jelas.
- ✅ Frontmatter hanya `name` & `description`; SKILL.md 100 baris; script Python standar tanpa jaringan.
- ✅ Riwayat versi di `ATTRIBUTION.md` akurat terhadap perubahan yang diverifikasi (66 tes).
