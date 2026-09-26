# Skenario 07 — Uji v1.1.0: alat ke-5 crm-wa (bagian PROSPEK)

**Penguji:** agent penguji independen (simulasi, Claude Code). Bukan pembuat skill `laporan-harian-usaha` maupun `crm-wa`. Tanggal uji 2026-09-25 (data berpusat pada "hari ini" simulasi 2026-09-24). Semua nama, nomor WA, dan nilai rupiah **fiktif**.

## Lingkungan
- `laporan-harian-usaha`, `crm-wa`, dan `kasir-lokal` **disalin** ke `<scratchpad>/uji-lhu110/skills/` (folder datar, seperti terpasang di komputer pembeli). Tidak ada yang dipasang di `.claude/skills` repo asli; `~/KomunitechData` asli tidak disentuh.
- `HOME` & `KOMUNITECH_DATA` diarahkan ke folder sementara sendiri. `TZ` tidak diset khusus (laporan memakai `--sekarang`/`--tz` eksplisit, bukan jam sistem).
- Data CRM dibuat sendiri lewat **script resmi** `crm.py` (bukan ditulis tangan ke SQLite): 11 kontak, sumber Instagram/TikTok/Referensi, tersebar 2026-09-07 s.d. 2026-09-24 (± 2,5 minggu), mencakup: beberapa prospek terlambat follow-up, satu order (tahap deal) yang jadwal konfirmasinya sudah lewat, dua kontak batal, dan tiga deal — termasuk deal dari lead **lama** (masuk beberapa hari sebelum tanggal deal-nya). Data kasir-lokal minimal (1 nota, Rp 24.000) hanya untuk memastikan alat ke-5 tidak mengganggu alat lain saat berjalan bersamaan.
- Database asli tidak pernah ditulis oleh `laporan.py` (dibuka `mode=ro` + `VACUUM INTO` ke snapshot sementara), sama seperti 4 alat sebelumnya.

## 1. Data uji (dibuat dengan `crm.py`, semua `--hari-ini 2026-09-24`)

| Kode | Nama (fiktif) | Sumber | Masuk | Tahap saat ini | Follow-up | Nilai |
|---|---|---|---|---|---|---|
| K0001 | Ibu Wulan | Instagram | 2026-09-10 | ditawar | 2026-09-14 (**terlambat 10 hr**) | Rp 2.800.000 |
| K0002 | Pak Joko | TikTok | 2026-09-13 | dihubungi | 2026-09-23 (**terlambat 1 hr**) | - |
| K0003 | Bu Nita | Referensi | 2026-09-15 | **deal** (tgl deal 2026-09-24) | 2026-09-26 | Rp 3.200.000 |
| K0004 | Mas Rian | Instagram | 2026-09-24 (hari ini) | baru | 2026-09-24 (hari ini) | - |
| K0005 | Bu Siti | TikTok | 2026-09-20 | **deal** (tgl deal 2026-09-22) | 2026-09-26 | Rp 1.500.000 |
| K0006 | Bu Endah | Referensi | 2026-09-08 | batal (2026-09-10, "belum ada dana") | - | - |
| K0007 | Bu Yuli | Referensi | 2026-09-19 | **deal** (tgl deal 2026-09-21) | 2026-09-23 (**order lewat jadwal**) | Rp 900.000 |
| K0008 | Mbak Fira | Instagram | 2026-09-22 | dihubungi | 2026-09-25 (besok) | - |
| K0009 | Pak Dedi | TikTok | 2026-09-23 | baru | 2026-09-24 (hari ini) | - |
| K0010 | Ibu Ratna | Referensi | 2026-09-07 | dihubungi | 2026-09-26 | - |
| K0011 | Pak Agus | Instagram | 2026-09-09 | batal (2026-09-12, "tidak ada respon") | - | - |

Perintah pembuatan data (ringkas, lengkap di riwayat sesi): `crm.py init ...`, 11× `crm.py tambah ...` dengan `--masuk`/`--followup` eksplisit, lalu `crm.py catat --kontak ... --tahap batal/deal ...` untuk K0006/K0011 (batal) dan K0003/K0005/K0007 (deal).

## 2. Angka PROSPEK vs `crm.py rekap --json` langsung vs hitung ulang SQLite independen

Tiga sumber dibandingkan untuk **setiap** angka: (a) `laporan.py --json` bagian `prospek`, (b) `crm.py rekap --dari <periode> --sampai <periode> --hari-ini 2026-09-24 --json` dijalankan langsung, (c) query SQLite `mode=ro` + perhitungan Python independen (tidak memanggil kode `crm.py` maupun `laporan.py`) terhadap tabel `kontak` mentah.

### Harian 2026-09-24
| Angka | laporan.py | crm.py rekap | Hitung ulang SQL independen | Cocok |
|---|---|---|---|---|
| lead_masuk | 1 | 1 | 1 (hanya Mas Rian, masuk 24/9) | ✅ |
| deal.jumlah / nilai | 1 / Rp 3.200.000 | 1 / Rp 3.200.000 | 1 / Rp 3.200.000 (Bu Nita, tgl_deal 24/9) | ✅ |
| kohort (lead/deal/batal/berjalan) | 1/0/0/1 | 1/0/0/1 | 1/0/0/1 | ✅ |
| konversi_teks | "0,0%" | "0,0%" | 0/1 = 0,0% | ✅ |
| followup terlambat/hari ini/besok/order | 2/2/1/1 | 2/2/1/1 | terlambat={Ibu Wulan, Pak Joko}, hari ini={Mas Rian, Pak Dedi}, besok={Mbak Fira}, order={Bu Yuli} → 2/2/1/1 | ✅ |
| nilai_terlambat_dan_hari_ini | Rp 2.800.000 | Rp 2.800.000 | hanya Ibu Wulan bernilai & terbuka = Rp 2.800.000 | ✅ |
| sumber_terbaik | null | null | kohort hari ini cuma Mas Rian (Instagram, belum deal) → belum ada terbaik | ✅ |

**0 beda** pada seluruh angka harian, di tiga sumber independen.

### Mingguan 2026-09-14 s.d. 2026-09-20 (banding 2026-09-07 s.d. 2026-09-13)
| Angka | laporan.py | crm.py rekap | Hitung ulang SQL independen | Cocok |
|---|---|---|---|---|
| lead_masuk | 3 | 3 | Bu Nita(15), Bu Yuli(19), Bu Siti(20) = 3 | ✅ |
| deal.jumlah / nilai | 0 / Rp 0 | 0 / Rp 0 | tgl_deal ketiganya (24, 21, 22) **di luar** jendela 14–20 → 0 | ✅ |
| kohort (lead/deal/batal/berjalan) | 3/3/0/0 | 3/3/0/0 | ketiganya kini bertahap "deal" (status SAAT INI, bukan terikat tanggal) → 3/3 | ✅ |
| konversi_teks | "100,0%" | "100,0%" | 3/3 = 100,0% | ✅ |
| sumber_terbaik | Referensi, 2 lead, 2 deal, sampel kecil | idem | Referensi: Bu Nita+Bu Yuli, nilai_deal 4.100.000 > TikTok 1.500.000 | ✅ |
| banding lead_masuk minggu sebelumnya | 5, "turun 40,0%" | 5 (dihitung terpisah) | 07–13/9: Bu Endah, Ibu Wulan, Pak Agus, Ibu Ratna, Pak Joko = 5; (3−5)/5×100=−40,0% | ✅ |
| followup (sama seperti harian, tidak terikat periode) | 2/2/1/1, Rp 2.800.000 | idem | idem | ✅ |

**0 beda** pada seluruh angka mingguan, termasuk pembanding.

Kesimpulan bagian ini: klaim di deskripsi perubahan ("angka PROSPEK diambil apa adanya dari `crm.py rekap --json`, tidak dihitung ulang") **terbukti** — tidak ditemukan satu pun selisih di 15 angka × 2 periode × 3 sumber.

## 3. Kejelasan untuk pemilik awam — cacat ditemukan (lihat juga bagian 6)

Reproduksi persis contoh dari pembuat, dengan data independen:

```
PROSPEK
...
Deal periode ini: 1 senilai Rp 3.200.000
Konversi: 0,0% (0 dari 1 lead)
Sumber lead terbaik: belum ada deal dari lead periode ini.
```

Ditemukan kasus **lebih ekstrem** di skenario mingguan yang sama (lihat teks lengkap di bagian 2):

```
PROSPEK
Prospek baru: 3
...
Deal periode ini: 0 senilai Rp 0
Konversi: 100,0% (3 dari 3 lead)
```

Untuk pemilik awam, "0 deal" langsung diikuti "konversi 100%, 3 dari 3 lead" terbaca sebagai **kontradiksi**, bukan sekadar kurang jelas — berlawanan arah dengan contoh pembuat (deal ada tapi konversi 0%), tapi sumber masalahnya **sama persis**: "Deal periode ini" dihitung dari **tanggal closing** (`tgl_deal` di dalam periode), sedangkan "Konversi" dihitung dari **tanggal lead masuk** (`tgl_masuk` di dalam periode) — dua populasi kontak yang bisa berbeda. Di skenario mingguan ini, ketiga lead masuk minggu 14–20/9, tapi ketiganya baru closing di tanggal 21/22/24/9 (minggu berikutnya) — jadi "Deal baru periode ini" = 0 (tidak ada yang closing DI DALAM 14–20/9), sementara "Konversi" = 3 dari 3 (ketiganya SUDAH deal per hari ini, terlepas kapan closing-nya).

**Baris "Konversi: ... (Y dari Z lead)" tidak menjelaskan bahwa Z (lead) dan angka deal di baris atasnya bisa berasal dari periode/hitungan yang berbeda.** Diperiksa lebih lanjut:
- `SKILL.md:104-111` memuat contoh keluaran dengan pola yang sama (1 deal / 0% konversi) tapi bagian "Aturan hitung" (`SKILL.md:127`) hanya menjelaskan nuansa follow-up (terlambat/hari ini dihitung per hari ini, bukan per periode) — **tidak** menjelaskan beda basis tanggal deal vs konversi. Agent yang membaca SKILL.md pun tidak mendapat bekal untuk menjelaskan ke pengguna.
- `crm.py` sendiri (di balik layar) **kadang** menambahkan catatan peredam pada teks lengkapnya: *"Catatan: periode ini masih baru; konversi akan naik bila lead yang masih berjalan jadi deal."* — tapi catatan itu hanya muncul bila `masih_berjalan > 0`. Pada skenario mingguan di atas, `masih_berjalan = 0` (ketiganya sudah closing), jadi catatan itu **tidak muncul** bahkan di `crm.py rekap` sendiri — dan `laporan.py` tidak meneruskan/menulis ulang catatan itu maupun catatan penggantinya sama sekali di bagian PROSPEK (dicek: kata "masih baru"/"berjalan" tidak ada satu pun di `teks_laporan()` bagian PROSPEK).

**Kesimpulan:** ini cacat kejelasan yang nyata (bukan sekadar gaya penulisan) karena bisa dibaca sebagai laporan yang salah/kontradiktif oleh pengguna awam, dan bisa muncul di **kedua arah** (deal tinggi+konversi rendah, atau deal nol+konversi tinggi). Akar masalah ada di semantik `crm-wa` sendiri (kohort `tgl_masuk` vs `deal_baru` `tgl_deal`) yang memang sengaja diambil apa adanya oleh `laporan-harian-usaha` (sesuai desain "tidak dihitung ulang") — tapi teks pendek PROSPEK tidak mewarisi penjelasan/catatan yang kadang ada di `crm.py rekap` versi lengkap. Lihat cacat **S2** di bagian 6.

## 4. Privasi

- Grep nama, sapaan+nama, dan 8 nomor WA fiktif (`0813-1000-000X`) serta kode kontak (`K0001`…`K0011`) pada **seluruh** keluaran (teks harian, JSON harian, teks mingguan, JSON mingguan, JSON `--samarkan`): **0 kecocokan**.
- `--samarkan`: dijalankan berdampingan dengan tanpa `--samarkan` — bagian `prospek` **identik** (rekap `crm-wa` sendiri sudah tanpa nama/nomor per kontrak `skema_json 1`, jadi `--samarkan` memang tidak mengubah bagian ini; diverifikasi bukan berarti diabaikan diam-diam — tidak ada data nama yang bisa bocor di bagian ini untuk disamarkan).
- Catatan rendah (bukan kebocoran aktual, lihat N-baru di bagian 6): `ambil_crm()` di `laporan.py` tidak meneruskan flag `--samarkan` ke pemanggilan `crm.py rekap`. Saat ini tidak berdampak karena `rekap --json` tidak pernah memuat nama/alasan bebas yang dipakai `laporan.py`; hanya perlu diperhatikan bila kontrak `crm.py rekap` berubah di masa depan.
- DB CRM asli **tidak berubah**: `sha256sum data/crm/crm.db` sebelum = sesudah menjalankan `laporan.py` (harian, mingguan, `--samarkan`, dan seluruh skenario di bagian 5) berkali-kali:
  ```
  1885fb57274c072f53ff60c7f11741184de3dd22c32e4208dfe4561a6b8042bf  data/crm/crm.db   (sebelum)
  1885fb57274c072f53ff60c7f11741184de3dd22c32e4208dfe4561a6b8042bf  data/crm/crm.db   (sesudah)
  ```

## 5. Ketahanan (crm-wa tidak ada / rusak / terkunci) & opsi lokasi

| Kasus | Cara | Hasil |
|---|---|---|
| crm-wa tidak pernah dipakai (folder `data/crm` dihapus) | hapus folder | `alat.crm.status = "tidak_ada"`, `prospek = null`, teks: "Belum ada data dari alat mana pun..." bila semua alat kosong, atau baris "Belum ada data (crm-wa belum dipakai...)" di bagian PROSPEK bila alat lain ada. **Tidak error.** |
| DB CRM rusak (bukan file SQLite) | `crm.db` ditimpa teks acak | `status = "gagal"`, pesan "file bukan database atau rusak...", `prospek = null`, PROSPEK: "Belum ada data: crm-wa tidak terbaca (lihat Perlu Perhatian)", dan `PERLU PERHATIAN` memuat "crm-wa tidak terbaca: ...". **Tidak error, tidak crash.** |
| DB CRM terkunci (koneksi lain `BEGIN EXCLUSIVE` 6 detik, `--timeout 3`) | koneksi tulis paralel | `status = "gagal"`, pesan "database sedang dipakai program lain lebih dari 3 detik... Data aman", muncul juga di `PERLU PERHATIAN`. **Tidak menggantung** (selesai < 4 detik, bukan menunggu 6 detik penuh atau macet). |
| `--tanpa crm` | opsi eksplisit | `status = "dilewati"`, `prospek = null`. |
| `--crm-db <path lain>` | DB disalin ke folder lain di luar `KOMUNITECH_DATA` | Terbaca, angka identik (lead_masuk=1 utk harian). |
| `--crm-script <path lain>` | salinan `crm.py` di folder custom | Terbaca & dipakai, `alat.crm.script` menunjuk ke path custom itu. |

Semua kasus di atas: exit code 0 (laporan tetap dibuat), tidak ada crash, tidak ada macet/hang, dan tidak menyentuh data lain.

## 6. Regresi (bagian selain PROSPEK)

- `tests/uji_regresi.py` (bawaan skill) → **47 tes OK**, termasuk 8 tes khusus crm-wa milik pembuat (`test_crm_prospek_cocok_dengan_rekap_langsung`, `test_crm_mingguan_banding_minggu_sebelumnya`, `test_crm_tidak_terpasang_bukan_error`, `test_crm_db_rusak_dilewati_dengan_catatan`, `test_crm_script_tidak_ditemukan`, `test_tanpa_crm`, `test_crm_tanpa_nama_nomor_prospek`, `test_crm_db_asli_tidak_berubah`) — dijalankan ulang di lingkungan penguji, bukan dijadikan satu-satunya dasar penilaian (data & skenario tambahan pada bagian 1–5 dibuat independen oleh penguji).
- `python3 scripts/validate.py` (dari `/home/user/Skills`) → **58 skill valid, 58 baris katalog sesuai**.
- `bash scripts/uji_openclaw.sh` (dari `/home/user/Skills`) → OpenClaw **2026.9.6**: 58/58 `eligible`/`modelVisible`/`commandVisible`.
- Uji gabungan (kasir-lokal minimal + crm-wa bersamaan, di luar suite bawaan): laporan harian dengan 1 nota kasir (Rp 24.000) **dan** data CRM di atas — bagian PENJUALAN tetap benar (Rp 24.000, 1 nota) dan bagian PROSPEK tetap sama persis dengan uji crm-wa sendirian; footer "Sumber: kasir-lokal, crm-wa (hanya dibaca)." muncul benar. Tidak ada interferensi antar alat.

## 7. Uji jadwal OpenClaw sungguhan (bukan simulasi)

Dijalankan dengan OpenClaw **2026.9.6** nyata (bukan simulasi), `HOME=/tmp/uji-openclaw/home`, `gateway run --dev --allow-unconfigured --bind loopback`:

1. `openclaw skills check --json` → `laporan-harian-usaha`, `crm-wa`, `kasir-lokal` semuanya di `eligible`, `modelVisible`, `commandVisible`.
2. `openclaw automations add --cron "0 21 * * *" --tz Asia/Jakarta --command-argv [...laporan.py...] --command-env "KOMUNITECH_DATA=<data uji>"` → `nextRunAtMs` = 2026-09-25 14:00:00 UTC = **21:00 WIB** (benar).
3. `openclaw automations run <id> --wait` → `status: "ok"`, exit code 0, **`summary` memuat teks PROSPEK lengkap** persis sama dengan uji terminal langsung (termasuk "Deal periode ini: 1 senilai Rp 3.200.000" / "Konversi: 0,0% (0 dari 1 lead)"). `completionStatus: "failed"` hanya karena pengiriman channel Telegram belum dikonfigurasi (`Channel is required...`) — sesuai peringatan yang **sudah ditulis sendiri** oleh pembuat di `references/openclaw-jadwal.md` ("Pesan sampai di Telegram belum diuji"), bukan regresi baru.
4. Jadwal mingguan `--cron "0 7 * * 1"` → `nextRunAtMs` = 2026-09-28 00:00:00 UTC = **Senin 07:00 WIB** (benar). `automations run --wait` untuk jadwal ini juga memuat teks PROSPEK mingguan lengkap di `summary` (termasuk skenario "Deal periode ini: 0 / Konversi 100%" pada bagian 3).
5. Kedua automation dihapus (`automations rm`) dan gateway dihentikan setelah uji.

**Ini menutup catatan "belum diuji ulang lewat `automations run` sungguhan" yang pembuat tulis sendiri di `references/openclaw-jadwal.md` untuk bagian PROSPEK** — sudah diuji, dan lulus (teks PROSPEK muncul benar di `summary` lewat Gateway asli, bukan hanya lewat pemanggilan `python3 laporan.py` langsung).

## 8. Ringkasan cacat baru di v1.1.0

| ID | Keparahan | Lokasi | Temuan & reproduksi |
|---|---|---|---|
| **S2** | **Sedang** | `scripts/laporan.py` bagian `teks_laporan()` PROSPEK (baris "Deal periode ini" & "Konversi"); akar semantik di `crm-wa scripts/crm.py:hitung_rekap` (`deal_baru` per `tgl_deal` vs `kohort` per `tgl_masuk`) | "Deal periode ini" dan "Konversi (Y dari Z lead)" bisa berasal dari populasi kontak yang berbeda & terbaca kontradiktif oleh pemilik awam. Reproduksi ringan (persis contoh pembuat): data bagian 1 → harian 24/9 → "Deal periode ini: 1 senilai Rp 3.200.000" + "Konversi: 0,0% (0 dari 1 lead)". Reproduksi kuat (arah sebaliknya, lebih membingungkan): data yang sama → mingguan 14–20/9 → "Deal periode ini: **0** senilai Rp 0" + "Konversi: **100,0%** (3 dari 3 lead)". Tidak dijelaskan di teks, tidak dijelaskan di `SKILL.md` "Aturan hitung", dan catatan peredam yang kadang ada di `crm.py rekap` sendiri ("periode ini masih baru...") tidak diteruskan `laporan.py` serta tidak muncul sama sekali bila `masih_berjalan = 0`. Saran (tidak diimplementasikan oleh penguji): tambah satu baris penjelas tetap, mis. "(Deal dihitung dari tanggal closing; Konversi dari tanggal lead masuk — bisa beda periode)", atau ganti label jadi "Deal closing periode ini" / "Konversi lead periode ini" agar basis tanggalnya tersirat di label itu sendiri. |
| N-baru | Rendah | `scripts/laporan.py` fungsi `ambil_crm()` | `--samarkan` tidak diteruskan ke pemanggilan `crm.py rekap`. Tidak berdampak saat ini (kontrak `rekap --json` `crm-wa` 1.0.1 tidak memuat nama/alasan bebas), tapi bila kontrak `crm-wa` berubah (mis. menambah ringkasan `alasan_batal` bebas teks ke `rekap --json`), potensi privasi baru bisa lolos tanpa terlihat di sini karena `--samarkan` dikira sudah diteruskan. Saran: teruskan `--samarkan` juga ke pemanggilan `crm.py rekap` untuk jaga-jaga (defense in depth), meski tidak wajib untuk versi `crm-wa` saat ini. |
| Kosmetik | Kosmetik | PROSPEK, "order perlu konfirmasi" | Order (deal) yang jadwal konfirmasinya sudah lewat (K0007, 1 hari lewat) dihitung di ringkasan angka PROSPEK tapi **tidak** memicu butir tersendiri di `PERLU PERHATIAN` (hanya "follow-up prospek CRM terlambat" yang dihitung dari `followup.terlambat`, bukan `order_perlu_konfirmasi`). Bukan cacat privasi/angka, hanya potensi terlewat oleh pemilik yang hanya membaca `PERLU PERHATIAN`. |

Tidak ditemukan angka yang salah, tidak ada penulisan ke database asli, tidak ada kebocoran nama/nomor prospek, tidak ada crash/hang untuk kasus alat tidak ada/rusak/terkunci, dan jadwal OpenClaw (harian 21:00 WIB & mingguan Senin 07:00 WIB) benar termasuk lewat `automations run` sungguhan.

**Rekomendasi:** perbaiki S2 sebelum naik ke `beta` (murah: satu baris penjelas atau perubahan label, tidak mengubah angka apa pun) — tanpa perbaikan, laporan bisa terbaca kontradiktif oleh audiens awam yang jadi sasaran utama produk ini. N-baru dan catatan kosmetik boleh dijadwalkan untuk versi berikutnya.
