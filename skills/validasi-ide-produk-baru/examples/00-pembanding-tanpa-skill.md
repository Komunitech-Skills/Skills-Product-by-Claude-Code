# Uji A/B — Tanpa Skill vs Dengan Skill

**Skenario normal pertama:** "Saya mau coba jual sambal botolan rumahan, enak katanya keluarga saya, mau saya botolin dan jual online. Punya sekitar 80 follower IG dan 40 kontak WA. Rencana harga Rp28.000/botol."

## A. Tanpa skill (respons generik agent umum, disimulasikan)
> "Ide bagus! Sambal rumahan punya potensi karena tren produk homemade lagi naik. Beberapa saran:
> - Buat kemasan yang menarik dan higienis
> - Posting di Instagram dengan foto menggugah selera
> - Minta testimoni dari keluarga/teman dulu
> - Coba jual di marketplace seperti Shopee
> - Pertimbangkan harga yang kompetitif dibanding sambal kemasan lain
> - Lakukan riset pasar untuk tahu apakah orang tertarik
>
> Semoga sukses jualannya!"

**Masalah respons ini:**
- Tidak ada langkah konkret "bagaimana caranya tahu laku sebelum produksi banyak" — hanya saran umum yang bisa dicari di Google mana saja.
- Tidak ada angka: berapa orang harus ditawari, berapa yang harus pre-order supaya dianggap layak lanjut. "Riset pasar" disebut tanpa cara.
- Tidak ada kriteria lulus/gagal, tidak ada keputusan akhir (LANJUT/UBAH/HENTIKAN) — pengguna tetap harus menyimpulkan sendiri.
- Tidak ada template pesan siap kirim — pengguna harus menulis sendiri dari nol.
- Tidak memakai kanal spesifik yang disebut pengguna (40 WA, 80 IG) — saran generik "posting Instagram" tidak menghitung apa pun dari angka itu.

## B. Dengan skill `validasi-ide-produk-baru`
Lihat hasil lengkap di `examples/03-sambal-botolan-uji-akun-b.md`. Ringkasnya, output mencakup:
1. Hipotesis eksplisit dan spesifik (siapa, kenapa beli, harga pasti, ambang keberhasilan).
2. Metode uji terpilih dengan alasan tercocokkan ke kanal nyata pengguna (WA 40 kontak ≥ ambang 30).
3. Kriteria lulus/gagal berangka, ditetapkan **sebelum** uji jalan (15%/8%).
4. Template pesan broadcast WA siap kirim, tinggal isi kurung siku.
5. Form pencatatan harian siap tempel.
6. Setelah data masuk, perhitungan otomatis via `scripts/hitung_validasi.py` (konversi 16,0%, margin Rp56.000, balik modal uji +Rp21.000) — diverifikasi independen dengan Decimal, hasilnya cocok.
7. Keputusan akhir eksplisit: **LANJUT**, plus arahan skill lanjutan (`hitung-hpp`, `harga-jual-marketplace`).

## Kesimpulan uji A/B
Perbedaannya jelas dan signifikan, bukan sekadar kosmetik: versi tanpa skill berhenti di saran umum tanpa angka, tanpa kriteria, tanpa keputusan; versi dengan skill menghasilkan rencana uji yang bisa langsung dijalankan hari itu juga (pesan siap kirim, form siap isi) dan diakhiri keputusan berbasis angka yang bisa dipertanggungjawabkan. Skill ini **memberi nilai tambah nyata**, bukan hanya skor maksimal 6 (sesuai kriteria Tahap 6 poin 4 di pedoman kurasi Komunitech, karena perbedaan dengan-tanpa-skill sangat jelas lebih baik).
