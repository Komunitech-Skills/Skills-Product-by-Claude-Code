# Regulasi & pajak kripto Indonesia (untuk bot) — dicek 2026-09-29

Status: **T** = dibaca langsung di situs resmi; **L** = pemberitaan pihak ketiga. Aturan bisa
berubah; untuk kepastian, cek ojk.go.id / pajak.go.id / peraturan.bpk.go.id atau konsultan.

## Pengawasan
- Aset kripto diawasi **OJK** (peralihan dari Bappebti sejak 10 Januari 2025; masa transisi
  berakhir 20 Januari 2026). Dasar: UU 4/2023 (P2SK), PP 49/2024, POJK 27/2024 jo. POJK 23/2025. (T)
- Perdagangan hanya lewat **PAKD** (Pedagang Aset Keuangan Digital) berizin OJK. Per Mei 2026
  tercatat 26 PAKD, termasuk Indodax, Tokocrypto, Pintu, Reku, Pluang (L — pemberitaan:
  https://coinvestasi.com/berita/daftar-exchange-kripto-berizin-ojk-di-indonesia).
  Daftar resmi: https://ojk.go.id/id/Fungsi-Utama/ITSK/Perizinan-ITSK-Aset-Keuangan-Digital-Aset-Kripto/
- **Binance global** tidak tercantum di daftar itu (L). Di skill ini Binance dipakai untuk
  **testnet** (latihan). Live di Binance butuh pernyataan tambahan di konfigurasi.
- Bot di skill ini menjalankan transaksi di **akun member sendiri**, dengan aturan member sendiri.
  Komunitech tidak mengelola dana dan tidak memberi rekomendasi (kegiatan itu diatur OJK).
- Dugaan investasi ilegal: OJK 157 / Satgas PASTI.

## Pajak (PMK 50/2025, berlaku 1 Agustus 2025) (T)
Sumber: https://www.pajak.go.id/index.php/en/node/118105 · https://www.pajak.go.id/en/node/117774 ·
teks: https://peraturan.bpk.go.id/Details/326291/pmk-no-50-tahun-2025

| Hal | Aturan | Di bot |
|---|---|---|
| PPh 22 final, jual lewat PPMSE/PAKD dalam negeri | 0,21% dari nilai transaksi, dipungut dari **penjual** oleh bursa | `"pajak": "domestik"` (bawaan Indodax) |
| PPh 22 final, platform luar negeri | 1% dari nilai transaksi; bila platform tidak ditunjuk DJP, penjual menyetor sendiri | `"pajak": "luar_negeri"` (bawaan Binance) |
| PPN atas penyerahan aset kripto | Tidak dikenai (Pasal 2 ayat (1): dipersamakan dengan surat berharga) | tidak dihitung |
| Pembeli | Tidak dikenai PPh ini | beli tanpa PPh |
| PPN atas jasa/fee platform | tidak dirinci di sumber yang dibaca | fee diperlakukan sebagai angka total dari bursa |

**Pembulatan:** PPh = nilai jual × tarif, dibulatkan **ke bawah** ke rupiah (tidak pernah
melebihi tarif). Fee dibulatkan ke rupiah terdekat. **Belum dicocokkan dengan Coretax** —
bukti potong dari bursa yang berlaku. Untuk pasangan USDT, PPh dihitung dalam USDT (8 desimal);
rekap Rupiah memakai `--kurs-idr` yang member isi sendiri.
