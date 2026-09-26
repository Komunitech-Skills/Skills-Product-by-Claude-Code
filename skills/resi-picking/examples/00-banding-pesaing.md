# Uji banding pesaing — resi-picking vs alat sejenis

## Kata kunci & sumber yang dicari
- "picking list generator Shopee CSV template gratis"
- "AI agent skill pick list OR picking list ClawHub OR skills.sh marketplace order"

Tidak ditemukan skill agent (ClawHub/skills.sh/anthropics/skills/GitHub) yang spesifik untuk
"picking list dari ekspor pesanan marketplace" — pencarian hanya mengarah ke direktori umum
marketplace skill (skills.sh, ClawHub) tanpa hasil skill konkret untuk tugas ini. Jadi **tidak ada
skill agent pesaing langsung** yang bisa dibaca & dinilai berdampingan untuk uji ini.

## Pesaing yang ada (bukan skill agent, tapi alat/fitur sejenis)
1. **Fitur bawaan Shopee Seller Centre "Generate Documents"** — bisa membuat picklist/packlist,
   tapi ini fitur di dalam dashboard Shopee sendiri (butuh login Seller Centre), tidak menggabungkan
   lintas marketplace (Tokopedia/TikTok Shop), dan tidak melakukan cross-check stok gudang sendiri.
2. **BigSeller / OneCart** — SaaS pihak ketiga berbayar (biaya bulanan/langganan), multi-channel,
   fitur lebih lengkap (barcode scanner, wave picking), tapi mengharuskan hubungkan akun toko ke
   layanan pihak ketiga (sesuai risiko yang justru dihindari CLAUDE.md: tanpa scraping/login akun
   toko oleh pihak luar) dan berbayar bulanan.

## Perbandingan
| Aspek | resi-picking | Fitur bawaan Shopee | SaaS pihak ketiga (BigSeller/OneCart) |
|---|---|---|---|
| Biaya berjalan | Sekali beli, tanpa langganan | Gratis (bagian Shopee) | Langganan bulanan |
| Lintas marketplace dalam 1 daftar | Manual gabung (jalankan 2x) | Tidak | Ya (native) |
| Perlu hubungkan akun ke pihak ketiga | Tidak (hanya file CSV lokal) | Tidak (asli Shopee) | Ya |
| Cross-check stok gudang sendiri | Ya (`--stok`) | Tidak | Tergantung paket |
| Privasi data pesanan | Tetap di komputer pengguna | Di Shopee | Di server SaaS pihak ketiga |
| Deteksi kolom ekspor non-standar | Sebagian (lihat skenario 02) | N/A | N/A |

## Kesimpulan uji banding
Tidak ada skill agent pesaing yang unggul untuk dinilai berdampingan langsung; dibanding
alternatif SaaS berbayar, keunggulan resi-picking adalah privasi (data tidak keluar komputer) dan
tanpa biaya bulanan — sejalan dengan misi "produk pengganti SaaS berbayar" di CLAUDE.md.
Kelemahannya: tidak menggabungkan lintas marketplace otomatis dan deteksi kolom non-standar masih
perlu override manual (lihat skenario 02) — SaaS berbayar biasanya lebih matang di titik ini karena
integrasi API resmi per marketplace.
