# Skenario 02 — Kantor konsultan (normal): notulen WA jadi tugas

**Penguji:** pembuat skill, 2026-09-26. Dijalankan sungguhan terhadap **Vikunja 2.6.0 asli**,
proyek "Kantor Konsultan Mitra Prima" (id 3).

## Permintaan pengguna
> "Ini notulen rapat internal tadi, tolong jadikan daftar tugas:
> - Rina: siapkan draf laporan audit untuk klien PT Sentosa sebelum Jumat
> - Dimas - follow up pembayaran invoice klien besok
> * Rapat evaluasi bulanan urgent minggu depan
> Catatan: rapat berikutnya hari Senin"

## Perintah agent
```bash
python3 scripts/vikunja.py dari-teks --teks "Notulen rapat internal, Sabtu 26 September 2026
- Rina: siapkan draf laporan audit untuk klien PT Sentosa sebelum Jumat
- Dimas - follow up pembayaran invoice klien besok
* Rapat evaluasi bulanan urgent minggu depan
Catatan: rapat berikutnya hari Senin" --keluaran draf-konsultan.json
```

## Keluaran
```
DRAF 3 TUGAS (BELUM masuk Vikunja) -> disimpan di: draf-konsultan.json
1. siapkan draf laporan audit untuk klien PT Sentosa sebelum Jumat (PIC: Rina; tenggat: 2026-10-02)
2. follow up pembayaran invoice klien besok (PIC: Dimas; tenggat: 2026-09-27)
3. Rapat evaluasi bulanan urgent minggu depan (tenggat: 2026-10-03; mendesak)
(2 baris lain diabaikan — bukan baris berawalan '-'/'*'/angka.)

PERIKSA dulu tiap baris (field 'ke' & 'tenggat' hanya TEBAKAN dari kata-kata di teks; 'proyek' masih kosong)...
```
Agent menyampaikan draf ini ke pengguna: "Ini 3 tugas yang saya tangkap dari notulen. Tolong cek PIC dan tanggalnya — sudah benar? Mau saya masukkan ke proyek 'Kantor Konsultan Mitra Prima'?"

**Catatan jujur:** Rina dan Dimas dalam contoh ini adalah nama fiktif yang **belum** terdaftar sebagai
pengguna di instance Vikunja uji. Ini sengaja dipertahankan untuk menunjukkan perilaku nyata pada
langkah berikutnya.

## Setelah pengguna menjawab "ya" (proyek dipilih)
```bash
python3 scripts/vikunja.py tambah --batch draf-konsultan.json --proyek "Kantor Konsultan Mitra Prima" --ya
```
```
CATATAN: tugas #14 tersimpan, tapi GAGAL menugaskan ke 'Rina': Anggota 'Rina' tidak ditemukan di proyek ini (atau token tidak berizin 'projects: projectusers'). Pastikan orang itu sudah ditambahkan ke tim/proyek di Vikunja.
CATATAN: tugas #15 tersimpan, tapi GAGAL menugaskan ke 'Dimas': Anggota 'Dimas' tidak ditemukan di proyek ini (atau token tidak berizin 'projects: projectusers'). Pastikan orang itu sudah ditambahkan ke tim/proyek di Vikunja.
TERSIMPAN 3 TUGAS DI VIKUNJA:
- #14 siapkan draf laporan audit untuk klien PT Sentosa sebelum Jumat (proyek id 3)
- #15 follow up pembayaran invoice klien besok (proyek id 3)
- #16 Rapat evaluasi bulanan urgent minggu depan (proyek id 3)
```
Agent menyampaikan apa adanya: ketiga tugas **berhasil tersimpan**; penugasan ke Rina & Dimas
**gagal** karena mereka belum jadi anggota proyek di Vikunja — agent menyarankan pemilik menambah
mereka di Vikunja lalu menugaskan manual, atau mengulang `tambah --ke` setelah itu.

## Ringkasan tim setelahnya
```bash
python3 scripts/vikunja.py ringkasan --proyek "Kantor Konsultan Mitra Prima"
```
```
RINGKASAN TUGAS TERBUKA

BELUM ADA PIC (3 tugas):
  - siapkan draf laporan audit untuk klien PT Sentosa sebelum Jumat (jatuh tempo 2 Okt 2026)
  - follow up pembayaran invoice klien besok (jatuh tempo 27 Sep 2026)
  - Rapat evaluasi bulanan urgent minggu depan (mendesak; jatuh tempo 3 Okt 2026)
```

**Kesimpulan:** `dari-teks` mengubah notulen jadi draf terstruktur tanpa menyentuh Vikunja;
kegagalan penugasan ditangani dengan baik (tugas tetap tersimpan, kegagalan dilaporkan jelas,
tidak ada data yang hilang atau silang).
