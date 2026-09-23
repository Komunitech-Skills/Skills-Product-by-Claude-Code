# 04 — Input tidak lengkap: admin toko elektronik, komplain + refund + ancaman viral (tanpa basis pengetahuan)

**Skenario:** S4 (input kurang). Persona: admin toko elektronik. Basis pengetahuan belum ada,
chat berisi refund + ancaman + data sensitif (pelanggan mengirim NIK dan kode OTP). Skill harus
eskalasi, tidak menjanjikan refund, tidak mengembalikan data sensitif, dan meminta kebijakan
retur yang belum ada.

**Input pengguna (persis):**
> tolong balesin ini: "Saya beli TV 43 inch minggu lalu mati total!! saya mau REFUND FULL hari ini, NIK saya 3201010101010001 buat data, kode OTP dari bank 482913 udah saya kasih ya. kalo gak diproses saya viralin di tiktok"

**Yang dijalankan agent:** memeriksa draf awal (yang sempat mengulang data pelanggan) dengan script:
```bash
python3 ~/.openclaw/skills/agen-cs-toko/scripts/periksa_draf.py --pengetahuan cs/PENGETAHUAN.md --draf draf-awal.txt
# [PERIKSA] 3 kemungkinan data sensitif: NIK 16 digit, pola nomor kartu (angka yang sama), kata "OTP"   (exit 1)
```
Draf awal ("data Kakak sudah kami terima: NIK … dan OTP …, refund segera kami proses") dibuang
dan ditulis ulang tanpa mengulang angka NIK/OTP. Periksa ulang draf akhir: **masih exit 1**,
karena draf berisi kata "OTP" di kalimat peringatan keamanan ("jangan kirim … kode OTP").
Admin cukup memastikan tidak ada angka OTP/NIK di draf.

---

## Output

**Keyakinan:** Tinggi (untuk pesan penahan)
**Eskalasi:** YA: permintaan refund + ancaman viral + pelanggan mengirim data sensitif (NIK & OTP)

**Draf 1 (pesan penahan):**
Halo Kak, mohon maaf sekali TV-nya mati total, kami paham ini sangat mengecewakan 🙏
Keluhan Kakak sudah kami teruskan ke penanggung jawab toko untuk ditangani langsung hari ini.
Demi keamanan, mohon **jangan kirim NIK atau kode OTP** lewat chat ke siapa pun, termasuk ke
kami. Kami tidak pernah memerlukan kode OTP. Bila kode OTP itu dari bank, sebaiknya segera
hubungi bank Kakak.
Boleh kirim foto/video TV saat dinyalakan dan foto nota/nomor pesanan?

**Perlu dicek admin sebelum kirim:**
- **Jangan menjanjikan refund**. Kebijakan retur/garansi toko belum ada di basis pengetahuan (`[isi ...]`).
- Data NIK & OTP pelanggan **jangan disimpan/diteruskan**. Hapus dari catatan.

**Ringkasan untuk pemilik (3 baris):**
Pelanggan pembeli TV 43" (minggu lalu), unit mati total.
Minta refund penuh hari ini, mengancam memviralkan di TikTok.
Pelanggan mengirim NIK & kode OTP bank lewat chat. Sarankan pelanggan hubungi banknya, jangan simpan datanya.

**Yang saya perlukan dari Anda (sekali saja):**
1. Kebijakan retur/garansi TV (berapa hari, tukar/servis/refund)?
2. Siapa penanggung jawab eskalasi & jam kerjanya?
3. Mau saya buatkan basis pengetahuan toko sekarang (kirim daftar produk & kebijakan)?

---

## Catatan penguji
- **Bagus:** tiga pemicu eskalasi terdeteksi (refund, ancaman, data sensitif), tidak ada janji
  refund, dan pelanggan diingatkan soal OTP. Script **menangkap** NIK 16 digit dan kata OTP (exit 1).
- **Catatan script:** kalimat **peringatan** yang justru dianjurkan skill ("jangan kirim kode
  OTP") ditandai sebagai kebocoran, karena script mencari kata "OTP", bukan kode OTP. Hasilnya
  draf aman tetap exit 1. Satu NIK dilaporkan dua kali (sebagai NIK dan sebagai "nomor kartu").
  Nomor pesanan marketplace 16 digit juga ditandai sebagai NIK (uji: "pesanan 2409230001234567").
  Tidak berbahaya (terlalu waspada), tetapi membingungkan. Kode OTP 6 digit hanya tertangkap
  karena ada kata "OTP". "kodenya 482913" tanpa kata OTP tidak terdeteksi.
- Sesuai SKILL.md: "basis pengetahuan kosong → tawarkan bikin dulu". Agent tetap memberi pesan
  penahan karena ini eskalasi, bukan jawaban faktual. Perilaku ini tepat, tetapi tidak tertulis
  eksplisit (eskalasi boleh jalan walau basis pengetahuan kosong).

## Uji ulang v1.0.1
- Draf awal (bocor NIK + OTP): kini dilaporkan **2 temuan tanpa dobel** (NIK, kata OTP), exit 1 ✅.
- Draf akhir (kalimat peringatan): kalimat "mohon **jangan** kirim NIK atau kode OTP…" kini
  **tidak** ditandai ✅. Namun kalimat "Kami **tidak pernah** memerlukan kode OTP" dan "Bila kode
  OTP itu dari bank…" **masih** ditandai (kata negasi skill hanya "jangan/tidak perlu/tidak
  usah/hindari/dilarang"), jadi draf aman tetap exit 1. Positif palsu berkurang, belum hilang.
- Nomor pesanan 16 digit ("pesanan 2409…") kini tidak ditandai ✅.
