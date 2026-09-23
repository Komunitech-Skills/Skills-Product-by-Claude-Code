# 00 — Uji banding pesaing: buku-stok

Tanggal: 2026-09-23. Semua sumber hanya **dibaca**; tidak ada script pihak ketiga yang dijalankan, tidak ada teks yang disalin.

## Pencarian
| Sumber | Kata kunci / halaman | Hasil |
|---|---|---|
| Web/GitHub | "SKILL.md inventory stock management agent skill" | `peterbamuhigire/skills-web-dev` → skill `inventory-management` (MIT, via skills.lc); `majiayu000/claude-skill-registry` → `commerce-inventory` (lisensi tidak disebut) |
| github.com/VoltAgent/awesome-openclaw-skills | README + `categories/shopping-and-e-commerce.md` | Tidak ada skill stok/inventori untuk toko; tidak ada Shopee/Tokopedia/TikTok Shop (hanya amazon-orders, atoship, food-order, filewave "device inventory") |
| manairalabs/bicara-skills | daftar skill | invoice-extract-id, wa-reply-id; `stock-opname-id` baru disebut sebagai rencana — belum ada |
| alvinindra/bahasa-skills | daftar skill | hanya skill penulisan bahasa; tidak relevan |
| anthropics/skills, skills.sh, ClawHub | (lewat awesome-list & pencarian) | Tidak ditemukan skill stok untuk toko/marketplace Indonesia |
| Aplikasi open-source | InvenTree (MIT) — docs.inventree.org (stock, pricing) | Pembanding kemampuan (bukan skill) |

## Pesaing yang dinilai
1. **`inventory-management`** — https://skills.lc/peterbamuhigire/skills-web-dev/peterbamuhigire-skills-web-dev-inventory-management-skill-md (repo github.com/peterbamuhigire/skills-web-dev, MIT). Isinya panduan untuk **developer** yang membangun modul inventori ERP berbasis PHP (alur purchase → receiving → movement → sale, FIFO/LIFO/average per kelas produk, approval penyesuaian). Tidak ada database/script yang bisa dipakai pemilik toko.
2. **`commerce-inventory`** — https://github.com/majiayu000/claude-skill-registry/blob/main/skills/data/commerce-inventory/SKILL.md. Membungkus CLI/MCP platform Stateset (`stateset-inventory`, `adjust_inventory`, `--apply` untuk tulis). Tidak bisa jalan tanpa akun & backend Stateset; lisensi tidak disebut.
3. **InvenTree** (aplikasi, MIT) — server Django + database, stok per lokasi, stocktake, riwayat pelacakan, sales order. Valuasi memakai **rentang harga min/maks** (docs: "overall pricing range is calculated based on the minimum and maximum of available pricing data"), bukan HPP rata-rata tertimbang; tidak ada impor file pesanan Shopee/TikTok/Tokopedia.

## S1 dengan instruksi pesaing
Input: "Ini file pesanan Shopee hari ini (shopee-hari1.csv), potong stoknya dan buatkan daftar ambil barang ya"

**Agent yang memuat `inventory-management`:**
```
Skill ini menyiapkan arsitektur modul inventori. Saran saya: buat tabel stock_movements
(product_id, warehouse_id, qty, type, user, timestamp), endpoint penerimaan barang, dan
aturan "negative stock prevention". File Shopee Anda bisa diproses setelah modul ini
dibangun dan dihubungkan ke ERP (lihat docs/API.md proyek Anda).
```
→ Tidak menghasilkan stok terpotong maupun picking list; menganggap pengguna developer yang punya ERP.

**Agent yang memuat `commerce-inventory`:**
```
Saya perlu akses Stateset (stateset-inventory). Perintah tidak tersedia di komputer ini.
Silakan pasang/login Stateset CLI dan impor produk Anda dulu.
```
→ Berhenti: butuh akun & platform luar (bertentangan dengan "tanpa setup" dan data lokal).

**Agent dengan skill kita:** lihat `01-impor-shopee-dan-picking.md` (pratinjau → "ya" → stok terpotong + backup + daftar ambil per rak + urutan resi; angka diverifikasi).

## Penilaian (1–10)
| Kriteria | inventory-management | commerce-inventory | InvenTree (aplikasi) | **buku-stok** |
|---|---|---|---|---|
| Kualitas hasil S1 | 2 | 1 | 6 (setelah server dipasang & data disiapkan; tanpa impor Shopee) | **9** |
| Kesesuaian konteks Indonesia | 1 | 1 | 3 | **9** |
| Akurasi | n/a | n/a | tinggi untuk qty; tanpa HPP rata-rata | **9** (v1.1.1: HPP, stok & laporan cocok 100% dengan model independen, ±17.500 langkah acak) |
| Siap pakai untuk awam | 1 | 1 | 3 (butuh server/Docker) | **8** |

**Kesimpulan:** tidak ada skill publik yang sebanding untuk pemilik toko/seller marketplace Indonesia. buku-stok **menang** telak.

## Yang bisa dipelajari (ide, bukan salinan)
- Dari InvenTree: status tambahan per stok (rusak/karantina), riwayat per pengguna (siapa mengubah), dan "reservasi/alokasi" pesanan terpisah dari pemotongan stok — berguna agar pesanan yang "pembatalan diajukan" tidak langsung mengembalikan stok.
- Dari `inventory-management`: approval untuk penyesuaian besar (mis. opname dengan selisih > X% minta konfirmasi ekstra).
- Dari `commerce-inventory`: pola `--apply` sama dengan `--ya` kita — konfirmasi eksplisit sebelum tulis memang praktik umum yang baik.
