# Verifikasi `channels.telegram.streaming.mode = off` (bot uji kedua, 2026-11-04)

Latar: kebocoran kalimat monolog model sebagai pesan Telegram terpisah pada kasir-lokal/absensi-lokal (keputusan 123). Penyelidikan setelan pengiriman (keputusan 124).

## Temuan dokumentasi (OpenClaw 2026.10.2)
- `blockStreaming*` mati secara default dan tidak diatur di bot uji: bukan penyebab.
- Mode pratinjau Telegram default = `progress` (status draft + preamble/komentar model yang diedit lalu dihapus). `streaming.mode: "off"` mematikan pratinjau dan menahan teks progres/perantara; hanya jawaban akhir terkirim.

## Perubahan
Hanya di home bot uji kedua: `channels.telegram.streaming.mode = off` (backup `openclaw.json.bak-202611041532-sebelum-streaming-off`), gateway di-restart per PID. kasir-lokal di bot uji diperbarui ke 1.1.13 (backup folder lama di scratchpad). `produk.csv` fiktif (4 produk, sama dengan bukti uji Oktober) dipasang di workspace bot.

## Hasil (kasir-lokal 1.1.13, Telegram asli, grup uji)
| Gelombang | Topik | Sisi | Balasan bot | Bocor? | Angka |
|---|---|---|---|---|---|
| G30 | 2343/2344 | tanpa / dengan | 2 / 2 | tidak ada, **tetapi TIDAK SAH**: `produk.csv` belum ada di workspace, alur skill tidak jalan | - |
| G30b | 2353 | tanpa skill | 2 | tidak | rekap benar |
| G30b | 2354 | dengan skill | 2 (pratinjau + nota tersimpan) | tidak | total 35.100, kembalian 64.900 benar |
| G30c run 1 | 2363 | dengan skill | 2 | tidak | benar; skill menandai nota sama persis sebagai duplikat (nota N-261105-0001 dari G30b tersimpan di DB uji) |
| G30c run 2 | 2364 | dengan skill | 2 | tidak | sama seperti run 1 |

Pemeriksaan otomatis teks balasan: tidak ada frasa bocor ("identik plus", "Pengguna sudah konfirmasi", "Sekarang tampilkan", "jangan dikutip", "Preview OK").

## Kesimpulan dan batas kepercayaan
- Sebelum perubahan, kebocoran muncul di kedua uji Telegram asli sebelumnya (G28, G29, sisi dengan skill). Sesudah perubahan: 0 dari 3 run sah. Bila peluang bocor sebenarnya ±50 %, peluang 3 run bersih karena kebetulan ±12 %. Bukti **mengarah kuat** tetapi **belum final**; n kecil.
- Run G30c bukan skenario bersih (DB sudah berisi nota yang sama). Untuk penilaian formal, ulangi di DB kosong.
- Belum diuji: absensi-lokal. Belum dinilai formal oleh penilai + pemeriksa kedua; kasir-lokal tetap `beta` sampai itu selesai.
- Implikasi member VIP: OpenClaw member memakai default `progress`; kebocoran bisa terjadi di bot mereka. Usulan: tambahkan saran `streaming.mode: off` di panduan setup (teks saja; bot milik member tidak disentuh).
