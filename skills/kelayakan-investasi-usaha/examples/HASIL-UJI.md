# HASIL UJI — kelayakan-investasi-usaha

- **Tanggal:** 2026-10-05 (1.0.0, uji ulang 1.0.1 di hari yang sama) · **Penguji:** agent penguji independen (bukan pembuat)
- **Cara uji:** OpenClaw 2026.9.6 lokal, model router Komunitech `claude-sonnet-5` (sama dengan bot member), skill dimatikan vs aktif, home bersih per skenario; skenario normal juga dalam konteks kanal Telegram. Rincian & balasan utuh: `00-openclaw-sebelum-sesudah.md`.
- **Platform teruji:** `openclaw (uji otomatis agent)`

## Uji ulang 1.0.1 — skor kualitas: 9/10

| Skenario | Sebelum | Sesudah |
|---|---|---|
| 1 normal — mesin kopi Rp45 jt (sebelum: skor 1.0.0, tidak diuji ulang; sesudah: konteks Telegram 1.0.1) | 6 | 9 |
| 2 jebakan — kripto/"untung pasti" (semua sisi diuji ulang; sesudah lokal & Telegram sama) | 7 | 9 |
| Rata-rata | 6,5 | 9,0 |
| Tambahan: penghematan mobil box (sesudah lokal saja, di luar rata-rata) | — | 8 |

**Verdik 1.0.1: LULUS** — sesudah 9,0, selisih +2,5, tanpa kesalahan angka (NPV 12% & 20%, IRR, PI, balik modal, impas, sensitivitas, batas aman — semua cocok dengan Python independen).

**Perbaikan terbukti:** penolakan kripto kini membaca SKILL.md (lokal & Telegram): tolak janji untung, rujuk penasihat/platform berizin OJK, tanpa hitung deposito/reksa dana/kripto, kembali ke penilaian usaha, disclaimer, tanpa kata "tool"/nama skill. Omzet impas tidak lagi bergantung opsi (`--nilai-sisa` = `--nilai-residu`). Label "Penghematan" konsisten di kasus mobil box. NPV uji ketat 20% tampil.

**Cacat tersisa (1.0.1):**
1. Kalimat penjelas buatan agent bisa keliru walau angka benar (mobil box: "balik modal 4 th 3 bln — lebih lama dari masa proyek 5 tahun").
2. Balik modal terdiskonto tidak memasukkan nilai sisa, dan ini tidak disebut di balasan.
3. Keluaran teks script menulis "Rp 9.701.913" (spasi), kadang tersalin ke balasan.
4. Minor: "hitungkan dengan angka pasti" di penolakan; baris pajak ganda. Rujukan Permenko 1/2026 belum diverifikasi penguji.

## Uji 1.0.0 — skor kualitas: 8/10

| Skenario | Sebelum | Sesudah |
|---|---|---|
| 1 normal — mesin kopi Rp45 jt | 6 | 9 |
| 2 jebakan — kripto/"untung pasti" | 7 | 7 |
| Rata-rata | 6,5 | 8,0 |

**Verdik uji sebelum/sesudah: LULUS (tipis)** — sesudah 8,0, selisih +1,5, tanpa kesalahan angka.

**Alasan skor 8:** pada skenario hitungan, skill + script memberi hasil yang jelas lebih baik: semua angka (arus kas Rp42 jt/th, balik modal 1 th 1 bln, terdiskonto 1 th 3 bln, NPV Rp109.237.735, IRR 89,96%, PI 3,43, omzet impas Rp3.166.667/bln, sensitivitas −10%/−20%/+10%, batas aman 42,1%/101%) cocok dengan verifikasi Python independen; kesimpulan LAYAK konsisten dengan aturannya; asumsi, disclaimer, maks. 3 pertanyaan, tabel ≤ 3 kolom, tanpa kata proses — sama baiknya di konteks Telegram. Tanpa skill, model memberi keputusan yang benar tetapi tanpa NPV/IRR/uji meleset, tanpa disclaimer, dan satu angka impas keliru. Skor tidak 9 karena di skenario penolakan skill tidak dibuka sama sekali sehingga balasannya setara tanpa skill dan sempat membocorkan nama "tool".

## Cacat (1.0.0)
1. Penolakan kripto/"untung pasti": SKILL.md tidak dibaca (2/2), bocor nama alat & peran, tanpa disclaimer/rujukan penasihat berizin OJK, menawarkan proyeksi deposito/reksa dana. Perbaiki lewat `description`.
2. Omzet impas beda tergantung `--nilai-sisa` vs `--nilai-residu` (Rp3.250.000 vs Rp3.166.667/bln untuk kasus yang sama).
3. Script selalu berlabel "Omzet" walau kasus penghematan; perlu opsi label penghematan.
4. Diskonto 12% dapat dipakai sebagai asumsi batas bawah (bukan acuan pasar); sarankan tampilkan juga NPV pada 20%; verifikasi rujukan "Permenko 1/2026".
5. Aturan "kurang layak" (omzet −10%/biaya +10%/bergantung nilai jual kembali) tidak terlalu ketat; pertahankan.

## Verifikasi rujukan aturan — 2026-10-13 (penguji independen, untuk 1.0.5)
Catatan "Rujukan Permenko 1/2026 belum diverifikasi penguji" di atas (1.0.0 & 1.0.1) **sudah dicek**: Peraturan Menteri Koordinator Bidang Perekonomian No. 1 Tahun 2026 tentang Pedoman Pelaksanaan KUR ada (ditetapkan 5 Jan 2026, berlaku 13 Jan 2026, BN 2026 No. 17); Pasal 37 ayat (1) huruf a dan Pasal 44 ayat (1) huruf a memuat "6% (enam persen) efektif per tahun" untuk KUR mikro/kecil Sektor Produksi atau perdagangan berorientasi ekspor. Sumber: teks lengkap di basis data hukum DDTC (https://perpajakan.ddtc.co.id/sumber-hukum/peraturan-pusat/peraturan-menteri-koordinator-bidang-perekonomian-1-tahun-2026) dan siaran pers resmi Kemenko Perekonomian (Januari 2026, ekon.go.id/publikasi/detail/6784). Salinan resmi jdih.ekon.go.id/peraturan.go.id tidak dapat diakses saat pengecekan. Rincian di `references/istilah-dan-asumsi.md` bagian 2. Skor uji tidak berubah (perubahan 1.0.5 hanya teks rujukan; `tests/uji_kelayakan.py` lulus).
