# Kurasi: RamaAditya49/rama-copywriting

Tanggal tinjau: 2026-09-23 · Peninjau: agent kurator · Status: **menunggu keputusan koordinator/pemilik**

## 1. Identitas

| Item | Isi |
|---|---|
| Nama | rama-copywriting (1 skill) |
| URL | https://github.com/RamaAditya49/rama-copywriting |
| Ditemukan lewat | Pencarian GitHub `topic:agent-skills indonesia` (topik `bahasa-indonesia`, `copywriting`) |
| Pembuat | Rama Aditya (RamaAditya49) |
| Update terakhir | 2026-07-21 (3 commit) |
| **Lisensi (file LICENSE dibaca langsung)** | **Apache License 2.0**, teks lengkap tanpa pengisian baris hak cipta (appendix masih placeholder). **Tidak ada file NOTICE.** |
| Popularitas | 4 bintang |

Isi: `SKILL.md` (136 baris), `references/` (psychology-and-evidence, language-id-en, emoji-and-channels, anti-slop, examples; sekitar 1.000 baris), `agents/openai.yaml`, dan gambar hero.

### Ringkasan isi
Skill copywriting ID/EN yang menekankan **kejujuran klaim**: brief minimum (hasil, audiens, penawaran, bukti, konteks, suara), **claim ledger** (Verified / Attributed / Qualified / Unverified), pesan sebelum kata-kata, persuasi yang bertanggung jawab (tanpa kelangkaan palsu, dark pattern, atau testimoni palsu), transkreasi alih-alih terjemahan harfiah, pemeriksaan anti-slop, varian uji A/B per hipotesis, dan gerbang akhir. Referensi bahasa Indonesia membahas pemilihan sapaan (saya/Anda, kami/kamu), campur kode, dan aksesibilitas emoji.

## 2. Audit keamanan (Tahap 3)

| Pemeriksaan | Hasil |
|---|---|
| Script | Tidak ada. |
| Jaringan / kredensial / `curl \| bash` / obfuscation | Tidak ada. README hanya berisi `git clone` untuk instalasi manual. |
| Prompt injection | Tidak ada. Justru ada aturan menolak copy menipu dan tidak membocorkan data pribadi. |
| Karakter tersembunyi | Tidak ada. |
| Data pribadi / API key | Tidak ada. |

**Hasil: LULUS.**

## 3. Penilaian

- **Kualitas: 8/10.** Kerangka matang, jujur, dan sadar regulasi. Kelemahan untuk pasar kita: SKILL.md berbahasa Inggris, generik (tidak spesifik UMKM atau marketplace Indonesia), dan tidak ada contoh WhatsApp/Shopee/Tokopedia yang konkret. Referensinya panjang untuk pembeli awam.
- **Tumpang tindih:** `caption-sosmed-umkm`, `broadcast-wa`, `listing-marketplace`, `naskah-live-jualan`, `kalender-konten-30hari`, `surat-penawaran-harga`. Tidak ada skill kita yang punya "claim ledger" atau aturan kejujuran klaim setegas ini.
- **Keputusan: KURASI** (Apache-2.0 mengizinkan penggunaan komersial dan modifikasi), **sebagai komponen**, bukan dijual berdiri sendiri. Menjualnya apa adanya tidak memberi nilai tambah karena gratis di GitHub.

## 4. Usulan nilai tambah

1. **Transkreasi ke bahasa Indonesia sehari-hari** dan dipadatkan menjadi satu rujukan bersama, misalnya `references/klaim-jujur.md`, untuk skill marketing kita. Isinya: claim ledger, daftar "klaim yang wajib berbukti" (termasuk kata "gratis", "terlaris", dan "no. 1"), dan larangan kelangkaan palsu.
2. **Dasar aturan lokal:** Etika Pariwara Indonesia (superlatif), UU Perlindungan Konsumen (UU 8/1999), aturan klaim BPOM untuk kosmetik/pangan, dan UU PDP untuk personalisasi broadcast. Tanggal berlaku dicantumkan.
3. **Contoh lokal hasil uji:** caption Instagram warung kopi, deskripsi produk Shopee, broadcast WA promo Lebaran, dan naskah live TikTok Shop, masing-masing dengan versi sebelum/sesudah.
4. Opsional: skill mandiri `audit-klaim-promosi` (cek iklan/caption dari klaim berisiko) sebagai tier **GRATIS** (lead magnet) atau bagian "Paket Toko Online".

## 5. Kewajiban lisensi jika dipakai (Apache-2.0)
- Sertakan salinan teks lisensi Apache-2.0.
- Atribusi ke Rama Aditya dan URL repo di `ATTRIBUTION.md`.
- **Nyatakan dengan jelas bahwa file telah diubah** (terjemahan, ringkasan, penambahan konteks Indonesia).
- Tidak ada file NOTICE asli, jadi tidak ada NOTICE yang wajib diteruskan. Catat fakta ini.
- Catat `jalur=kurasi`, `lisensi=Apache-2.0` di `catalog.csv`.
