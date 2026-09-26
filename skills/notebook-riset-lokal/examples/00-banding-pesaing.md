# 00 — Uji banding pesaing

## Pesaing yang ditemukan
Pencarian web (26 September 2026, lihat kata kunci di bawah) tidak menemukan skill publik yang mengoperasikan **Open Notebook lokal** secara khusus (ClawHub/skills.sh/GitHub). Yang ditemukan dan relevan untuk dinilai berdampingan:

1. **Skill "NotebookLM connector" untuk Claude Code** (mengakses **Google NotebookLM** asli via API/browser dari dalam Claude Code) — disebut di hasil pencarian umum sebagai skill yang menjawab pertanyaan dari notebook NotebookLM pengguna dengan jawaban bersumber & berkutipan dari Gemini.
2. **Google NotebookLM** (produk resmi, dibaca lewat pengetahuan umum & dokumentasi publik, bukan disalin) sebagai pembanding produk yang dituju skill kita ("alternatif lokal").

Kata kunci yang dicari: `Open Notebook skill`, `NotebookLM skill Claude`, `ClawHub research assistant skill`, `skills.sh notebook`. Sumber: hasil pencarian web umum (Composio, DataCamp, awesome-openclaw-skills, dll.) — tidak ada satupun mengarah ke skill lokal Open Notebook yang setara.

## Perbandingan berdampingan (skenario: kumpulkan dokumen lalu tanya-jawab)

| Aspek | `notebook-riset-lokal` (skill kita) | Skill konektor NotebookLM (cloud) | NotebookLM asli (produk Google) |
|---|---|---|---|
| Lokasi data | 100% komputer pengguna (Open Notebook lokal) | Dokumen tetap di akun Google NotebookLM pengguna | Server Google |
| Butuh akun/login | Tidak (opsional kata sandi API lokal) | Ya, akun Google + izin | Ya, akun Google |
| Setup awal | Docker (±20–30 menit) atau jasa setup | Login Google sekali | Buka browser, langsung pakai |
| Biaya | Gratis (Docker) atau berbayar bila pakai API model | Gratis (kuota NotebookLM Google) | Gratis (kuota) |
| Menambah sumber lewat chat AI | **Rusak (bug ditemukan)** — lihat `HASIL-UJI.md` | Tidak jelas diuji (di luar cakupan sesi ini) | Manual lewat UI web |
| Pencarian tanpa AI | Ada (`cari`), tapi cuplikan/tipe kosong (bug lain) | Tidak ada padanan (NotebookLM tidak punya "cari kata kunci mentah" terpisah dari chat) | Tidak ada versi non-AI |
| Podcast audio | Ada (opsional, perlu TTS) | Tidak diketahui | Ada (fitur andalan NotebookLM) |
| Privasi | Tinggi (lokal) | Tergantung kebijakan data Google NotebookLM | Data diproses Google |

## Penilaian
- **Keunggulan konsep skill kita:** privasi penuh (data usaha lokal), tidak perlu akun Google, cocok untuk dokumen sensitif (kontrak, regulasi internal, SOP klinik) yang pemilik usaha Indonesia tidak mau kirim ke cloud pihak ketiga.
- **Kelemahan saat ini (implementasi, bukan konsep):** `tambah-sumber` — fitur paling dasar untuk "mengumpulkan dokumen" — gagal total terhadap server Open Notebook 1.14.0 asli (bug format request). Sampai bug ini diperbaiki, skill kita **kalah telak** dari NotebookLM asli (yang uploadnya via UI web tetap berfungsi) dan dari skill konektor NotebookLM cloud (yang tinggal memanggil API resmi Google yang stabil) — bukan karena konsepnya lemah, tapi implementasinya belum teruji ke server sungguhan sebelum sesi ini.
- Setelah bug diperbaiki, keunggulan privasi + tanpa akun + pencarian cepat tanpa AI membuat skill ini punya proposisi nilai yang kuat dan berbeda dari kedua pesaing di atas — tidak ada yang menawarkan kombinasi "100% lokal + operasional lewat chat AI" untuk profesional Indonesia.

**Kesimpulan:** bukan kasus "skill kita kalah karena skill pesaing lebih baik secara konsep" (skor maks. 6 tidak berlaku di sini) — konsepnya unik dan belum ada pesaing langsung yang ditemukan. Nilai diturunkan murni karena bug implementasi yang ditemukan uji ini terhadap server asli (lihat `HASIL-UJI.md`).
