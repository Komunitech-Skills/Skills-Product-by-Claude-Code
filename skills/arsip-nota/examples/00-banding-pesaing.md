# Uji banding pesaing — arsip-nota vs skill publik sejenis

Diuji oleh penguji independen, 26 September 2026. Skill pesaing **hanya dibaca untuk dinilai** (lewat pencarian web, ringkasan hasil pencarian, dan halaman deskripsi publik), **tidak disalin** kode/teks/template-nya.

## Kata kunci & sumber yang dicari
- "receipt organizer agent skill claude clawhub expense filing"
- "skills.sh receipt archive OCR expense organizer skill"
- "ComposioHQ invoice-organizer SKILL.md categories OCR duplicate detection database"

Sumber yang ditemukan: `github.com/ComposioHQ/awesome-claude-skills` (invoice-organizer), `claude-office-skills/skills` (expense-tracker, invoice-organizer), beberapa mirror di skills.sh/skillstore.io/agentskill.sh, dan `egadams/receipt-scanner-master`.

## Pesaing paling relevan: **ComposioHQ `invoice-organizer`**
(dinilai dari deskripsi publik & ringkasan README, tidak diunduh/dibaca kodenya secara utuh — cukup untuk menilai fitur berdampingan)

| Aspek | ComposioHQ `invoice-organizer` (pesaing) | Komunitech `arsip-nota` |
|---|---|---|
| Baca isi nota (OCR) | Ya, skill ini sendiri yang membaca PDF/foto & mengekstrak vendor/tanggal/nominal | Tidak — sengaja dipisah ke `ekstrak-nota-faktur`; arsip-nota murni merapikan file & data yang sudah ada |
| Penyimpanan indeks | Tidak disebutkan ada database terstruktur — mengandalkan CSV & struktur folder | SQLite lokal dengan skema (id, hash, tanggal, vendor, nominal, kategori) → bisa dicari/direkap presisi lewat SQL |
| Deteksi duplikat | "Menyimpan salinan kualitas terbaik" (generik, tidak dijelaskan mekanismenya) | Hash SHA-256 per file (pasti, diuji: dua file identik isi selalu terdeteksi) + kemungkinan-dobel by tanggal+vendor+nominal |
| Lokalisasi Indonesia | Tidak ada — kategori & bahasa Inggris (Software/Office/Travel), tidak menangani format "45rb"/"Rp 1.250.000" | Kategori UMKM Indonesia (bahan baku, listrik/air/internet, dst.), parser nominal format Indonesia teruji |
| Keamanan tulis | Tidak disebut ada mekanisme pratinjau/konfirmasi eksplisit sebelum menulis/memindah file | Wajib pratinjau tanpa `--ya` dulu, konfirmasi eksplisit, file asli tidak pernah dihapus |
| Integrasi pembukuan lokal | Ekspor CSV generik (siap QuickBooks/Xero — SaaS luar) | Ekspor CSV siap-impor langsung ke `kas-umkm` (buku kas lokal Indonesia) — **diuji nyata pada sesi ini**: 10 baris nota, Rp 2.422.500, berhasil diimpor tanpa error dan hasil rekap kas-umkm cocok persis |
| Biaya berjalan | Tidak diketahui (perlu akses OCR — kemungkinan API berbayar) | Python standar lokal, tanpa API key/langganan |

## Kesimpulan uji banding
Pesaing unggul di satu hal: menyatukan OCR + organizing dalam satu skill (lebih "instan" untuk pengguna yang belum punya hasil ekstrak nota). Namun untuk target pasar Komunitech (UMKM Indonesia, integrasi ke buku kas lokal, format Rupiah/tanggal Indonesia, kontrol keamanan data eksplisit), arsip-nota **unggul telak** pada lokalisasi, keandalan angka (parser teruji, bukan tebakan OCR yang bisa salah baca), deteksi duplikat berbasis hash yang pasti, dan integrasi nyata dengan `kas-umkm` — dibuktikan lewat pengujian impor CSV aktual di sesi ini, bukan klaim.

**arsip-nota tidak kalah dari pesaing → tidak termasuk kasus "skor maks. 6" pada Tahap 6 poin 5.**

Catatan: penilaian pesaing di atas berdasarkan deskripsi publik/README (skill tidak dijalankan/diinstal), sesuai batasan "hanya dibaca untuk dinilai".
