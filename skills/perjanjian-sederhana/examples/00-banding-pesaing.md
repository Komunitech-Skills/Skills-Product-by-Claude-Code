# 00 — Uji banding pesaing (S1: perjanjian reseller + permintaan harga minimum)

> **Catatan 1.0.9:** berkas ini rekaman uji versi lama dan dibiarkan apa adanya sebagai bukti. Gaya isian `[[...]]` di dalamnya sudah tidak dipakai; sejak 1.0.9 satu gaya isian saja: `[isi: ...]`.

## Pencarian yang dilakukan (2026-09-23)
| Sumber | Kata kunci / cara | Hasil |
|---|---|---|
| GitHub/web search | `SKILL.md contract drafting agreement template skill`, `perjanjian kerja sama skill SKILL.md` | stokebuilder/yc-saas-drafting-skill (SaaS AS), borghei/Claude-Skills `contract-and-proposal-writer` (AS/UE/UK/DACH, lisensi MIT + Commons Clause), evolsb/claude-legal-skill (review), claude-office-skills `contract-template` (skills.sh), open-agreements |
| github.com/adamriofc/indonesian-business-agent-skills (dikurasi di (riset internal kurator, tidak disertakan dalam paket)) | clone read-only, folder `legal-id` | **`spk-generator`** (perjanjian jasa/kemitraan, KUHPerdata), `nda-indonesia`, `contract-reviewer`: satu-satunya pesaing berkonteks Indonesia |
| github.com/VoltAgent/awesome-openclaw-skills | grep `contract`, `agreement`, `legal`, `indonesia` | Tidak ada skill perjanjian berbahasa/berhukum Indonesia |
| github.com/anthropics/skills | daftar skill | Tidak ada skill penyusunan perjanjian (hanya docx/pdf umum) |
| manairalabs/bicara-skills, alvinindra/bahasa-skills | daftar skill | Hanya bahasa/penulisan/WA/invoice. Tidak ada perjanjian |

Pesaing yang dibandingkan: **adamriofc — `legal-id/skills/spk-generator/SKILL.md`**, https://github.com/adamriofc/indonesian-business-agent-skills/blob/main/legal-id/skills/spk-generator/SKILL.md, lisensi **MIT**. Pembanding sekunder (hanya dibaca): borghei `contract-and-proposal-writer` (tidak berlaku untuk hukum Indonesia; lisensi Commons Clause melarang penjualan).

Tidak ada script pihak ketiga yang dijalankan. Isi pesaing tidak disalin ke skill kita.

## Isi pesaing (ringkas)
`spk-generator` (±60 baris, berbahasa Inggris dengan istilah Indonesia): dasar Pasal 1320 & 1338 KUHPerdata; input: identitas, lingkup kerja, nilai & termin (termasuk PPN/PPh 23), BAST, pilihan BANI/PN. Pasal wajib: (1) lingkup kerja + BAST, (2) termin pembayaran, (3) wanprestasi dengan 2× surat peringatan + **pengesampingan Pasal 1266 KUHPerdata**, (4) sengketa musyawarah → PN/BANI. Disclaimer: tinjau tim legal sebelum tanda tangan & meterai. Tidak ada daftar penolakan, tidak ada pembahasan persaingan usaha, tidak ada template reseller, tidak ada script terbilang.

## S1 dijalankan dengan instruksi pesaing
Penguji berperan sebagai agent yang memuat `spk-generator`. Permintaan reseller diperlakukan sebagai "partnership contract":

> **PERJANJIAN KERJA SAMA RESELLER** — Nomor: ……
>
> PIHAK PERTAMA: Rina Kartika, NIK ……, alamat ……, pemilik Sambal Mbak Rin. PIHAK KEDUA: Dewi Anggraini, NIK ……, alamat ……, Bandung.
>
> **Pasal 1 – Lingkup Kerja Sama.** PIHAK PERTAMA menunjuk PIHAK KEDUA sebagai reseller Sambal Mbak Rin di Bandung sesuai Lampiran I. Setiap pengiriman dianggap selesai setelah PIHAK KEDUA menandatangani Berita Acara Serah Terima (BAST) barang.
>
> **Pasal 2 – Harga dan Pembayaran.** Harga reseller Rp 18.000 per botol, minimal pembelian 24 botol per bulan, dibayar penuh di muka melalui transfer ke rekening PIHAK PERTAMA. Harga jual kepada konsumen minimal Rp 25.000 per botol; pelanggaran dikenakan denda Rp 5.000.000.
>
> **Pasal 3 – Wanprestasi.** Apabila salah satu pihak wanprestasi, pihak yang dirugikan berhak mengakhiri perjanjian setelah memberikan Surat Peringatan sebanyak 2 (dua) kali berturut-turut, masing-masing dengan waktu perbaikan 7 (tujuh) hari kerja. Para Pihak sepakat mengesampingkan ketentuan Pasal 1266 KUHPerdata sepanjang mensyaratkan putusan hakim untuk pengakhiran tersebut.
>
> **Pasal 4 – Penyelesaian Sengketa.** Musyawarah 30 (tiga puluh) hari kalender; bila tidak tercapai, Pengadilan Negeri Semarang.
>
> Ditandatangani di atas meterai Rp 10.000. *Draf harus ditinjau tim legal sebelum ditandatangani.*

## Tabel penilaian (1–10)
| Kriteria | Skill kita (`perjanjian-sederhana`) | Pesaing (`spk-generator`) |
|---|---|---|
| Kualitas output | 9: 11 pasal lengkap & seimbang, lampiran, daftar kekurangan, pasal ⚠, analisis 1320, checklist, catatan meterai | 5: 4 pasal inti; tidak ada jangka waktu, keadaan memaksa, retur, kerahasiaan, atau lain-lain |
| Kesesuaian konteks Indonesia | 9: bahasa awam, UMKM, UU 5/1999, UU 10/2020, UU PDP, gugatan sederhana, harta bersama | 6: KUHPerdata & BAST/BANI tepat, tetapi instruksi berbahasa Inggris dan berorientasi korporat (PPN/PPh 23, BAST) |
| Akurasi hukum | 9: MAP ditolak dengan dasar; pengesampingan 1266–1267 **ditandai diperdebatkan**; meterai bukan syarat sah dijelaskan benar | 4: klausul harga jual kembali minimum + denda **ikut ditulis**; pengesampingan 1266 dijadikan klausul "wajib" tanpa catatan |
| Siap pakai untuk awam | 9: `[[...]]` + checklist + angka dari script | 5: perlu diisi manual dan ditinjau tim legal (awam tidak punya) |
| **Keseluruhan** | **Menang** | Kalah |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Berita Acara Serah Terima (BAST)** sebagai syarat pelunasan. Berguna untuk template `jasa-freelance` dan `supplier-pemasok` (serah terima barang/pekerjaan tertulis sebelum pembayaran akhir).
2. **Teguran bertahap (2× surat peringatan)** sebelum pengakhiran bisa ditawarkan sebagai klausul pilihan di `references/klausul-pilihan.md` untuk kontrak bernilai lebih besar.
3. **Menanyakan status PPN/PPh 23** saat klien berbentuk badan usaha. Skill kita sudah mengingatkan secara umum, tetapi bisa menambah pertanyaan eksplisit "harga sudah termasuk pajak atau belum?" di input jasa/supplier.
