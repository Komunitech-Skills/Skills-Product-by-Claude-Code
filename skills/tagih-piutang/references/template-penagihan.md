# Template penagihan per tahap

Placeholder: `[Nama]`, `[Usaha]`, `[No. Invoice]`, `[nominal]` (sisa dari script), `[tanggal JT]`, `[rekening]`. Sapaan B2B "Bapak/Ibu", B2C/pelanggan dekat "Kak"/nama. Angka selalu dari script.

## Tahap 1 — H-3 s.d. H-1 (pengingat halus)
**WA:** "Selamat pagi, [Nama] 🙏 Sekadar mengingatkan, invoice [No. Invoice] senilai [nominal] akan jatuh tempo pada [tanggal JT]. Pembayaran dapat ditransfer ke [rekening]. Terima kasih atas kerja samanya. (Abaikan pesan ini jika sudah dibayar.)"
**Email subjek:** `Pengingat: Invoice [No. Invoice] jatuh tempo [tanggal JT]`

## Tahap 2 — Hari H
**WA:** "Selamat siang, [Nama]. Hari ini, [tanggal JT], merupakan jatuh tempo invoice [No. Invoice] sebesar [nominal]. Jika sudah ditransfer, mohon kirimkan bukti transfernya agar bisa langsung kami catat. Terima kasih 🙏"

## Tahap 3 — Lewat 1–6 hari (asumsi baik)
**WA:** "Selamat pagi, [Nama]. Kami belum menerima pembayaran invoice [No. Invoice] sebesar [nominal] yang jatuh tempo [tanggal JT]. Mungkin terlewat ya, [Pak/Bu]. Jika sudah dibayar, mohon kirim bukti transfer; jika belum, boleh kami tahu perkiraan tanggal pembayarannya?"

## Tahap 4 — Lewat 7–13 hari (tegas-sopan, minta tanggal pasti)
**WA:** "Selamat siang, [Nama]. Invoice [No. Invoice] sebesar [nominal] telah melewati jatuh tempo [N] hari (jatuh tempo [tanggal JT]). Mohon konfirmasi tanggal pembayaran paling lambat [tanggal +2 hari kerja]. Jika ada kendala, kami terbuka membicarakan jadwal pembayaran. Terima kasih."
**Email subjek:** `Tagihan lewat jatuh tempo: Invoice [No. Invoice]`

## Tahap 5 — Lewat 14–29 hari (pemberitahuan resmi)
Kirim sebagai email/PDF berkop + ringkasan di WA.
```
Perihal: Pemberitahuan Tagihan Lewat Jatuh Tempo – Invoice [No. Invoice]

Dengan hormat,
Bersama ini kami sampaikan bahwa Invoice [No. Invoice] tertanggal [tgl invoice] senilai [nominal awal] telah jatuh tempo pada [tanggal JT] dan hingga [tanggal hitung] masih terdapat sisa [nominal] ([N] hari keterlambatan). Kami telah mengirimkan pengingat pada [tanggal-tanggal].
[Jika ada dasar tertulis:] Sesuai [dasar denda], keterlambatan dikenai denda sebesar [denda] per [tanggal hitung].
Kami mohon pembayaran dapat diselesaikan paling lambat [tanggal +7 hari] ke [rekening]. Apabila diperlukan, kami bersedia membahas jadwal pembayaran bertahap yang dituangkan secara tertulis.
Atas perhatian dan kerja samanya, kami ucapkan terima kasih.
```
**WA pengantar:** "[Nama], kami kirimkan surat pemberitahuan resmi terkait invoice [No. Invoice] ke email [email]. Mohon konfirmasinya ya, [Pak/Bu]. Terima kasih."

## Tahap 6 — Lewat ≥ 30 hari: Surat Teguran (Somasi)
```
[KOP USAHA]
Nomor   : [..]/SP/[bulan romawi]/[tahun]
Lampiran: Salinan invoice & bukti pengiriman
Perihal : Surat Teguran [Pertama/Kedua] – Pembayaran Invoice [No. Invoice]

[Kota], [tanggal]

Kepada Yth.
[Nama/Jabatan]
[Perusahaan]
[Alamat]

Dengan hormat,
1. Kronologi: [PO/perjanjian tanggal ..], [barang/jasa diserahkan tanggal ..], Invoice [No.] senilai [..] jatuh tempo [..].
2. Pengingat telah disampaikan pada [tanggal-tanggal] melalui [WA/email].
3. Pembayaran yang telah diterima: [..]. Sisa kewajiban: [nominal].
4. [Jika ada dasar tertulis] Denda keterlambatan sesuai [dasar]: [denda]. Total: [total].

Dengan surat ini kami meminta Bapak/Ibu menyelesaikan kewajiban tersebut paling lambat [tanggal +7 hari] ke rekening [rekening], atau menghubungi kami sebelum tanggal tersebut untuk menyepakati jadwal pembayaran secara tertulis.

Apabila hingga batas waktu tersebut tidak ada pembayaran maupun tanggapan, dengan menyesal kami akan menempuh langkah penyelesaian sesuai peraturan perundang-undangan yang berlaku.

Demikian surat teguran ini kami sampaikan. Atas perhatiannya kami ucapkan terima kasih.

Hormat kami,
[Nama]
[Jabatan] – [Usaha]
```
Kirim lewat email + surat tercatat/kurir dengan tanda terima; simpan bukti. Teguran kedua (jika perlu) 7–14 hari kemudian dengan tenggat lebih pendek.

## Balasan saat debitur merespons
| Debitur bilang | Balasan inti |
|---|---|
| "Minggu depan ya" | "Baik, [Pak/Bu], kami catat pembayaran pada [tanggal pasti]. Mohon kirim bukti transfer setelahnya. Terima kasih." (Minta tanggal, bukan "minggu depan".) |
| "Belum ada dana, bisa dicicil?" | Tawarkan jadwal tertulis: jumlah per termin + tanggal, dituangkan dalam surat kesepakatan cicilan bermeterai Rp10.000 (berapa pun nilainya). Kuitansi tiap pembayaran > Rp5 juta juga bermeterai. |
| "Barangnya ada yang cacat" | Hentikan eskalasi, minta detail/bukti, lakukan rekonsiliasi dulu. |
| "Sudah transfer" | Minta bukti, cek mutasi, lalu kirim konfirmasi terima kasih. |
| Tidak ada respons | Lanjut tahap berikutnya sesuai jadwal. |

## Ucapan terima kasih setelah lunas
"Terima kasih, [Nama], pembayaran invoice [No. Invoice] sebesar [nominal] sudah kami terima pada [tanggal]. Senang bekerja sama dengan [Perusahaan] 🙏"

## Contoh kasus lokal
1. **Katering langganan kantor (Surabaya)**: tagihan bulanan Rp 6.300.000 jatuh tempo tanggal 5, pelanggan lama → tahap 1–3 dengan nada akrab, tanpa denda (tidak ada kesepakatan).
2. **Toko bahan kue ke reseller (Medan)**: 3 reseller menunggak, rekap umur piutang dari CSV → prioritaskan yang terlama & terbesar.
3. **Jasa desain untuk UMKM (Bandung)**: termin 2 Rp 4.500.000 lewat 20 hari → tahap 5 dengan tawaran cicilan 2× tertulis.
