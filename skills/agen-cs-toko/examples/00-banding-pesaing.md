# 00 — Uji banding pesaing (S1)

## Pencarian
- **ClawHub** (API pencarian `clawhub.ai/api/v1/search`): kata kunci "customer service",
  "customer support", "knowledge base support", "whatsapp reply" (yang terakhir: koneksi putus,
  tidak ada hasil). Hasil relevan: `customer-support-autopilot` (±1.033 unduhan, **lisensi tidak
  dicantumkan**), `ai-cs` (WeChat/WeCom, 619 unduhan, lisensi tidak dicantumkan),
  `customer-service-reply`/`ecommerce-customer-service-pro` (Tionghoa, Taobao/JD), `supportforge`
  (butuh API pihak ketiga).
- **manairalabs/bicara-skills** → **`wa-reply-id`** (MIT), https://github.com/manairalabs/bicara-skills/blob/main/skills/wa-reply-id/SKILL.md.
  Draf balasan WA CS dalam Bahasa Indonesia untuk retail/F&B/jasa. **Pesaing paling relevan.**
- VoltAgent/awesome-openclaw-skills, anthropics/skills, alvinindra/bahasa-skills: tidak ada agen
  CS berbasis basis pengetahuan + eskalasi untuk WA Indonesia.
- Semua SKILL.md pesaing hanya **dibaca**, tidak dijalankan, tidak disalin.

## S1 dengan instruksi pesaing (`wa-reply-id`, register Casual-Warm karena pelanggan memakai "kak", "gak")
> Halo Kak! Siaapp 🙌
> Untuk Pashmina Ceruti harganya 89rb/pcs. Kalau ambil 3 bisa pakai Paket 3 Pashmina jadi 240rb ya, lebih hemat 😊
> Warna dusty pink stoknya masih ada ya Kak. Ongkir ke Bekasi tergantung alamat, boleh info kecamatannya?

(Pola "Stock inquiry" pesaing memakai template "stok masih ada ya" tanpa mekanisme cek. Agent
harus menebak atau bertanya, dan template mendorong jawaban "ada".)

Pembanding kedua, `customer-support-autopilot` (generik, Inggris): menghasilkan kategori +
severity + draf + "confidence level" + rekomendasi eskalasi & SLA. Tidak ada basis
pengetahuan, tidak ada konteks WA/Indonesia, dan file `setup.md`/`examples.md` yang dirujuk
tidak ikut dibaca.

## Output skill kita
Lihat `01-toko-hijab-basis-pengetahuan-dan-draf.md`.

## Penilaian
| Kriteria | wa-reply-id (MIT) | customer-support-autopilot | agen-cs-toko |
|---|---|---|---|
| Kualitas draf | 8: register bahasa sangat baik | 5: generik | 8: nada baik + 2 alternatif |
| Konteks Indonesia | 9 | 2 | 9 |
| Akurasi (tidak mengarang) | 5: template stok/refund mendorong janji ("stok masih ada", "refund diproses") tanpa sumber | 6: "never invent policy promises" | 9: basis pengetahuan + tanda "perlu dicek" + script |
| Eskalasi & data sensitif | 3: refund dijawab langsung, tidak ada NIK/OTP | 7: routing risiko | 9: eskalasi wajib, NIK/OTP, pesan penahan |
| Setup OpenClaw & keamanan kanal | 0 | 0 | 6: Copilot + Telegram, tapi ada cacat konfigurasi WA (lihat HASIL-UJI) |
| Siap pakai | 8 | 5 | 8 |

**Kesimpulan:** skill kita **unggul** secara keseluruhan. `wa-reply-id` lebih unggul pada
**kekayaan register bahasa** (tiga register dengan sinyal pemilihan yang jelas, katalog frasa
formal vs santai).

## Yang bisa dipelajari (ide, bukan salinan)
1. **Pemilihan register berbasis sinyal** (kata "dong/sih/btw" → santai; B2B/komplain resmi →
   formal). Bisa ditambahkan ke `ATURAN.md` sebagai aturan nada per jenis pelanggan (mis.
   percetakan B2B vs pembeli hijab).
2. **"Satu pertanyaan klarifikasi, bukan tiga"** untuk pesan yang tidak jelas. Aturan ringkas yang baik untuk draf.
3. **Klasifikasi kategori + severity** (dari `customer-support-autopilot`) untuk rekap harian:
   rekap per kategori (harga/stok/ongkir/komplain) lebih berguna daripada daftar mentah.
