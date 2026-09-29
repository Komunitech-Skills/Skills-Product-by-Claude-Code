# Uji 04 — Input tidak lengkap: token belum disimpan, URL belum diatur (+ pesan galat)

**Permintaan:** "Cek stok menipis di InvenTree saya" — pengguna baru selesai memasang, belum menjalankan `simpan-kunci`, InvenTree-nya di port lain.

| Kondisi | Output skill (asli) | Kode | Penilaian |
|---|---|---|---|
| Tanpa file kunci (HOME kosong), `cek` & `stok-menipis` | `GALAT: File kunci (file kunci default) tidak ditemukan: .../.komunitech/inventree-kunci.txt. Jalankan dulu 'python3 inventree.py simpan-kunci' (lihat docs/panduan-inventree.md bagian 6).` | 3 | ✔ Indonesia, langkah jelas. Agent memandu pengguna menjalankan `simpan-kunci` SENDIRI di terminal (SKILL.md §Persiapan 2) — tidak meminta token di chat |
| URL tidak diatur, InvenTree di `127.0.0.1:8000` (tidak ada) | `GALAT: Tidak bisa menghubungi InvenTree di http://127.0.0.1:8000 (<urlopen error [Errno 111] Connection refused>). Pastikan InvenTree menyala (panduan bagian 3/7) dan alamatnya benar (ENV INVENTREE_API_HOST atau --url).` | 4 | ✔ |
| Token salah (401, server asli) | `GALAT: 401 dari InvenTree: token salah, kedaluwarsa, atau sudah dicabut (pesan server: Invalid token.). Buat token baru ... 'simpan-kunci --ya'.` | 5 | ✔ |
| Token baca-saja mencoba opname (403, server asli) | lihat Uji 02 | 5 | ✔ |
| Barang/PO tidak ada (404, server asli) `stok "#999"`, `--po "#99"` | `GALAT: 404: tidak ditemukan di InvenTree (/part/999/). Periksa id/kode ... No Part matches the given query.` | 4 | ✔ (pesan server Inggris ikut, wajar) |
| Timeout (soket yang tidak menjawab, `--timeout 3`) | `GALAT: Tidak bisa menghubungi InvenTree di http://127.0.0.1:8765 (timed out). ...` | 4 | ✔ |
| Server app mati, proxy Caddy hidup (502) | `GALAT: InvenTree membalas galat server (502). Coba lagi sebentar; bila terus, cek log InvenTree.` | 4 | ✔ (saran: sebut `docker compose ps`) |
| Semua kontainer mati | `Tidak bisa menghubungi InvenTree di http://localhost (... Connection refused)` ; `cek` menulis `TIDAK BISA DIHUBUNGI` | 4 | ✔ |
| 500 **saat menulis** (proxy lokal yang meneruskan GET ke InvenTree asli, POST dibalas 500) | `GALAT: InvenTree membalas galat server (500) saat MENULIS. Data MUNGKIN sudah masuk sebagian. JANGAN ulangi otomatis - cek dulu di layar InvenTree.` | 8 | ✔ |
| Koneksi diputus **saat menulis** | `GALAT: Koneksi ke InvenTree terputus/timeout saat MENULIS (...). Hasilnya TIDAK PASTI ... JANGAN ulangi otomatis` | 8 | ✔ ; PO tidak berubah (12/20/0/1) |

Jawaban agent (simulasi) untuk kasus utama:
> InvenTree Anda belum tersambung ke saya karena token API belum disimpan. Satu langkah saja, jalankan **sendiri** di terminal (bukan di chat): `python3 ~/.openclaw/skills/inventree-gudang/scripts/inventree.py simpan-kunci`, lalu tempel token dari *User Settings → Security → Access Tokens* (panduan §6). Kalau InvenTree Anda bukan di `http://localhost`, beri tahu alamatnya (mis. `http://localhost:8080`).

**Hasil: LULUS.**
