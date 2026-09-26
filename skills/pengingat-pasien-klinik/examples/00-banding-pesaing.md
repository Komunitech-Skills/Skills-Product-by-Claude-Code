# Uji banding pesaing — pengingat pasien klinik

## Kata kunci & sumber yang dicari
- "agent skill patient reminder appointment recall skill.md github clinic WhatsApp"
- "pengingat kontrol pasien klinik skrip WhatsApp aplikasi gratis reminder janji temu"
- Diperiksa juga (tanpa hasil relevan tambahan): ClawHub, skills.sh, anthropics/skills — tidak
  ditemukan skill agent (format SKILL.md) khusus "pengingat pasien klinik" per 26 Sep 2026.

## Yang ditemukan
Tidak ada skill/prompt AI-agent publik (ClawHub/skills.sh/GitHub awesome-list) untuk kasus yang
sama persis (buku jadwal lokal minimal + draf WA manual, dengan penjaga privasi kesehatan).
Yang ada adalah **aplikasi/SaaS berbayar** untuk klinik, semuanya dengan model berbeda:

| Produk | Model | Catatan |
|---|---|---|
| reminderpasien.com, hubpasien.com | SaaS berlangganan | Kirim **otomatis** via WhatsApp Business API/blast, perlu setup API & akun bisnis, biaya bulanan |
| Qontak (chatbot WA klinik) | SaaS berlangganan | Chatbot balasan otomatis, bukan sekadar draf; perlu integrasi WA Business API |
| Carepatron (patient appointment reminder software) | SaaS luar negeri, sebagian gratis | Bahasa Inggris, dirancang untuk sistem rekam medis penuh (EMR), bukan alat berdiri sendiri |
| whatsapp-clinic-agent, ai-agent-whatsapp-clinic (GitHub) | Kode sumber terbuka, tapi proyek pribadi/skrip developer | Perlu API key LLM + WhatsApp Business Cloud API, ditujukan untuk booking/triage otomatis, bukan skill agent siap pakai |

## Penilaian berdampingan (skenario "catat pasien kontrol behel + lihat siapa yang harus diingatkan hari ini")
- **Pesaing (SaaS/chatbot WA otomatis):** butuh pendaftaran akun, sering butuh WhatsApp Business
  API resmi (biaya & verifikasi Meta), dan **mengirim pesan otomatis** ke pasien — bertentangan
  langsung dengan keputusan pemilik (WA via OpenClaw tidak resmi, harus draf + manusia kirim).
  Sebagian besar juga menyimpan data pasien jauh lebih luas dari yang dibutuhkan (cocok untuk
  EMR, bukan minimal-data).
- **Skill kita:** tanpa akun/API/biaya bulanan, data 100% lokal di CSV, hanya field minimal
  (nama panggilan, WA, jenis umum, tanggal), draf WA disalin manual oleh staf, ada penjaga
  eksplisit agar diagnosis/rekam medis tidak pernah masuk, dan hak hapus data langsung dijalankan.

## Kesimpulan
Tidak ada pesaing skill-agent langsung yang bisa dibandingkan head-to-head dalam format yang
sama. Dibandingkan alternatif SaaS yang ada, skill kita unggul untuk target pasar (klinik kecil
UMKM, awam teknologi, tanpa mau bayar bulanan/API resmi, dan wajib manusia yang mengirim pesan
kesehatan) — justru karena **sengaja tidak** meniru fitur auto-send SaaS tersebut, sesuai batasan
pemilik. Nilai tambah dibanding "tanpa skill" sudah dibuktikan di `00-pembanding-tanpa-skill.md`.
