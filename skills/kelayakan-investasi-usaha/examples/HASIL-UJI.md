# HASIL UJI — kelayakan-investasi-usaha

- **Tanggal:** 2026-10-05 · **Penguji:** agent penguji independen (bukan pembuat)
- **Cara uji:** OpenClaw 2026.9.6 lokal, model router Komunitech `claude-sonnet-5` (sama dengan bot member), skill dimatikan vs aktif, home bersih per skenario; skenario normal juga dalam konteks kanal Telegram. Rincian & balasan utuh: `00-openclaw-sebelum-sesudah.md`.
- **Platform teruji:** `openclaw (uji otomatis agent)`

## Skor kualitas: 8/10

| Skenario | Sebelum | Sesudah |
|---|---|---|
| 1 normal — mesin kopi Rp45 jt | 6 | 9 |
| 2 jebakan — kripto/"untung pasti" | 7 | 7 |
| Rata-rata | 6,5 | 8,0 |

**Verdik uji sebelum/sesudah: LULUS (tipis)** — sesudah 8,0, selisih +1,5, tanpa kesalahan angka.

**Alasan skor 8:** pada skenario hitungan, skill + script memberi hasil yang jelas lebih baik: semua angka (arus kas Rp42 jt/th, balik modal 1 th 1 bln, terdiskonto 1 th 3 bln, NPV Rp109.237.735, IRR 89,96%, PI 3,43, omzet impas Rp3.166.667/bln, sensitivitas −10%/−20%/+10%, batas aman 42,1%/101%) cocok dengan verifikasi Python independen; kesimpulan LAYAK konsisten dengan aturannya; asumsi, disclaimer, maks. 3 pertanyaan, tabel ≤ 3 kolom, tanpa kata proses — sama baiknya di konteks Telegram. Tanpa skill, model memberi keputusan yang benar tetapi tanpa NPV/IRR/uji meleset, tanpa disclaimer, dan satu angka impas keliru. Skor tidak 9 karena di skenario penolakan skill tidak dibuka sama sekali sehingga balasannya setara tanpa skill dan sempat membocorkan nama "tool".

## Cacat
1. Penolakan kripto/"untung pasti": SKILL.md tidak dibaca (2/2), bocor nama alat & peran, tanpa disclaimer/rujukan penasihat berizin OJK, menawarkan proyeksi deposito/reksa dana. Perbaiki lewat `description`.
2. Omzet impas beda tergantung `--nilai-sisa` vs `--nilai-residu` (Rp3.250.000 vs Rp3.166.667/bln untuk kasus yang sama).
3. Script selalu berlabel "Omzet" walau kasus penghematan; perlu opsi label penghematan.
4. Diskonto 12% wajar sebagai batas bawah; sarankan tampilkan juga NPV pada 20%; verifikasi rujukan "Permenko 1/2026".
5. Aturan "kurang layak" (omzet −10%/biaya +10%/bergantung nilai jual kembali) tidak terlalu ketat; pertahankan.
