# Pembanding A/B – Permintaan S1 dengan dan tanpa skill

**Permintaan yang sama (S1):** catatan rapat mingguan Rumah Rajut Nadia (lihat `01-weekly-olshop-catatan-kasar.md` untuk teks lengkap). Isinya: omzet 38 juta dari target 50 juta; usulan diskon 10.10 (15% vs "kayaknya 10%, nanti diitung dulu"); "deal" tabel ukuran, Bima update listing "paling lambat jumat depan"; rak gudang "nadia oke, budget max 2jt", Yoga kasih penawaran "kamis"; Tari buat template chat "besok"; ads "nanti ada yg cek"; rapat berikutnya "selasa depan jam 10".

## A. Tanpa skill (AI agent biasa, tanpa membaca skill apa pun)

> **Notulen Rapat Mingguan – Rumah Rajut Nadia**
> **Tanggal:** Selasa, 22 September 2026, 10.00–11.00 (Google Meet)
> **Peserta:** Nadia, Bima, Tari, Yoga (Rini cuti)
>
> **1. Evaluasi September**
> Omzet hingga 20 September mencapai Rp38 juta dari target Rp50 juta. Iklan Shopee dinilai kurang efisien (ROAS 3).
>
> **2. Promo 10.10**
> Diputuskan diskon sebesar 10% untuk menjaga margin (usulan awal 15%).
>
> **3. Retur**
> Terdapat 12 retur, mayoritas karena salah ukuran. Akan ditambahkan tabel ukuran di semua listing oleh Bima paling lambat Jumat depan.
>
> **4. Gudang**
> Pengadaan rak tambahan disetujui dengan budget maksimal Rp2 juta. Yoga akan mencari vendor dan memberikan penawaran pada hari Kamis.
>
> **5. Customer Service**
> Tari akan membuat template balasan chat untuk pertanyaan ukuran besok.
>
> **6. Iklan**
> Setting iklan akan dicek ulang.
>
> **Action Items:**
> - Bima: update tabel ukuran di listing – Jumat depan
> - Yoga: penawaran vendor rak – Kamis
> - Tari: template balasan chat – besok
> - Tim: cek setting ads
>
> **Rapat berikutnya:** Selasa depan, pukul 10.00.

## B. Dengan skill `notulen-rapat`
Output lengkap ada di `01-weekly-olshop-catatan-kasar.md`. Ringkasnya:
- Diskon 10.10 ditulis sebagai **belum diputuskan** (usulan 15% vs 10%, menunggu hitungan margin), bukan keputusan.
- Tanggal relatif dikonversi dengan script: besok = Rabu 23/9, kamis = Kamis 24/9, selasa depan = Selasa 29/9. "Jumat depan" berstatus ambigu (2/10 atau 25/9) dan masuk "Perlu dikonfirmasi".
- Tabel action item dengan PIC dan tenggat, diurutkan. Tugas tanpa pelaksana diberi `⚠️ belum ditentukan`.
- Bagian "Perlu dikonfirmasi" (4 butir) dan pesan WA siap kirim (80 kata).

## Penilaian singkat
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Keputusan palsu | **"Diputuskan diskon 10%"**, padahal catatan berkata "kayaknya 10% aja... nanti diitung dulu". Tim bisa memasang promo yang belum disetujui. | Ditulis sebagai usulan yang belum diputuskan, dengan ⚠️. |
| Tanggal | "Jumat depan", "Kamis", "besok" dibiarkan relatif. Seminggu kemudian tidak jelas maksudnya. | Tanggal nyata + nama hari dari script. Tanggal ambigu ditandai. |
| Tugas tanpa pelaksana | "Tim: cek setting ads". Tanggung jawabnya kabur. | `PIC: ⚠️ belum ditentukan` + masuk daftar konfirmasi. |
| Hal yang perlu dikonfirmasi | Tidak ada. | 4 butir yang konkret. |
| Pesan WA | Tidak ada. | Ada, siap kirim. |
| Struktur | Rapi tapi naratif, tanpa tabel tugas. | Format baku: info rapat, agenda, pembahasan, keputusan, tabel action item. |

**Kesimpulan: hasil dengan skill jelas lebih baik.** Kesalahan paling berbahaya dari agent biasa, yaitu menulis usulan sebagai keputusan ("diputuskan diskon 10%"), dicegah oleh aturan klasifikasi skill. Konversi tanggal dan tanda ⚠️ membuat tugas bisa langsung dieksekusi dan ditagih.
