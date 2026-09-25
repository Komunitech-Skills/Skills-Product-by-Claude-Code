# 00 — Uji banding pesaing: skenario 01

> Penguji independen, 2026-09-25. Skill pesaing hanya **dibaca untuk dinilai**, tidak disalin ke skill kita.

## Pencarian (kata kunci & sumber)
| Kata kunci | Sumber | Hasil |
|---|---|---|
| `privacy policy agent skill SKILL.md github` | Web search | phuryn/pm-skills `privacy-policy`; PGScully/privacy-skill (privacy-compliance); mukul975/privacy-data-protection-skills (282+ skill, GDPR/CCPA/LGPD/PIPL/DPDP); openclaw/skills `metehan777/gdpr-cookie-consent` |
| `clawhub OR skills.sh "privacy policy" skill Indonesia PDP` | Web search (ClawHub, skills.sh, awesome-openclaw-skills) | Tidak ditemukan skill khusus UU PDP Indonesia |
| `generator kebijakan privasi UU PDP gratis Indonesia` | Web search | Tidak ada generator publik khusus UU PDP yang menonjol; hasil hanya artikel/kebijakan instansi |

URL:
- https://github.com/phuryn/pm-skills/blob/main/pm-toolkit/skills/privacy-policy/SKILL.md (dibaca penuh, 238 baris)
- https://github.com/PGScully/privacy-skill (README dibaca: cakupan Australia, EU GDPR/AI Act/Data Act, California CCPA — **tidak mencakup Indonesia**)
- https://github.com/mukul975/privacy-data-protection-skills (deskripsi: GDPR, CCPA, EU AI Act, HIPAA, LGPD, PIPL, DPDP — tidak menyebut Indonesia; tanda "ratusan skill" = pola yang CLAUDE.md waspadai)
- https://github.com/openclaw/skills/blob/main/skills/metehan777/gdpr-cookie-consent/SKILL.md (hanya cookie/GDPR)

Jumlah bintang/instal tidak bisa diverifikasi (akses API GitHub untuk repo luar dibatasi di lingkungan uji).

**Pesaing terpilih:** `phuryn/pm-skills` → `privacy-policy` (skill generator kebijakan privasi umum paling relevan & lengkap untuk tugas yang sama).

## Output agent memakai skill pesaing (skenario 01)
Agent mengikuti proses skill pesaing (Summary → Full Policy 14 bagian dengan penanda `[⚠️ LEGAL REVIEW REQUIRED]` → Compliance Notes), yurisdiksi diisi "Indonesia".
```markdown
## Part 1: Summary
- Product: Kirana Wear online fashion store (kiranawear.id, WooCommerce) + WhatsApp orders
- Data: name, email, phone/WhatsApp, delivery address, order & payment details (Midtrans), device/usage data (cookies, Meta Pixel, Google Analytics)
- Jurisdiction: Indonesia (Law No. 27/2022 on Personal Data Protection); hosting in Singapore
- Key rights: access, correction, deletion, withdraw consent
- Retention: [⚠️ LEGAL REVIEW REQUIRED]
- Contact: [CONTACT_EMAIL]

## Part 2: Full Privacy Policy (Bahasa Indonesia)

# Kebijakan Privasi Kirana Wear
Tanggal berlaku: [tanggal] · Terakhir diperbarui: 25 September 2026

Kebijakan ini menjelaskan bagaimana CV Kirana Busana Nusantara ("Kirana Wear", "kami") mengumpulkan, menggunakan, dan melindungi data pribadi Anda ketika Anda menggunakan kiranawear.id atau menghubungi kami melalui WhatsApp.

## 1. Informasi yang Kami Kumpulkan
- Data pribadi: nama, email, nomor telepon/WhatsApp, alamat pengiriman.
- Data pembayaran: diproses oleh Midtrans; kami tidak menyimpan data kartu lengkap.
- Data penggunaan & perangkat: alamat IP, browser, halaman yang dikunjungi, cookie, Meta Pixel, Google Analytics.
- Komunikasi: pesan WhatsApp/email dengan layanan pelanggan.
- [⚠️ LEGAL REVIEW REQUIRED] Kategori khusus: kami tidak mengumpulkan data sensitif.

## 2. Cara Kami Mengumpulkan
Langsung dari Anda (checkout, akun, chat), otomatis (cookie, pixel, analitik), dan dari pihak ketiga (Midtrans, JNE, J&T).

## 3. Penggunaan Informasi
Memproses & mengirim pesanan; layanan pelanggan; analitik untuk memperbaiki situs; pemasaran & iklan (Meta); keamanan & pencegahan penipuan; kepatuhan hukum.

## 4. Dasar Hukum Pemrosesan [⚠️ LEGAL REVIEW REQUIRED]
- Persetujuan: pemasaran, cookie analitik & iklan.
- Kontrak: pemrosesan pesanan & pengiriman.
- Kewajiban hukum: pencatatan transaksi.
- Kepentingan sah: keamanan & pencegahan penipuan.

## 5. Berbagi Data
Penyedia layanan: hosting ([nama], Singapura), Midtrans, JNE, J&T, Google, Meta; otoritas bila diwajibkan hukum. [⚠️ LEGAL REVIEW REQUIRED] Lokasi pihak ketiga.

## 6. Transfer Internasional [⚠️ LEGAL REVIEW REQUIRED]
Data disimpan di server di Singapura dan dapat diproses oleh Google & Meta di luar Indonesia. Mekanisme: Standard Contractual Clauses / persetujuan pengguna.

## 7. Retensi Data [⚠️ LEGAL REVIEW REQUIRED]
Data akun: selama akun aktif, lalu X bulan. Data transaksi: X tahun. Log penggunaan: X bulan.

## 8. Hak Anda [⚠️ LEGAL REVIEW REQUIRED]
Akses, penghapusan, koreksi, pembatasan pemrosesan, portabilitas, berhenti dari pemasaran, dan mengajukan keluhan kepada otoritas pelindungan data. Hubungi [CONTACT_EMAIL]; kami merespons dalam [30] hari.

## 9. Cookie & Pelacakan [⚠️ LEGAL REVIEW REQUIRED]
Kami memakai cookie fungsional, analitik (Google Analytics), dan pemasaran (Meta Pixel). Anda dapat mengelola cookie melalui banner atau pengaturan browser.

## 10. Keamanan
Enkripsi saat transit (HTTPS), kontrol akses, audit berkala, prosedur respons insiden. Tidak ada sistem yang 100% aman.

## 11. Privasi Anak [⚠️ LEGAL REVIEW REQUIRED]
Layanan tidak ditujukan untuk anak di bawah 13 tahun (COPPA).

## 12. Kontak
[CONTACT_EMAIL] · [COMPANY_ADDRESS] · DPO: [jika diwajibkan]

## 13. Perubahan Kebijakan
Kami akan memberi tahu perubahan material melalui email atau situs 30 hari sebelumnya.

## 14. Ketentuan Tambahan
Kami tidak menjual data pribadi. Kami tidak bertanggung jawab atas situs pihak ketiga. Hukum yang berlaku: Republik Indonesia.

(English version mirrors the above.)

## Part 3: Customization and Compliance Notes
- Have a data privacy attorney review sections marked ⚠️.
- GDPR/CCPA considerations if you serve EU/California customers.
- Sign DPAs with processors; consider a DPIA for ad tracking.
- Next steps: legal review, cookie banner, request-handling process.
```

Hasil `cek_kebijakan.py` (pemeriksa milik kita — potensi bias, dibaca bersama penilaian manual):
```
PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — output-pesaing-01.md
Skor kelengkapan: 78/100  |  Status: PERLU PERBAIKAN  |  487 kata

UNSUR:
  [v] Identitas pengendali data (nama usaha/pemilik) — ADA
  [v] Kontak yang bisa dihubungi (email/WA/alamat) — ADA
  [v] Jenis data pribadi yang dikumpulkan — ADA
  [ ] Tujuan pemrosesan — TIDAK ADA
  [v] Dasar pemrosesan (persetujuan, perjanjian, kewajiban hukum, dll.) — ADA
  [v] Pihak yang menerima data (kurir, payment gateway, marketplace, cloud, iklan) — ADA
  [v] Transfer/penyimpanan data di luar negeri — ADA
  [v] Masa simpan (retensi) data — ADA
  [~] Hak subjek data (akses, koreksi, hapus, tarik persetujuan) — SEBAGIAN (kurang: akses)
  [v] Cara mengajukan permintaan hak & batas waktu tanggapan — ADA
  [v] Langkah keamanan data — ADA
  [ ] Pemberitahuan bila terjadi kebocoran (kegagalan pelindungan data) — TIDAK ADA
  [v] Tanggal berlaku / terakhir diperbarui — ADA
  [v] Cara memberi tahu perubahan kebijakan — ADA
  [ ] Data anak: persetujuan orang tua/wali — TIDAK ADA

```
Catatan: "Tujuan TIDAK ADA", "hak akses kurang", dan frasa "100% aman" pada output pesaing adalah **salah-deteksi script** (bagian "Penggunaan Informasi" ada; "Tidak ada sistem yang 100% aman" = kalimat jujur). Penilaian di bawah memakai penilaian manual.

## Penilaian berdampingan (1–5)
| Kriteria | Pesaing (pm-skills) | Skill kita | Catatan |
|---|---|---|---|
| Rujukan hukum Indonesia yang benar | 2 | 5 | Pesaing: daftar hukum GDPR/CCPA/HIPAA/COPPA, tanpa pasal UU PDP; menyarankan SCC (mekanisme EU) dan "anak < 13 th (COPPA)" — tidak tepat untuk Indonesia (Ps. 25: anak, persetujuan orang tua/wali) |
| Dasar pemrosesan | 4 | 5 | Keduanya punya; kita per data dalam tabel + masa simpan |
| Masa simpan | 2 | 4 | Pesaing: "X bulan/X tahun"; kita: 10 th UU KUP, 1 th chat (saran) |
| Tenggat hak subjek | 1 | 5 | Pesaing: "30 hari" (**salah** untuk UU PDP, seharusnya 3×24 jam utk akses/perbaikan/tarik persetujuan) |
| Pemberitahuan kebocoran 3×24 jam | 1 | 5 | Pesaing: hanya "prosedur respons insiden" |
| Transfer LN | 3 | 5 | Pesaing menyebut SG + SCC; kita Ps. 56 |
| Bahasa awam & siap tempel untuk UMKM | 3 | 5 | Pesaing banyak penanda ⚠️ di teks publik; perlu disunting |
| Klaim tidak dikarang | 3 | 5 | Pesaing mengklaim "audit berkala, prosedur respons insiden" (dari template, belum tentu dilakukan) |
| Versi EN | 2 | 5 | Pesaing "mirrors the above" |
| Kelebihan pesaing | Ringkasan "Part 1" & catatan DPA/DPIA | — | Layak dipelajari: kita bisa menambah ringkasan 5 baris di atas output dan pengingat perjanjian dengan prosesor (Ps. 51) |
| **Total (maks 45)** | **21** | **44** | |

## Kesimpulan
**Skill kita menang telak** untuk konteks Indonesia. Pesaing bersifat generik GDPR/US dan menghasilkan dua kesalahan substantif untuk UU PDP (tenggat 30 hari, batas anak 13 th/COPPA) serta tidak memuat pemberitahuan kebocoran 3×24 jam. Tidak ditemukan skill/generator publik khusus UU PDP untuk dibandingkan. Pelajaran untuk revisi (ditulis dengan cara kita sendiri): tambahkan ringkasan singkat di awal output dan pengingat perjanjian pengendali–prosesor.
