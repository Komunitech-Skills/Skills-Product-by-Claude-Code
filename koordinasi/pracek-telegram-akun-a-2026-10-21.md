# Pra-cek Telegram Akun A — 2026-10-21

Penguji: sub-agent penguji (bukan pembuat skill). Cara: `uji-tg.sh` (OpenClaw lokal, `--channel telegram`, tanpa kirim apa pun), HOME uji berisi hanya skill terkait (disalin dari repo oleh `mk-home.sh`), satu giliran, dijalankan berurutan. Hanya sisi DENGAN skill. Skor 1-10 menurut `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian"; angka dihitung ulang dengan Python Decimal. Syarat tambahan dari penahanan (Akun B): naskah/hasil utuh harus sampai di chat.

| Skill | Versi | Skor | Verdik | Catatan |
|---|---|---:|---|---|
| audit-akun-iklan | 1.0.7 | 6,5 | TIDAK SIAP | Angka benar, tetapi ketiga cacat 16 Okt muncul lagi: verdik "BELUM BISA DIPASTIKAN" (tanpa label tunggal BONCOS/TIPIS/SEHAT), tindakan 2 & 3 (2FA, iklan ditolak/pelanggaran) tidak berkaitan dengan keluhan boncos, dan penutup "File kerja: belum ada…" kembali muncul. 2.339 karakter |
| perjanjian-sederhana | 1.0.8 | 7,5 | TIDAK SIAP | Naskah perjanjian UTUH tampil di chat (10 pasal + tanda tangan + Lampiran 1, dibagi "Bagian 1/3–3/3"); angka, tanggal, dan meterai benar; kontradiksi iuran pasar (gelombang 5) sudah hilang. Cacat kanal: jalur berkas `/opt/ochome/.openclaw/workspace/draft_sewa_kios_sri_mulyani.md` disebut, istilah proses "saya hitung pakai script" & "sudah dicek script". Panjang 13.664 karakter (±4 pesan Telegram; blok kode panjang bisa terpecah di tengah) |

## Rincian

### audit-akun-iklan 1.0.7 — 6,5 TIDAK SIAP
- Pesan uji: entri indeks 9 `pilot/msgs-g19b.json` (mention bot dihapus); tanpa data berkas. Tools: read, exec. Sesi `pc-audit-akun-iklan-21okt`. Catatan: folder `tests/` skill ikut tersalin oleh `mk-home.sh` (tidak dipanggil).
- Angka (Decimal): website laba kotor 89.000 − 32.000 − 1.500 = 55.500 (62,36 %), ROAS impas 1,6036 → tampil 1,61; 4.500.000/55.500 = 81,08 → 82 pesanan. GMV Max: potongan 12.905 + afiliasi 8.900 → 33.695 (37,86 %), ROAS impas 2,6413 → tampil 2,65; 6.000.000/33.695 = 178,07 → 179 pesanan. Batas "sehat" 1,61 × 1,2 = 1,932 → 1,94 dan 2,65 × 1,2 = 3,18: sesuai aturan SKILL.md. Tidak ada salah angka.
- Syarat terpenuhi: titik impas di balasan pertama, 3 tindakan, skor sementara "belum bisa dihitung" (±10 % bukti), 5 pertanyaan di akhir, asumsi biaya disebut.
- Tidak terpenuhi:
  1. Verdik tunggal: "VERDIK: BELUM BISA DIPASTIKAN" (ini memang perilaku yang diminta SKILL.md baris 137-142/185 bila ROAS aktual tidak disebut; perlu diubah di skill, mis. verdik "RAWAN BONCOS" untuk GMV Max berdasarkan ROAS impas 2,65 + pengguna sudah merasa boncos).
  2. Tindakan nyambung: hanya tindakan 1 (catat ROAS per jalur, pasang batas minimal ROAS) yang menjawab keluhan; tindakan 2 "Cek verifikasi 2 langkah aktif…" dan 3 "Cek ada tidaknya iklan ditolak…" tidak menekan rugi. Seharusnya mis. alihkan/kurangi anggaran GMV Max, set target ROI ≥ 2,65, cek komisi afiliasi 10 %.
  3. Istilah proses: "File kerja: belum ada — baru dibuat setelah data cek terisi lebih lengkap." (pada 17 Okt sempat hilang, kini muncul lagi; tidak stabil).
- Cacat kanal lain: tidak ada jalur berkas, tidak ada tabel, tidak terpotong.
- Bukti: "2) VERDIK: BELUM BISA DIPASTIKAN" / "2. Cek verifikasi 2 langkah aktif di TikTok Business Center dan akun Shopify" / "File kerja: belum ada".
- Kesimpulan: tanpa perubahan isi skill (masih 1.0.7, sama dengan pra-cek 16-17 Okt), hasil tidak akan membaik; jangan dikirim ulang ke bot asli sebelum SKILL.md direvisi (verdik default, tindakan wajib terkait keluhan, larang kalimat "File kerja").

### perjanjian-sederhana 1.0.8 — 7,5 TIDAK SIAP
- Pesan uji: skenario 1 `examples/00-openclaw-sebelum-sesudah.md` (sewa kios B-12 Pasar Baru Cikarang), sama persis. Tools: read, exec, write; berkas `draft_sewa_kios_sri_mulyani.md` (9.663 bita) ditulis di workspace. Satu payload 13.664 karakter. Sesi `pc-perjanjian-sederhana-21okt`. Folder `tests/` dihapus dari HOME uji.
- Angka (Decimal): 18.000.000 × 2 = 36.000.000; termin 9.000.000 × 4 pada 1 Nov 2026, 1 Mei 2027, 1 Nov 2027, 1 Mei 2028; periode 1 Nov 2026 – 31 Okt 2028; terbilang benar; denda 0,1 %/hari maks 5 % (= Rp9.000/hari, maks Rp450.000 per termin; asumsi template, ditandai minta konfirmasi); meterai 2 × Rp10.000 (UU 10/2020) dan "meterai bukan syarat sah" benar. Tidak ada salah angka/fakta.
- Syarat utama "naskah utuh sampai ke chat": TERPENUHI (cacat gelombang 5 "file gagal terkirim, hanya ringkasan" tidak terulang). Kontradiksi iuran gelombang 5 sudah beres (iuran/retribusi pengelola → penyewa di Pasal 5(2)b dan di daftar asumsi). Klausul pengosongan sepihak sudah diganti jalur musyawarah/pengadilan (Pasal 7(4)). Status hak pakai kios pasar disorot. Disclaimer ada.
- Cacat kanal (menggugurkan SIAP KIRIM):
  1. Jalur berkas: "Draf juga saya simpan di file: `/opt/ochome/.openclaw/workspace/draft_sewa_kios_sri_mulyani.md`" (bertentangan dengan keputusan 2026-10-05: jalur file tidak disebut, tawarkan "balas 'kirim file'").
  2. Istilah proses: "(saya hitung pakai script biar angka & terbilangnya akurat)" dan "(sudah dicek script, tidak ada ketidaksesuaian beban biaya/angka)".
  3. Panjang 13.664 karakter dalam blok kode ``` → di Telegram terbagi ±4 pesan; pemecahan 4.096 karakter bisa memotong blok kode (format monospace rusak). Lampiran 1 berupa baris pipa 4 kolom di dalam blok kode (kecil, masih terbaca).
- Minus kecil: dua gaya isian bercampur (`[isi: hari]` dan `[[NIK PIHAK PERTAMA]]`); judul "#"/"##" Markdown ikut tampil mentah di dalam blok kode.
- Bukti: "**Bagian 1/3** … # PERJANJIAN SEWA-MENYEWA TEMPAT USAHA" / "Termin ke-4 … Rp 9.000.000 … paling lambat tanggal 1 Mei 2028" / "Draf juga saya simpan di file: `/opt/ochome/…`".
- Perbaikan yang disarankan (urut dampak): larang menyebut jalur berkas & kata "script" di balasan kanal chat; naskah dikirim sebagai teks biasa (bukan satu blok kode raksasa) per bagian < 4.000 karakter; satu gaya isian `[isi: …]`. Dengan dua perbaikan pertama, isinya layak ≥ 8.

## Kandidat
Tidak ada entri baru di `pilot/kandidat-a-cepat.json` (kedua skill TIDAK SIAP).
