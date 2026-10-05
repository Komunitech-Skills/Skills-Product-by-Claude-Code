# Rincian cek ambang & konfigurasi (dipindah dari SKILL.md v1.0.9)

**Baca file ini hanya bila:** pengguna mengubah format `PANTAU.md` yang tidak biasa, memakai
harga acuan/sumber Indodax, menanyakan arti exit code/anti-spam, `cek_ambang.py` mengeluarkan
error konfigurasi yang tidak jelas, atau Python tidak bisa dijalankan. Untuk memasang alert
biasa, contoh di SKILL.md Langkah A sudah cukup.

## 1. Daftar pantau `kripto/PANTAU.md` (ditulis/diubah oleh member)
Format lihat `templates/PANTAU.md`. Tabel:

| Koin | Ambang naik | Ambang turun | Harga acuan | Kata kunci berita | Jam ringkasan pagi |
|---|---|---|---|---|---|
| BTC | 8% | 5% | (kosong = pakai 24 jam terakhir) | bitcoin, ETF, halving | 07:00 WIB |

- **Ambang naik/turun**: persen perubahan. "Harga acuan" kosong → dihitung dari perubahan
  24 jam (data bawaan sumber). Diisi (mis. harga beli member) → dihitung dari acuan itu dan
  tetap sampai member mengubahnya sendiri. Boleh juga harga absolut, mis. "di atas Rp 1,6 M".
- **Kata kunci berita**: ditambahkan ke `ambil_berita.py` sebagai `KODE:kata1,kata2`.
- **Jam ringkasan pagi**: default 07:00 WIB bila kosong (sebutkan asumsinya).
- **Ambang hanya dari pengguna** -- angka ambang = sinyal, jadi tidak pernah diisi agent
  (juga bukan "default teknis"). Koin tanpa ambang → `"tanpa_ambang": true` (hanya harga).

Pertanyaan sekali jalan (bernomor, maks 5) bila belum ada `PANTAU.md`: koin apa; naik/turun
berapa persen atau di harga berapa; harga acuan sendiri atau 24 jam; kata kunci berita; jam &
kanal ringkasan pagi.

## 2. Field `konfigurasi.json` (`cek_ambang.py --help` / docstring)
Satu objek per koin di `{"koin": [...]}`:
- `kode` (wajib), `mata_uang` (wajib: `idr`/`usd`), `coingecko_id` (id resmi CoinGecko, mis.
  `bitcoin`, `ethereum`, `solana`; cek di URL halaman koin coingecko.com).
- opsional `indodax_pair` (mis. `btcidr`) + `sumber: "indodax"` untuk harga lokal Rupiah --
  Indodax tidak memberi % 24 jam, jadi ambang persen dengan sumber Indodax butuh `harga_acuan`.
- ambang: `ambang_naik_persen`, `ambang_turun_persen`, `ambang_harga_di_atas`,
  `ambang_harga_di_bawah`; opsional `harga_acuan`. Angka boleh teks format Indonesia
  (`"5%"`, `"1.450.000.000"`). Semua > 0.
- `"tanpa_ambang": true` untuk koin yang hanya ditampilkan harganya (tidak boleh bersama ambang).

`--konfigurasi` menerima path file ATAU teks JSON langsung (diawali `{`) -- dipakai untuk
pratinjau sebelum file ditulis. `--state` opsional saat `--pratinjau`.

## 3. Membaca hasil `cek_ambang.py`
- `pesan_singkat` sudah siap kirim (sumber, jam data, peringatan data basi, status tiap ambang,
  disclaimer). `--keluaran teks` mencetak hanya teks itu.
- `status_ambang` per koin: **SUDAH TERLEWATI** atau "belum terlewati" + jarak ke ambang. Bila
  SUDAH TERLEWATI saat alert baru dipasang, katakan di awal balasan: notifikasi pertama akan
  langsung terpicu.
- `perlu_lapor_sekarang: true` → itu yang dikirim sebagai notifikasi.
- `ada_koin_gagal_total: true` → sebutkan koin yang gagal diambil; jangan menyimpulkan "tidak
  ada ambang terlewati" bila sebagian koin TIDAK BISA dicek.

## 4. Anti-spam & state
`cek_ambang.py` (tanpa `--pratinjau`) menyimpan status "sudah dilaporkan" **per jenis ambang**
(naik/turun/di atas/di bawah) di `kripto/state.json`. Ambang yang masih terlewati tetapi belum
berubah diredam sampai `--jeda-ulang-jam` (default 6 jam) habis atau kondisinya pulih lalu
terpicu lagi. `ambang_terlewati` selalu fakta apa adanya; `perlu_lapor` yang membedakan
"baru" dari "sudah dilaporkan". "Pemantauan buta" (gagal total, cache lebih tua dari
`--usia-basi-jam`, ambang % tak bisa dievaluasi) punya anti-spam yang sama: dilaporkan sekali
saat terjadi, diredam, lalu dilaporkan sekali saat PULIH (`pemantauan_bermasalah`,
`perlu_lapor_pemantauan`, `pemantauan_pulih`).

**Pratinjau wajib saat memasang/mengubah alert** (`--pratinjau`, alias `--tanpa-simpan`): state
tidak ditulis, exit 0. Menjalankan perintah tanpa opsi itu dengan state asli mencatat ambang
"sudah dilaporkan" dan jadwal pertama diredam 6 jam. Hanya jadwal otomatis & cek rutin yang
memakai perintah tanpa `--pratinjau`.

## 5. Exit code
`0` = tidak ada yang perlu dilaporkan sekarang · `2` = ada ambang HARGA perlu dilaporkan ·
`3` = ada "pemantauan buta" perlu dilaporkan (baru terjadi/baru pulih) · `1` = error
input/konfigurasi. `scripts/cek_dan_lapor.py` menerjemahkannya menjadi pesan siap kirim atau
`NO_REPLY` dan selalu keluar 0 (untuk jadwal, lihat `openclaw-jadwal.md`).

## 6. Uji offline, sumber gagal, Python tidak bisa jalan
- Uji tanpa jaringan: `--harga-file <file>` (format di docstring script).
- Sumber gagal: dipakai cache terakhir dengan peringatan + jam datanya; tanpa cache → koin
  "gagal_total" tanpa angka. Selalu tunjukkan status ini ke member.
- Python tidak bisa dijalankan: persen = (harga sekarang − harga acuan) / harga acuan × 100,
  bandingkan ke ambang, dan sebut "belum diverifikasi script".
- Sumber data & contoh respons nyata: `sumber-data.md`.
