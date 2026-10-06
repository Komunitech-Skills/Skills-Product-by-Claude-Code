# Contoh 3: admin kantor, 8 email tagihan dan vendor

> Contoh rancangan pembuat dengan email fiktif; bukan hasil uji platform. Hari ini Selasa, 2026-10-06.

## Masukan pengguna
"Saya admin kantor. Ini email tagihan dan vendor minggu ini. Mana yang harus dibayar dulu? Buatkan rekap untuk grup tim tanpa data rahasia."

Email yang ditempel (ringkas):
1. PT Listrik Contoh: tagihan listrik Rp4.200.000, jatuh tempo 12 Okt.
2. CV Kertas Jaya: invoice ATK Rp1.850.000, jatuh tempo 6 Okt (hari ini).
3. Internet Cepat: invoice Rp1.100.000 jatuh tempo 20 Okt.
4. "Bank Mandiri Layanan" dari `layanan@mandiri-cs.top`: "Token Anda kedaluwarsa, klik http://192.0.2.15/token dan isi PIN".
5. Pak Bambang (vendor kebersihan): "Mulai bulan ini mohon bayar ke rekening baru 9876543210 a.n. Bambang S, rekening lama ditutup", dari alamat Gmail.
6. Penyedia Perangkat: penawaran printer diskon, berhenti berlangganan di bawah.
7. Bu Wati (HR): minta rekap lembur September sebelum 10 Okt.
8. Sewa Gedung Contoh: pengingat sewa Rp35.000.000 jatuh tempo 31 Okt.

## Keluaran di chat

**Waspada:** E4 kemungkinan besar phishing (nama pengirim bank, alamat berakhiran `.top`, tautan berupa alamat angka, meminta PIN). Jangan klik dan jangan isi PIN; bank tidak meminta PIN lewat email. E5 patut diverifikasi dulu: perubahan rekening lewat email, dari alamat Gmail, dengan tekanan "rekening lama ditutup". Telepon Pak Bambang ke nomor yang sudah dikenal sebelum membayar ke rekening baru; sampai itu, bayar hanya ke rekening lama yang tercatat bila masih aktif.

**Ringkasan:** 8 email: 2 dicurigai, 3 tagihan perlu dibayar, 1 permintaan rekap, 1 pengingat, 1 promosi.

| Urut. | Email | Prioritas dan alasan | Ringkasan dan tindakan |
|---|---|---|---|
| 1 | E2 CV Kertas Jaya | P1: jatuh tempo hari ini, Rp1.850.000 | Invoice ATK. Bayar atau minta persetujuan hari ini |
| 2 | E1 Listrik | P1: jatuh tempo 12 Okt (6 hari), Rp4.200.000 | Tagihan listrik. Jadwalkan bayar sebelum 12 Okt |
| 3 | E7 Bu Wati | P2: tenggat 10 Okt | Minta rekap lembur September. Kirim sebelum 10 Okt |
| 4 | E3 Internet | P2: jatuh tempo 20 Okt, Rp1.100.000 | Jadwalkan bayar pekan depan |
| 5 | E8 Sewa gedung | P2: Rp35.000.000 jatuh tempo 31 Okt (nominal besar) | Ajukan persetujuan dana minggu ini |

**Draf balasan**

E2
> Subjek: Re: Invoice ATK
> Selamat pagi, terima kasih atas invoicenya. Invoice sebesar Rp1.850.000 kami catat dan pembayaran dijadwalkan [isian: tanggal bayar]. Bukti transfer kami kirim setelahnya.

E7
> Subjek: Re: Rekap lembur September
> Selamat pagi Bu Wati, rekap lembur September kami kirim paling lambat [isian: tanggal, sebelum 10 Oktober]. Mohon info format yang dibutuhkan.

E5 (verifikasi)
> Subjek: Re: Perubahan rekening
> Pak Bambang, terima kasih infonya. Sesuai prosedur kantor, perubahan rekening kami konfirmasi lewat telepon ke nomor yang sudah kami simpan. Kami hubungi Bapak hari ini; pembayaran berikutnya menunggu konfirmasi itu.

**Rekap untuk grup tim (tanpa data rahasia):**
> Rekap email 6 Okt: 5 tagihan/permintaan perlu tindakan (1 jatuh tempo hari ini, 1 sebelum 12 Okt, 1 rekap HR sebelum 10 Okt, 2 pekan depan dan akhir bulan). 2 email dicurigai penipuan, jangan diklik atau dibalas. 1 promosi diarsipkan. Detail nominal ada di admin.

**Arsipkan:** E6 (promosi printer).

**Asumsi:** hari ini 6 Okt 2026; nominal besar mulai Rp10.000.000. Boleh saya tahu: (1) siapa yang menyetujui pembayaran? (2) apakah rekening Pak Bambang pernah berubah sebelumnya? (3) format rekap lembur yang diminta HR?
