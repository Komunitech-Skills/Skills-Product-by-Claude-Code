# Uji 04 (penguji independen, Akun B) - Input tidak lengkap

> Uji simulasi agent, 2026-09-26. Skenario: **input tidak lengkap**.

## Permintaan pengguna
"iklanku boncos, cek dong"

## Perilaku yang diharapkan (dari SKILL.md)
- Platform = wajib → tanya. Bukti = wajib → ajukan pertanyaan dari `references/bukti-per-platform.md`.
- Tanya **sekali**, satu pesan, maks. 8 pertanyaan. Jangan menilai sebelum ada bukti; jangan
  mengarang `lulus`.
- Ambiguitas dengan `laporan-iklan-mingguan`: "boncos" bisa berarti minta angka mingguan. Deskripsi
  kedua skill saling merujuk, jadi agent bisa menawarkan keduanya.

## Jawaban agent (simulasi)
> Siap, saya bantu cek. Supaya tidak menebak, jawab singkat saja (boleh "tidak tahu"):
> 1. Iklannya di mana: Meta (FB/IG), TikTok, Google, Shopee, atau TikTok Shop/Tokopedia?
> 2. Iklan diarahkan ke mana: WhatsApp, website, atau produk marketplace?
> 3. Tujuan kampanye yang dipilih (Penjualan / Pesan / Traffic / Boost)?
> 4. Harga jual, modal, dan potongan marketplace produk utama? (untuk hitung batas untung)
> 5. Rata-rata biaya per pesanan/chat bulan lalu?
> 6. Siapa saja yang punya akses akun iklan? Verifikasi 2 langkah aktif?
> 7. Ada iklan ditolak/akun dibatasi 30 hari terakhir?
> 8. (Marketplace) Anggaran harian biasanya habis jam berapa?
>
> Kalau ada, kirim screenshot daftar kampanye (kolom Tujuan, Hasil, Biaya per hasil). Jangan kirim
> password/OTP. Kalau yang Anda butuhkan rekap angka minggu ini, kirim file ekspor CSV — saya buatkan
> laporan mingguannya.

## Uji script dengan bukti minim
Jika pengguna hanya menjawab 7 cek Meta (format Indonesia: pemisah `;`, BOM, "Ya/Tidak/Sudah/N/A"),
script: `Skor gabungan: BELUM BISA DIBERIKAN - bukti kurang dari 60%`, 3 cek kritis masuk "CEK DULU"
(M01, M02, M15), status "mungkin" → `tidak_tahu` dengan peringatan. Perilaku benar.

## Catatan penguji
- ✅ Satu pesan, 8 pertanyaan, tidak mengarang skor.
- ⚠️ Baris per platform tetap mencetak label: `Meta Ads: 79,5/100 (Cukup, ada yang perlu dibenahi);
  bukti 25,0% (BUKTI KURANG - jangan dijadikan nilai akun)`. Label kualitas pada skor bukti kurang
  mudah tersalin ke jawaban dan bertentangan dengan aturan "tidak boleh disebut nilai akun"
  (claude-ads juga melarang). Sebaiknya script tidak mencetak skor/label untuk status bukti kurang.

## Penyegaran v1.0.7 (2026-10-17)
> Jawaban asli di atas (8 pertanyaan, v1.0.0) dan catatan penguji **tidak diubah**. Sejak v1.0.7 batas pertanyaan **maks. 5**. Pesan "iklanku boncos, cek dong" tidak berisi satu pun angka atau bukti, jadi bertanya lebih dulu masih diperbolehkan (SKILL.md bagian Input), tetapi dengan batas yang sama. Label skor pada bukti kurang yang dikritik penguji sudah tidak dicetak skrip (kini "BUKTI BELUM CUKUP ... skor & label tidak diberikan"; dicek ulang dengan skrip v1.0.7 pada 2026-10-17).

Balasan (format v1.0.7):
```
Siap, saya bantu cek. Supaya bisa langsung saya hitung, jawab singkat saja (boleh "tidak tahu"):
1. Iklannya di mana dan diarahkan ke mana? (mis. TikTok/Meta/Google/Shopee; ke WhatsApp, website, atau produk marketplace)
2. Harga jual, modal, dan potongan marketplace produk utama? (untuk menghitung batas untung)
3. Belanja iklan sebulan dan ROAS/biaya per pesanan rata-rata 7–14 hari terakhir?
4. Siapa saja yang punya akses akun iklan, dan verifikasi 2 langkah sudah aktif?
5. Ada iklan ditolak atau akun dibatasi 30 hari terakhir?

Jawab nomor 2 dan 3 saja pun cukup — saya langsung hitung titik impas dan verdik boncos/tipis/sehat. Screenshot daftar kampanye juga boleh. Jangan kirim password/OTP.
```
