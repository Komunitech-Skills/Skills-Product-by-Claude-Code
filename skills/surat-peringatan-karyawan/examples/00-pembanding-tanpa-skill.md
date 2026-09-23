# Pembanding A/B – Permintaan S1 dengan dan tanpa skill

**Permintaan yang sama (S1):**
```
Tolong buatkan SP lanjutan untuk Bayu Pratama, staf packing di online shop skincare saya (Glowria Skin, Tangerang). Dia masih kena SP1 nomor 004/SP-1/GS/VII/2026 tanggal 14 Juli 2026 karena salah kirim juga. Sekarang salah kirim lagi 5 paket: tanggal 8, 10, 11, 15, dan 17 September, semuanya ada komplain pembeli dan video packing. Kemarin (21 Sept) sudah saya panggil, katanya kurang fokus karena sering begadang. Di peraturan perusahaan kami Pasal 12 soal kewajiban mengikuti SOP packing. Saya pemiliknya, Rudi Hartono.
```

## A. Tanpa skill (AI agent biasa, tanpa membaca skill apa pun)

> **SURAT PERINGATAN KEDUA (SP-2)**
> No: 005/SP-2/GS/IX/2026
>
> Kepada Yth.
> Sdr. Bayu Pratama
> Staf Packing Glowria Skin
>
> Dengan hormat,
>
> Sehubungan dengan kelalaian yang Saudara lakukan berupa kesalahan pengiriman barang sebanyak 5 (lima) paket pada tanggal 8, 10, 11, 15, dan 17 September 2026, di mana sebelumnya Saudara telah menerima Surat Peringatan Pertama (SP-1) Nomor 004/SP-1/GS/VII/2026 tanggal 14 Juli 2026 atas pelanggaran yang sama, maka dengan ini manajemen memberikan **Surat Peringatan Kedua (SP-2)**.
>
> Tindakan tersebut melanggar Pasal 12 Peraturan Perusahaan tentang kewajiban mengikuti SOP packing, dan telah merugikan perusahaan baik secara materi maupun nama baik toko.
>
> Kami harap Saudara dapat lebih fokus dan bertanggung jawab dalam bekerja. Apabila Saudara kembali melakukan kesalahan, maka perusahaan akan memberikan SP-3 dan **dapat melakukan Pemutusan Hubungan Kerja (PHK)** sesuai peraturan yang berlaku.
>
> Surat peringatan ini berlaku selama 6 (enam) bulan sejak tanggal diterbitkan.
>
> Demikian surat peringatan ini kami sampaikan untuk diperhatikan.
>
> Tangerang, 23 September 2026
>
> Hormat kami,
>
> Rudi Hartono
> Pemilik Glowria Skin
>
> Karyawan yang bersangkutan,
>
> Bayu Pratama

## B. Dengan skill `surat-peringatan-karyawan`
Output lengkap ada di `01-sp2-staf-packing-salah-kirim.md`. Ringkasnya:
- Alasan pemilihan SP2 dijelaskan. Status SP1 dicek dengan script ("MASIH AKTIF" pada 8 dan 17 September; berlaku s.d. 13 Januari 2027).
- Masa berlaku ditulis dengan tanggal pasti: 23 September 2026 s.d. 22 Maret 2027.
- Bagian A–D lengkap: fakta + bukti + rujukan SP1, dasar pasal, harapan perbaikan terukur (0 salah kirim, video 100%), dan tawaran pelatihan ulang.
- Tersedia kolom tanggal terima, saksi, lampiran, dan tembusan.
- Draf Berita Acara Klarifikasi dari pertemuan 21 September.
- Catatan proses (cara menyerahkan, jika karyawan menolak tanda tangan, soal begadang/lembur, larangan potong gaji) dan disclaimer bertanggal.

## Penilaian singkat
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Masa berlaku | "6 bulan sejak diterbitkan", tanpa tanggal berakhir. Rawan sengketa. | Tanggal pasti dari script: s.d. 22 Maret 2027. |
| Cek SP1 masih aktif | Tidak dicek, hanya diasumsikan. | Dicek dengan script, dan alasannya ditulis. |
| Ancaman PHK | Ada ("dapat melakukan PHK"), bertentangan dengan pola bertahap dan berisiko. | Konsekuensi bertahap (SP3), tanpa ancaman PHK. |
| Bukti & klarifikasi | Bukti tidak disebut, pertemuan 21 September tidak dicatat. | Bukti disebut, ada BA klarifikasi dan lampiran. |
| Harapan perbaikan | Umum ("lebih fokus"). | Terukur, disertai pembinaan. |
| Tanda tangan | Tanpa saksi dan tanpa tanggal terima. | Lengkap, dengan langkah bila karyawan menolak. |
| Panduan proses & disclaimer | Tidak ada. | Ada, termasuk dasar PP 35/2021 dan peringatan RUU baru. |
| Nomor surat | Nomor urut "005" dikarang. | Placeholder `[nomor urut]`. |

**Kesimpulan: hasil dengan skill jelas lebih baik.** Surat tanpa skill terlihat rapi, tapi punya kelemahan hukum dan praktis yang nyata: tidak ada tanggal berakhir, ada ancaman PHK, tidak ada saksi atau tanggal terima, dan status SP1 tidak dicek. Skill mengubahnya menjadi dokumen yang terukur dan lebih kuat bila dipersoalkan.
