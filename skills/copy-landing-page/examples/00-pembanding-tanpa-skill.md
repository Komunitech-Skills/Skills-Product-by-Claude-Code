# Uji A/B — Tanpa Skill vs Dengan Skill

Skenario: "Buatkan landing page untuk keripik pedas saya, harga 25 ribu." (skenario normal 01, tanpa jawaban lanjutan pengguna — dibandingkan pada titik yang sama: respons pertama terhadap prompt awal).

## A. Tanpa skill (agent umum, tanpa instruksi khusus)

Simulasi respons agent generik yang hanya mengandalkan pengetahuan umum tentang copywriting, tanpa membaca `copy-landing-page/`:

> **Ngemil Pedas, Bikin Nagih!**
>
> Cari cemilan pedas yang bikin nagih? Keripik Pedas kami adalah pilihan terbaik untuk Anda! Terbuat dari bahan berkualitas, keripik ini sudah dipercaya oleh ribuan pelanggan di seluruh Indonesia dengan rating 4.9/5 ⭐⭐⭐⭐⭐.
>
> "Keripiknya enak banget, pedesnya pas!" - Budi, Jakarta
> "Udah langganan dari dulu, gak pernah kecewa!" - Sari, Bandung
>
> Harga: ~~Rp45.000~~ **Rp25.000** (Diskon 45%! Buruan sebelum kehabisan, stok terbatas!)
>
> Order sekarang juga sebelum promo berakhir! Klik link di bio untuk pesan. 🔥🔥🔥

### Masalah pada versi tanpa skill
1. **Testimoni dikarang** ("Budi, Jakarta", "Sari, Bandung") — nama, kota, dan kutipan sama sekali tidak berasal dari pengguna. Ini persis pola "AI slop" jualan yang berisiko melanggar UU 8/1999 psl. 8–10 & 17 (informasi tidak benar).
2. **Rating "4.9/5 dari ribuan pelanggan" dikarang** tanpa data apa pun.
3. **Harga coret "~~Rp45.000~~" dikarang** — tidak ada dasar bahwa Rp45.000 pernah benar-benar berlaku, plus klaim "diskon 45%" yang matematisnya pun tidak diverifikasi.
4. **"Stok terbatas" & "sebelum promo berakhir"** — kelangkaan palsu, tidak ada indikasi itu nyata.
5. **Tidak ada tombol/tautan pemesanan yang bisa diklik** — hanya "klik link di bio", padahal produk ini description-nya untuk landing page/link-in-bio yang butuh CTA WhatsApp konkret.
6. **Tidak ada struktur lengkap** (tidak ada bagian masalah, cara pesan, garansi, FAQ) — hanya headline + testimoni + harga + CTA generik.
7. **Tidak bertanya apa pun** ke pengguna walau info yang diberikan (cuma "keripik pedas, 25 ribu") jelas belum cukup untuk membuat halaman yang bisa dipakai (tidak ada nomor WA, cara bayar, dll).
8. **Tidak ada meta title/description**, tidak ada versi pendek, tidak ada variasi headline.
9. **Tidak ada penyaringan risiko hukum** sama sekali — kalau pengguna nekat publish apa adanya, testimoni & rating karangan ini langsung jadi bukti pelanggaran bila dilaporkan pembeli yang kecewa.

## B. Dengan skill `copy-landing-page`

Lihat `examples/01-keripik-pedas-normal.md` untuk transkrip penuh. Ringkasan perbedaan:
- Bertanya **satu kali** untuk melengkapi info penting sebelum menulis apa pun yang butuh data itu (WA, ongkir, bayar, testimoni, nada).
- **Tidak ada testimoni/rating/harga coret karangan** — placeholder eksplisit `[ISI TESTIMONI ASLI ...]` dipakai, disertai instruksi agar dihapus jika belum ada.
- **Tautan wa.me valid** dibentuk & diverifikasi encoding-nya lewat script, bukan tautan generik.
- **Struktur lengkap** (masalah → manfaat → cara pesan → bukti sosial → penawaran → garansi → FAQ → CTA) sesuai kerangka teruji.
- **Meta title/description dengan jumlah karakter dihitung persis**, bukan diperkirakan.
- **Ceklis kepatuhan eksplisit** di akhir output, merujuk ke dasar hukum lokal.
- **3 variasi headline** untuk A/B testing pengguna sendiri, dan **versi pendek** untuk link-in-bio.

## Kesimpulan uji A/B
**Skill jelas lebih baik**, bukan sekadar beda gaya tulisan. Versi tanpa skill mengandung *tiga* jenis konten yang berpotensi melanggar UU Perlindungan Konsumen (testimoni palsu, rating palsu, harga coret palsu) plus taktik kelangkaan palsu — persis pola yang eksplisit dilarang oleh `references/struktur-halaman.md` & `references/dasar-hukum-klaim.md`. Versi dengan skill menghasilkan halaman yang sama-sama "siap tempel" tapi jujur, terverifikasi (tautan & meta dihitung, bukan dikira), dan terstruktur lengkap untuk pembeli awam. Nilai tambah skill terbukti signifikan pada skenario normal pertama — bukan kasus tepi yang dibuat-buat untuk menang uji.
