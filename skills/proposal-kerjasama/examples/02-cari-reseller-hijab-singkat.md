# 02 — Permintaan singkat: proposal cari reseller

**Skenario:** S2 — permintaan singkat/malas; nama brand tidak disebut → default + placeholder + asumsi.

**Input pengguna:**
> bikinin dong proposal buat nyari reseller hijab, HET 150rb, reseller diskon 20%

**Perintah script:**
```bash
python3 scripts/hitung_skema.py reseller --het 150000 --diskon-reseller 20% --skenario "20;50;100" --format teks
```
Hasil: harga reseller Rp 120.000, untung Rp 30.000/pcs (20%); 20/50/100 pcs → untung Rp 600.000 / Rp 1.500.000 / Rp 3.000.000.

## Output

# Proposal Kemitraan Reseller – [Nama Brand Hijab]

**Ringkasan:** [Nama Brand Hijab] membuka kesempatan menjadi reseller dengan keuntungan **Rp 30.000 per pcs**. Anda membeli di harga reseller Rp 120.000 dan menjual di harga eceran Rp 150.000 — kami bantu dengan [isi: dukungan yang benar-benar Anda sediakan, mis. foto & konten siap posting].

**Peluang:** Hijab adalah kebutuhan harian yang dibeli berulang. Reseller bisa berjualan dari rumah lewat WhatsApp, Instagram, atau marketplace tanpa perlu produksi sendiri.

**Yang kami tawarkan:**
- Harga reseller Rp 120.000/pcs (diskon 20% dari HET Rp 150.000).
- [isi: dukungan yang Anda sediakan, mis. foto katalog & caption siap pakai, grup WA reseller untuk info stok dan produk baru — tulis hanya yang benar-benar ada].
- Retur untuk cacat produksi [isi batas hari].

**Skema kerja sama:**
- Minimal order: [isi] pcs per transaksi (boleh campur warna/motif).
- Harga jual ke konsumen wajib sesuai HET Rp 150.000 agar harga pasar terjaga; aturan jual di marketplace: [isi].
- Order & pembayaran via [WA/transfer], barang dikirim [isi] hari kerja setelah pembayaran.

*Simulasi potensi keuntungan reseller per bulan (perkiraan, belum dikurangi ongkir/biaya jualan):*

| Terjual per bulan | 20 pcs | 50 pcs | 100 pcs |
|---|---|---|---|
| Modal belanja | Rp 2.400.000 | Rp 6.000.000 | Rp 12.000.000 |
| Potensi untung | Rp 600.000 | Rp 1.500.000 | Rp 3.000.000 |

**Manfaat untuk reseller:**
- Untung jelas Rp 30.000 per pcs.
- Tidak perlu produksi sendiri; [isi: konten jualan/desain disediakan, bila ada].
- Harga seragam (HET) sehingga tidak perang harga antar-reseller.

**Langkah berikutnya:** Daftar lewat WA [nomor], lakukan order pertama minimal [isi] pcs, [isi: dan bergabung di grup reseller — hanya bila grupnya ada].

Kontak: [Nama] – [Jabatan] – WA 0812-0000-xxxx – [email/IG]

---

**Pesan pengantar WA (untuk calon reseller):**
```
Halo Kak [Nama] 🙏
Saya [nama] dari [Nama Brand Hijab]. Kami sedang membuka reseller dengan untung Rp 30.000 per pcs (harga reseller Rp 120.000, jual Rp 150.000), plus [isi: dukungan, mis. foto & konten jualan siap pakai].
Proposal singkatnya saya lampirkan ya. Kalau tertarik, boleh saya jelaskan lebih lanjut?
Terima kasih, Kak.
```

**Email** — Subjek: *Kesempatan Reseller [Nama Brand Hijab] – Untung Rp 30.000/pcs*. Isi: sapaan, perkenalan brand 1 kalimat, ringkasan untung & dukungan, proposal terlampir, ajakan daftar via WA, tanda tangan + kontak.

**Asumsi yang dipakai:** nama brand, minimal order, aturan marketplace, kontak, dan dukungan reseller (foto/konten, grup WA) belum diberikan → `[isi]`; simulasi 20/50/100 pcs per bulan; satu tingkat (reseller) saja — jika ingin ada tingkat agen/distributor dengan diskon lebih besar, sebutkan diskon & minimal ordernya.

## Catatan penguji
- Angka benar (150.000 × 80% = 120.000; untung 30.000 × 20/50/100).
- Bagus: tidak bertanya panjang untuk permintaan singkat; placeholder jelas; tetap menyebut HET & aturan marketplace (sesuai kerangka reseller).
- Kurang (ringan): istilah "HET" formalnya dipakai untuk barang yang harganya diatur pemerintah; untuk brand swasta lebih tepat "harga jual yang disarankan (SRP)". Skill memakai "HET" tanpa penjelasan.
