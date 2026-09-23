# 00 — Uji banding pesaing (S1)

## Pencarian
- Kata kunci: "invoice chaser", "overdue invoice reminder SKILL.md", "payment reminder", "dunning", "accounts receivable", "tagih piutang".
- Sumber dicek: github.com/VoltAgent/awesome-openclaw-skills (invoice-chaser oleh audsmith28, norman-overdue-reminders, invoice-tracker-pro — halaman ClawHub/clawskills.sh **diblokir proxy**, isi tidak terbaca; norman-* terikat API akuntansi Jerman), github.com/anthropics/skills (tidak ada), manairalabs/bicara-skills & alvinindra/bahasa-skills (tidak ada), pencarian web GitHub.
- Temuan yang terbaca & paling sebanding: **`invoice-chaser`** — github.com/Ootto-AI/claude-invoice-skills (skills/invoice-chaser/SKILL.md), lisensi **MIT**, v1.0.0. Juga ada `payment-plan-drafter` di repo yang sama (tawaran cicilan).
- Script pihak ketiga tidak dijalankan; isi tidak disalin.

## Input S1 (sama)
> Katering Dapur Sehati Fiktif, Surabaya. Tagihan makan siang Agustus ke PT Fiktif Makmur Sejahtera Rp 6.300.000, INV-KT-0825, jatuh tempo 5 September. Sudah WA tanggal 8 dan 15 September tapi cuma dibaca. Bu Dewi bagian GA. Pelanggan lama, tidak ada denda. Rekening BCA 000-000-0000 a.n. Dapur Sehati Fiktif.

## Output dengan instruksi pesaing (`invoice-chaser`, disimulasikan)
Instruksi pesaing: kumpulkan nama, nomor & nominal invoice, jatuh tempo, **hari terlambat**, pengingat sebelumnya, hubungan; nada menurut umur (15–30 hari: sopan tapi lebih jelas, minta tanggal bayar pasti); email < 150 kata, 2 opsi subjek, satu permintaan jelas, akhiri dengan satu pertanyaan.
```
Subjek opsi 1: Invoice INV-KT-0825 – mohon konfirmasi tanggal pembayaran
Subjek opsi 2: Pembayaran makan siang Agustus (Rp 6.300.000)

Halo Bu Dewi,

Semoga baik-baik saja. Kami ingin menindaklanjuti invoice INV-KT-0825 untuk layanan makan siang
Agustus sebesar Rp 6.300.000 yang jatuh tempo pada 5 September (sudah lewat 18 hari). Kami sudah
mengirim pengingat lewat WhatsApp pada 8 dan 15 September.

Pembayaran dapat ditransfer ke BCA 000-000-0000 a.n. Dapur Sehati Fiktif. Jika sudah dibayar,
mohon abaikan pesan ini dan kirimkan bukti transfernya.

Boleh kami tahu tanggal pasti pembayaran bisa dilakukan, paling lambat Selasa, 30 September?

Terima kasih,
[Nama] – Dapur Sehati Fiktif
```
(Hari terlambat dihitung agent sendiri karena pesaing tidak punya kalkulator.)

## Output dengan skill kita
Lihat `01-katering-kantor-lewat-18-hari.md` (ringkasan hitungan script, surat tahap 5 berkop + WA pengantar, jadwal tahap berikutnya, saran tindakan, catatan hukum).

## Penilaian

| Kriteria | Pesaing (`invoice-chaser`) | Skill kita |
|---|---|---|
| Kualitas pesan S1 | Baik, ringkas, satu permintaan jelas — **mendekati** kualitas kita untuk kasus ini | Setara isi, plus format surat resmi & WA pengantar sesuai tahap |
| Konteks Indonesia | Umum (gaya email AS); tidak kenal somasi, meterai, UU ITE/PDP, WA | Tahapan hingga somasi (KUHPerdata), larangan UU ITE/PDP, meterai, gugatan sederhana |
| Akurasi | Hari terlambat & denda tidak dihitung (bergantung input pengguna); tahap 60+ hari menyebut "late fee" tanpa syarat kesepakatan tertulis | Script teruji: hari, sisa, denda hanya bila tertulis, rekap umur piutang CSV |
| Siap pakai | Satu email per permintaan | Pesan + jadwal lanjutan + saran tindakan + CSV prioritas |
| **Total** | Kalah (unggul di keringkasan) | **Menang** |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Dua opsi subjek email** — murah dan berguna untuk tahap 4–5.
2. **Batas panjang eksplisit** (mis. < 150 kata untuk email pengingat) agar pesan tahap 3–4 tidak bertele-tele.
3. **Menutup dengan satu pertanyaan spesifik yang memancing balasan** — sudah ada di tahap 3–4 kita; bisa dijadikan butir checklist.
4. Skill terpisah **penyusun rencana cicilan** (payment plan) — kita punya baris "tawarkan cicilan"; template kesepakatan cicilan ringkas bisa ditambahkan ke `references/template-penagihan.md`.
