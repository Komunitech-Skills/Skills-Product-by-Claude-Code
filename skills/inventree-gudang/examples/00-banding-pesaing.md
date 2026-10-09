# Uji banding pesaing

**Pencarian (29 Sep 2026):** "InvenTree MCP server AI agent", "inventree skill SKILL.md clawhub skills.sh". Ditemukan: server MCP resmi **inventree/inventree-mcp** (https://github.com/inventree/inventree-mcp, MIT, © Oliver Walters/InvenTree; PyPI `inventree-mcp` 0.3.0; commit pertama 2026-07-29, terakhir 2026-09-22), beberapa MCP komunitas (munin92/inventree-mcp, hvkshetry/inventree-mcp di Glama, syntaxerr66 di LobeHub, sengine-cloud fork). **Tidak ditemukan** SKILL.md InvenTree di ClawHub/skills.sh/anthropics/skills. Pesaing terkuat = MCP resmi (pembuat resmi, dirawat, ada tes).

## Pesaing: inventree-mcp resmi (dibaca dari kode sumber, tidak disalin)
- Bentuk: **plugin InvenTree** (Streamable HTTP di `/plugin/inventree-mcp/mcp/`), dipasang `pip install inventree-mcp` di server lalu diaktifkan di Admin > Plugins.
- Alat: ±55 alat `list_*`/`get_*` pembungkus tipis REST API (parts, stock, lokasi, PO/SO/RO/build + baris, BOM, supplier parts, tracking, parameter…), skema keluaran otomatis, alat difilter sesuai hak akun. **Saat ini hanya-baca** (tidak ada opname / terima barang).
- Tidak ada lokalisasi, rumus "perlu dipesan", format siap tempel, atau panduan awam.

## Menjalankan skenario 1 dengan pesaing
Tidak dapat dijalankan langsung di instalasi uji: (1) plugin wajib `INVENTREE_PLUGINS_ENABLED=True`, sedangkan panduan §4 (pengamanan) mematikan plugin; (2) memasang paket ke kontainer butuh internet dari kontainer (diblokir di sandbox). Karena alatnya membungkus REST API yang sama, penguji menilai dengan data API identik (lihat 00-pembanding bagian A): agent + MCP akan memanggil `list_parts(low_stock=true)` dan `list_stock_items(part=…)` lalu menyusun jawaban sendiri — kualitas akhirnya bergantung pada agent (sama seperti "tanpa skill", minus kerepotan menebak endpoint & token).

| Kriteria (skenario 1) | inventree-mcp resmi | inventree-gudang |
|---|---|---|
| Kelengkapan data baca | **lebih luas** (SO, RO, parameter, tes, lampiran) | cukup untuk gudang |
| Jawaban siap tempel Bahasa Indonesia | tidak (agent menyusun) | ya |
| Saran pesan (min − stok − dipesan − diproduksi) | tidak ada | ada, eksplisit |
| Opname & terima barang | tidak ada (read-only) | ada, dengan pratinjau & pengaman |
| Setup untuk awam | pasang paket di server + aktifkan plugin + klien MCP | tanpa instalasi (Python standar) |
| Sesuai panduan keamanan (plugin mati) | tidak | ya |
| Kualitas rekayasa/tes | sangat baik (CI, codecov, cek hak per alat) | baik (61 uji regresi + uji server asli) |

**Kesimpulan:** untuk target Komunitech (pemilik gudang awam Indonesia, tugas opname/terima barang), **skill unggul**. Kelebihan pesaing yang layak dipelajari (ditulis ulang dengan cara sendiri): cakupan baca lebih luas (mis. riwayat stok per item, sales order) dan penyaringan kemampuan berdasar hak akun sebelum menawarkan aksi. Catatan: bila kelak MCP resmi menambah alat tulis, pembeda utama skill = alur pratinjau/pengaman + lokalisasi.
