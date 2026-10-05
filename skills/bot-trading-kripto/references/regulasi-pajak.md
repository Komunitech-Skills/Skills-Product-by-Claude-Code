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
Teks resmi (dibaca langsung 2026-09-29):
https://jdih.kemenkeu.go.id/api/download/66a7633b-9e1b-4a54-9046-5320aa96c7e1/2025pmkeuangan050.pdf ·
https://peraturan.bpk.go.id/Details/326291/pmk-no-50-tahun-2025 · ringkasan DJP:
https://www.pajak.go.id/index.php/en/node/118105 · https://www.pajak.go.id/en/node/117774

| Hal | Aturan | Di bot |
|---|---|---|
| PPh 22 final, jual lewat PPMSE/PAKD dalam negeri | 0,21% dari nilai transaksi (Pasal 12 ayat (1)–(4)), dipungut oleh bursa | `"pajak": "domestik"` (bawaan Indodax) |
| PPh 22 final, platform luar negeri | 1% dari nilai transaksi (Pasal 20 ayat (1)); bila platform belum ditunjuk, penjual menyetor sendiri (Pasal 22) | `"pajak": "luar_negeri"` (bawaan Binance) |
| Nilai transaksi, pasangan **rupiah** | nilai uang yang dibayar pembeli (Pasal 12 ayat (5) huruf a) | PPh hanya di sisi **jual**; beli tanpa PPh |
| Nilai transaksi, **tukar-menukar kripto (swap)**, mis. BTC/USDT | nilai **masing-masing** aset kripto yang diserahkan para pihak (Pasal 11 ayat (2) huruf b, Pasal 12 ayat (5) huruf b & ayat (7)); contoh resmi Lampiran huruf B: kedua pihak masing-masing dipungut 0,21% | PPh di **kedua sisi**: beli (menyerahkan USDT) dan jual (menyerahkan BTC); dihitung dalam USDT; rekap dipisah per mata uang kutipan, rupiah hanya perkiraan dengan `--kurs USDT=<angka>` dari member |
| PPN atas penyerahan aset kripto | Tidak dikenai (Pasal 2 ayat (1): dipersamakan dengan surat berharga) | tidak dihitung |
| PPN atas jasa platform (fee) | **Dikenai PPN** (Pasal 2 ayat (2) huruf a, Pasal 3): 12% × 11/12 × komisi (Pasal 5), dipungut oleh platform | fee diperlakukan sebagai angka total dari bursa (termasuk PPN bila bursa membebankannya) |

**Pembulatan:** PPh = nilai jual × tarif, dibulatkan **ke bawah** ke rupiah (tidak pernah
melebihi tarif). Fee dibulatkan ke rupiah terdekat. **Belum dicocokkan dengan Coretax** —
bukti potong dari bursa yang berlaku. Untuk pasangan USDT, PPh dihitung dalam USDT (8 desimal);
rekap dipisah per mata uang kutipan (IDR/USDT/USDC/BTC tidak pernah dijumlahkan); angka rupiah untuk kutipan non-IDR hanya perkiraan dengan `--kurs KUTIPAN=<angka>` yang member isi sendiri, format Indonesia (`16.500`/`16500`, desimal koma; bentuk ambigu ditolak; `--kurs-idr` lama = kurs USDT). PMK meminta konversi kripto memakai nilai
bursa/sistem platform (Pasal 12 ayat (7)); kurs dari member hanyalah perkiraan rekap — bukti potong
dari bursa yang berlaku. Kutipan yang dianggap fiat (tanpa PPh sisi beli): IDR, USD, EUR, dan mata
uang fiat lain di `KUTIPAN_FIAT` (`scripts/inti.py`); kutipan lain dianggap aset kripto.
