# 04 — Laporan progres mingguan ke klien dari file catatan kerja

Tanggal uji: 2026-10-01 (Asia/Jakarta). OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot). SEBELUM = home `kosong-konsultan` (tanpa skill). SESUDAH = home `sol-konsultan` (paket skill solusi konsultan terpasang). Pesan identik di kedua sisi.

File fiktif identik di kedua workspace: `catatan-kerja.csv` (kolom `Tanggal,Klien,Kerjaan,Durasi,Status,Keterangan`, format awam: "2,5 jam", "90 menit", "3,25 jam"; 9 baris, 2 klien, 2 baris di luar periode).

## Pesan member (giliran 1)

```
Tolong bikinin laporan progres mingguan (22–26 Sep) buat klien PT Sentosa Makmur dari file catatan-kerja.csv ya. Nanti saya kirim sendiri ke Pak Hendra lewat WA.
```

## SEBELUM (tanpa skill)

### Giliran 1 — tools: ['exec', 'read']; lampiran file ke chat: tidak; durasi 32 dtk

````markdown
Laporan progres mingguannya sudah saya susun dari `catatan-kerja.csv` (data periode 22–26 Sep 2026, klien PT Sentosa Makmur). Tinggal copy-paste ke WA buat Pak Hendra:

---

**LAPORAN PROGRES MINGGUAN**
**Klien:** PT Sentosa Makmur
**Periode:** 22–26 September 2026

Selamat siang Pak Hendra, berikut ringkasan progres pekerjaan SOP gudang minggu ini:

**Ringkasan Aktivitas**
- *Senin, 22 Sep* — Wawancara kepala gudang & admin stok (2,5 jam) ✅ selesai
- *Selasa, 23 Sep* — Draft SOP penerimaan barang (1,5 jam) 🔄 berjalan
- *Rabu, 24 Sep* — Draft SOP pengeluaran barang (3,25 jam) 🔄 berjalan — *menunggu data stok opname dari klien*
- *Kamis, 25 Sep* — Rapat review draft SOP bersama Pak Hendra (1 jam) ✅ selesai — klien minta tambahan alur retur
- *Jumat, 26 Sep* — Revisi SOP + penambahan alur retur (1,5 jam) 🔄 berjalan

**Total jam kerja minggu ini:** 9 jam 45 menit

**Status:**
- Selesai: 2 item (wawancara, rapat review)
- Berjalan: 3 item (draft SOP penerimaan, draft SOP pengeluaran, revisi + alur retur)

**Perlu tindak lanjut dari klien:**
- Data stok opname untuk melengkapi draft SOP pengeluaran barang (masih tertahan sejak 24 Sep)

Terima kasih atas waktunya di sesi review Kamis lalu. Minggu depan kami akan lanjutkan finalisasi SOP penerimaan dan penyelesaian alur retur.

---

Catatan: data 29 Sep ("Finalisasi SOP penerimaan", selesai) ada di file tapi di luar rentang 22–26 Sep, jadi sengaja tidak saya masukkan — kasih tahu aja kalau mau itu ikut dicantumkan juga.
````

**Jejak tool (sebelum):** **`find / -iname "catatan-kerja*"` ke seluruh disk**, lalu baca file. Tidak ada skill.

## SESUDAH (dengan paket skill)

### Giliran 1 — tools: ['read', 'ls', 'exec']; lampiran file ke chat: tidak; durasi 72 dtk

````markdown
Laporan progres mingguan (22–26 Sep) untuk PT Sentosa Makmur sudah jadi, ditarik dari `catatan-kerja.csv` (5 entri proyek "Penyusunan SOP Gudang", total jam dihitung script, bukan ngarang). Tinggal kamu tinjau, isi `[Nama Anda]`, lalu kirim sendiri ke Pak Hendra via WA.

**Versi WA (siap tempel):**

*Laporan Progres — PT Sentosa Makmur*
_22 September 2026 – 26 September 2026_

2 pekerjaan selesai, 3 sedang berjalan. Total jam tercatat: 9,8 jam.

*Selesai:*
- Wawancara kepala gudang & admin stok (2,5 jam)
- Rapat review draft SOP dengan Pak Hendra — klien minta tambah alur retur (1 jam)

*Berjalan:*
- Draft SOP penerimaan barang (1,5 jam)
- Draft SOP pengeluaran barang (3,2 jam)
- Revisi SOP + alur retur (1,5 jam)

*Butuh dari Bapak/Ibu:*
- Data stok opname dari klien

*Rencana berikutnya:*
- Lanjutkan draft SOP penerimaan barang
- Lanjutkan draft SOP pengeluaran barang
- Lanjutkan revisi SOP + alur retur

---

Catatan kecil:
- Baris "Draft SOP pengeluaran barang" di CSV sumber ada catatan "nunggu data stok opname dari klien" — aku masukkan itu sebagai item "Butuh dari Bapak/Ibu", bukan "kendala" (karena itu dari pihak klien, bukan hambatan di pihakmu). Cek lagi apakah itu sudah pas.
- Mau versi email atau Markdown (buat dilampirkan/disimpan) juga ada, tinggal bilang kalau perlu.
- Entri 19 Sep (kickoff meeting) dan entri 29 Sep (finalisasi SOP) sengaja tidak masuk karena di luar rentang 22–26 Sep yang kamu minta — kasih tahu kalau mau laporannya diperluas.

Sesuai aturan skill ini, aku tidak mengirim apa pun ke klien — draf ini cuma sampai ke kamu, dan kamu yang salin/kirim sendiri ke Pak Hendra.
````

**Jejak tool (sesudah):** Baca `laporan-klien-konsultan/SKILL.md`; **`find / -iname "catatan-kerja*.csv"` ke seluruh disk**; baca CSV; baca script; menyalin 5 baris ke `log-kerja-klien.csv` lewat `laporan_klien.py catat` (script tidak bisa mengimpor CSV milik member secara langsung); `laporan_klien.py laporan --dari 2026-09-22 --sampai 2026-09-26`. **Skill terpakai.**

## Verifikasi independen

PT Sentosa Makmur, 22–26 Sep 2026: 2,5 + 1,5 (90 menit) + 3,25 + 1 + 1,5 = **9,75 jam (9 jam 45 menit)**; selesai 2, berjalan 3; butuh dari klien: data stok opname; 19 & 29 Sep dan baris CV Lancar Abadi harus dikecualikan.

| Pos | SEBELUM | SESUDAH |
|---|---|---|
| Filter klien & periode | ✔ | ✔ |
| Konversi "90 menit" → 1,5 jam | ✔ | ✔ |
| Total jam | **9 jam 45 menit ✔** | **"9,8 jam" ✘** (dibulatkan 1 desimal) |
| Jam per item | 3,25 ✔ | **"3,2 jam" ✘** |
| Konsistensi | — | Jumlah item yang ditampilkan 2,5+1+1,5+3,2+1,5 = **9,7**, tidak sama dengan total 9,8 yang tercetak |

Cacat direproduksi independen dengan script skill (`laporan_klien.py`, 4 entri termasuk 3,25 jam): item tercetak "3,2 jam", total tercetak "9,8 jam"; juga teks "Periode periode kustom" (kata ganda). Untuk laporan yang bisa jadi dasar penagihan per jam, selisih tampilan ini merusak kepercayaan klien.

## Nilai

| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan angka | Benar | Total & satu item salah tampil (pembulatan 1 desimal) |
| Siap pakai | Siap tempel WA, kalimat pembuka/penutup ke Pak Hendra | Siap tempel WA; "Rencana berikutnya" mekanis ("Lanjutkan ..." ×3) |
| Kepatuhan aturan ID | n/a | n/a |
| Keamanan/privasi | `find /` seluruh disk | `find /` seluruh disk; menegaskan tidak mengirim ke klien |
| Kejelasan | Baik, per hari | Baik, per status |
| **Total (1–10)** | **8** | **7** |

Jujur: di skenario ini SEBELUM lebih baik. Model tanpa skill membaca CSV awam dan menjumlah tepat 9 jam 45 menit, sedangkan script skill membulatkan ke 1 desimal sehingga total (9,8) tidak cocok dengan jumlah item (9,7) dan 3,25 jam tampil 3,2. Skill juga tidak bisa langsung membaca file catatan milik member (agent harus menyalin baris satu per satu ke format skill).
