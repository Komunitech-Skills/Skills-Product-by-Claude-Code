# Uji pembuat kas-umkm v1.0.1 (26 September 2026)

> Catatan **pembuat** atas revisi pemeliharaan berdasarkan temuan penguji independen Akun B
> (`examples/HASIL-UJI.md`, skor 8/10). Bukan uji independen — temuan 1–2 perlu diuji ulang oleh penguji terpisah.

## Perubahan
| Temuan | Perbaikan v1.0.1 |
|---|---|
| 1 [SEDANG] `impor --ya` menyimpan baris belum jelas sebagai "lain-lain" (tarik tunai ATM jadi beban) | Kategori sistem baru **`perlu-dicek`** ("Perlu dicek (belum digolongkan)"): ikut saldo akun (saldo bank tetap cocok dengan mutasi) tetapi **tidak** dihitung di hasil usaha. `rekap` menampilkan "BELUM DIGOLONGKAN" + ID; `ekspor --format emkm` ditolak sampai digolongkan (`perlu_dicek`: daftar ID); `ekspor --format arus-kas` melewatinya dengan catatan; `daftar --kategori "perlu dicek"`. Perintah baru `golongkan --id N[,M] --kategori <kategori>|pindah:<akun>` (pratinjau → `--ya`, tercatat di log). `--kategori-default` tetap bisa dipakai sebagai pilihan eksplisit pengguna. |
| 1 — aturan pindah dana | `kenali_pindah`: tarik tunai ATM (rekening/e-wallet KELUAR → satu-satunya akun tunai atau akun tunai yang disebut), setor tunai (akun tunai → rekening, atau rekening MASUK dari akun tunai), pindah buku / antar rekening sendiri / top up yang **menyebut nama akun pasangan** → `pindah` otomatis, ditampilkan "DIKENALI SEBAGAI PINDAH DANA" (`pindah_dikenali`) dengan saran `--tetapkan N=prive` bila uang dipakai pribadi. Pasangan tidak pasti (akun tunai lebih dari satu, nama akun tidak disebut, arah janggal, tanggal sebelum saldo awal akun pasangan) → `perlu-dicek`. Baris biaya ("BIAYA TARIK TUNAI ATM BERSAMA") tetap pengeluaran lain-lain (kamus biaya bank ditambah). `catat` tanpa kategori dengan catatan "tarik tunai/setor tunai/pindah buku/top up" ditolak dengan arahan `kas.py pindah`; dengan kategori usaha diberi peringatan. |
| 2 [SEDANG] tidak ada larangan pembukuan ganda | SKILL.md: baris "Kapan TIDAK digunakan" + **Aturan 7** jawaban penolakan baku (dua versi buku/omzet dikecilkan/hapus catatan, termasuk database kedua) dengan dasar UU KUP Pasal 28 ayat (3) dan Pasal 39 ayat (1) huruf d & f, plus alternatif sah (`pph-final-umkm`, omzet s.d. Rp 500 juta tidak dikenai pajak untuk orang pribadi, konsultan). |
| 6 [KOSMETIK] ResourceWarning di tes | `open()` di tes impor-kasir asli memakai `with`. |

Dasar hukum dicek 26-09-2026 dari naskah UU 28/2007 (perubahan ketiga UU KUP): Pasal 28 ayat (3) "Pembukuan atau pencatatan tersebut harus diselenggarakan dengan memperhatikan iktikad baik dan mencerminkan keadaan atau kegiatan usaha yang sebenarnya"; Pasal 39 ayat (1) huruf d (SPT/keterangan isinya tidak benar) dan huruf f (memperlihatkan pembukuan yang palsu/tidak menggambarkan keadaan sebenarnya). Sumber: https://learning.hukumonline.com/wp-content/uploads/2021/07/UU-No.-28-Tahun-2007.pdf (salinan naskah; naskah resmi juga di JDIH Kemenkeu).

## Otomatis: `python3 tests/uji_regresi.py` → 65 tes lulus (59 lama + 6 baru, Python 3.11 Linux)
- Dua tes lama disesuaikan dengan perilaku baru: "Sumbangan 17an" kini `perlu-dicek` (bukan lain-lain); "TARIKAN ATM" kini otomatis pindah dana ke Laci kas (bukan perlu dicek).
- Tes baru `UjiV101`: mutasi berisi tarik tunai/setor tunai/top up GoPay/pindah buku tanpa nama akun/sumbangan/biaya tarik tunai → kategori, pasangan akun, saldo 3 akun, hasil usaha 742.500 (tarik/setor/top up/perlu dicek tidak ikut), ekspor emkm ditolak lalu lolos setelah `golongkan` (pindah:GoPay & lain-lain), catatan pindah tidak bisa digolongkan ulang; `--tetapkan` mengalahkan aturan pindah; akun tunai ganda → perlu dicek kecuali disebut ("KE BRANKAS"); baris tanpa kategori tidak mengurangi hasil usaha tetapi saldo laci tetap benar, `--kategori-default` eksplisit; `catat` tarik tunai diarahkan ke `pindah`; SKILL.md memuat penolakan pembukuan ganda.

## Belum dikerjakan
Temuan RENDAH 3–5 (prive bulanan di ekspor arus kas, kamus prive "rumah", pesan argparse `--keluar -20rb`) dan catatan 7 (sintaks `openclaw automations`).
