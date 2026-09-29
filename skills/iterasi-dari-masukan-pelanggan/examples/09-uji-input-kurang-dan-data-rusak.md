# Uji 09 (input tidak lengkap) - permintaan singkat + berkas rusak/encoding campur
Penguji independen, 2026-09-29.

## A. Percakapan
Pengguna: "tolong olah feedback pelanggan toko roti saya ya: 1) rotinya keras bgt 2) enak tp kemanisan 3) kurirnya lama 4) mantul 5) harga naik"
Perilaku sesuai SKILL.md (Kapan TIDAK / Input): data < 8 masukan -> baca langsung, tanpa statistik; tidak perlu bertanya karena data sudah ada.
Jawaban yang diharapkan & dinilai penguji: 3 temuan (tekstur keras, terlalu manis, pengiriman lama) + 2 tindakan + catatan "data < 8, tanpa persentase"
+ saran kumpulkan ekspor WA/ulasan bulan depan. SKILL.md dan `examples/04` memberi arahan yang jelas untuk ini. **Lulus.**
Bila tanpa data sama sekali: SKILL.md meminta sekali (kanal, periode, jenis usaha) - sesuai prinsip "tanya sekali".

## B. Berkas rusak (script dijalankan sungguhan)
| Masukan | Hasil | Nilai |
|---|---|---|
| file kosong / hanya spasi | "Tidak ada masukan yang bisa dibaca..." exit 2 | Baik |
| CSV tanpa kolom teks (nama,hp) | "Kolom teks tidak ketemu. Kolom yang ada: ..." exit 1 | Baik |
| file tidak ada | **Traceback** FileNotFoundError, exit 1 | Perlu pesan jelas |
| file biner bernama .csv | **Traceback** `_csv.Error`, exit 1 | Perlu pesan jelas |
| `--tema` JSON rusak | **Traceback** JSONDecodeError | Perlu pesan jelas |
| teks **UTF-16** (ekspor "Unicode Text" Excel/Notepad) | exit 0, 2 "masukan" berisi `ÿþk\x00a\x00k...` - **sampah diam-diam** | Buruk |
| CSV tanda kutip tidak tertutup | 2 baris tergabung jadi 1 masukan "rotinya gosong,1 enak,5", dihitung keluhan+pujian rasa | Diam-diam salah |
| CSV cp1252 (“parah”, é) | terbaca; karakter ganjil jadi "é"/dihapus | Baik |
| WA UTF-8 dengan satu baris cp1252 | seluruh file jatuh ke latin-1: aman untuk teks ASCII, tetapi emoji/huruf UTF-8 lain akan rusak (mojibake) | Cukup |
| WA format AS (`9/29/26, 2:05 PM`) | terbaca sebagai WA, bulan tidak valid -> "tanpa tanggal" (sesuai batasan yang ditulis) | Baik |
| 5 baris dengan 3x "roti enak" (3 pelanggan) | "duplikat 2" -> 3 masukan saja; pujian rasa 1, bukan 3 | Menyesatkan |

## C. Penyamaran (fungsi `samarkan`)
Lolos (bocor): "kak rina" (huruf kecil), "Saya Budi", "a.n. Siti", telepon rumah "021 555 1234", "Perum Griya Asri Blok C2 No 5", plat "B 1234 XYZ",
"mba [nama] Lestari" (nama belakang tertinggal), "Pak RT Joko". Tersamar: HP, NIK/rekening (sebagai [nomor]), wa.me, "Jalan Sudirman...".
SKILL.md sudah jujur bahwa penyamaran tidak sempurna dan mewajibkan baca ulang kutipan; tetap perlu diperkuat.

## Nilai skenario: 6/10
