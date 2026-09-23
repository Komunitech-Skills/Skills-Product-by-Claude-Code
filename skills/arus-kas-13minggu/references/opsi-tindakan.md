# Bank Opsi Tindakan Saat Kas Menipis

Pilih 3–5 opsi yang **relevan dengan data pengguna** (ada pos yang bisa digeser). Urutkan: dampak terbesar dan paling mudah dijalankan dulu. Setiap opsi harus menyebut pos/pihak, nominal, minggu asal → tujuan, dan angka hasil simulasi script (atau hasil jalankan ulang setelah CSV diubah).

## A. Mempercepat uang masuk
| Opsi | Kapan cocok | Cara konkret / contoh kalimat |
|---|---|---|
| Percepat tagihan piutang | Ada pelunasan piutang setelah minggu bermasalah | "Pak/Bu, apakah pembayaran invoice Rp … bisa dilakukan tanggal … ? Jika dilunasi minggu ini kami beri potongan 1–2%." Tawarkan skill `tagih-piutang` untuk menyusun pesan bertahap. |
| Potongan bayar cepat (early payment discount) | Pelanggan B2B dengan termin 30 hari | Hitung biaya: potongan 2% dari Rp 15.000.000 = Rp 300.000 — bandingkan dengan biaya telat bayar gaji/denda. |
| Minta uang muka (DP) pesanan baru | Usaha pesanan/produksi/jasa | DP 30–50% di depan untuk pesanan besar; masukkan sebagai baris `masuk` baru lalu jalankan ulang. |
| Jual stok lambat laku | Ada persediaan menumpuk | Promo bundling/cuci gudang; masukkan perkiraan hasil sebagai penerimaan (konservatif, mis. 50% dari harga normal). |
| Tagih langsung saat serah terima | Sering kirim dulu baru tagih | Ubah kebijakan: bayar saat barang diterima (COD/transfer sebelum kirim). |

## B. Memundurkan / mengatur uang keluar
| Opsi | Kapan cocok | Cara konkret / contoh kalimat |
|---|---|---|
| Negosiasi termin supplier | Ada pembayaran bahan rutin | "Kami pelanggan rutin sejak …; bisakah pembayaran bulan ini diberi termin 14 hari?" **Ingatkan:** utang tetap ada; lihat nilai `jatuh_setelah_horizon`. |
| Tunda belanja non-kritis | Ada renovasi, alat baru, iklan besar, perjalanan, prive besar | Geser ke minggu setelah saldo pulih (lihat minggu saat saldo kembali di atas batas aman). |
| Pecah pembayaran besar | Sewa tahunan, THR, pembelian alat | Minta dibayar 2–3 kali; buat baris terpisah per termin di CSV. |
| Kurangi pembelian bahan sementara | Stok masih cukup untuk 1–2 minggu | Beli sesuai kebutuhan minggu itu saja (just-in-time) — hati-hati kehabisan stok. |
| Kurangi prive (ambil uang pribadi) | Pemilik rutin mengambil uang usaha | Tetapkan jumlah prive tetap per bulan dan catat sebagai pengeluaran. |

## C. Menambah dana (pilihan terakhir)
| Opsi | Catatan wajib |
|---|---|
| Suntikan modal pemilik/keluarga | Tulis kesepakatan sederhana (tawarkan skill `perjanjian-sederhana`). |
| Pinjaman bank / KUR | Jumlah = `tambahan_dana_agar_di_atas_batas_aman`. Proses butuh waktu (bisa beberapa minggu) sehingga tidak cocok untuk minggu negatif yang sudah dekat. Simulasi cicilan & persiapan dokumen: skill `pengajuan-kur`. |
| Fasilitas supplier (konsinyasi) | Barang dibayar setelah laku. |

**Dilarang disarankan:** pinjol ilegal (tidak terdaftar OJK), gadai barang pelanggan, menunda gaji tanpa persetujuan karyawan, menunda setor pajak (denda/bunga). Cicilan bank dan pajak sebaiknya tetap diperlakukan **kritis**.

## Cara menunjukkan dampak opsi
1. Pakai `simulasi_opsi` dari script untuk opsi A1 (piutang), B1 (supplier), B2 (non-kritis), dan gabungan.
2. Untuk opsi lain (DP, jual stok, pecah pembayaran): ubah CSV (tambah baris masuk / pecah baris keluar), jalankan ulang, lalu laporkan saldo terendah & minggu bermasalah yang baru.
3. Tulis dampak dengan kalimat awam: "Minggu 8 yang tadinya tinggal Rp 0 menjadi Rp 9.000.000."
