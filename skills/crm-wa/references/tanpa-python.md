# Jika Python tidak bisa dijalankan (mode manual)

Skill tetap bisa dipakai sebagai **buku CRM di spreadsheet**. Beri tahu pengguna: "Mode manual: angka dihitung
manual, mohon dicek." Jangan membuat/mengubah file `crm.db` secara manual.

## 1. Tabel kontak (Excel/Google Sheets atau CSV)
Pakai kolom yang sama dengan `templates/kontak-contoh.csv` agar kelak bisa diimpor (`crm.py impor`) begitu Python siap:
`nama;no wa;sumber;tahap;nilai;kebutuhan;label;catatan;follow up;tgl masuk;alasan batal`
- Nomor WA: tulis `62` + nomor tanpa 0 di depan (0812-0000-1234 → `6281200001234`). Format kolom sebagai **Teks**
  agar Excel tidak mengubahnya menjadi `6,28E+12`.
- Tahap: `baru`, `dihubungi`, `ditawar`, `deal`, `selesai`, `batal` (batal wajib diisi alasannya).
- Tanggal: `YYYY-MM-DD`. Nilai: angka bulat tanpa titik (4500000).
- Jangan menaruh nomor di kolom nama. Jangan membagikan file ini ke grup (data pribadi).

## 2. Daftar follow-up hari ini
Urutkan kolom `follow up` dari yang paling lama. Kontak non-batal dengan tanggal < hari ini = **terlambat**;
= hari ini = **hari ini**. Kontak baru/dihubungi/ditawar tanpa tanggal = **belum dijadwalkan**.

## 3. Draf & tautan
Susun draf mengikuti pola di `references/perintah.md` (bagian "Irama follow-up & jenis draf"): sapaan awal →
menyambung obrolan → pilihan mudah (balas 1/2/3) → pesan pamit; deal → konfirmasi order; selesai → terima kasih.
Jangan menulis harga kecuali pemilik menyebutkannya. Tautan: `https://wa.me/62812xxxxxxx?text=` + teks yang
di-*URL-encode* (spasi `%20`, koma `%2C`, tanda tanya `%3F`, baris baru `%0A`). Jika ragu, berikan draf saja dan
minta pemilik menyalin-tempel ke WhatsApp.

## 4. Rekap manual
- Lead masuk periode = jumlah baris dengan `tgl masuk` di periode.
- Konversi = (lead periode yang tahapnya deal/selesai) ÷ (lead masuk periode) × 100%, 1 desimal.
- Win rate = deal/selesai ÷ (deal/selesai + batal) dari lead periode.
- Nilai deal = jumlah kolom nilai untuk kontak deal/selesai yang deal-nya terjadi di periode.
- Sumber terbaik = sumber dengan nilai deal terbesar (seri → konversi lebih tinggi). Kurang dari 5 lead = sampel kecil.
Tuliskan rumusnya di bawah hasil supaya pemilik bisa memeriksa.
