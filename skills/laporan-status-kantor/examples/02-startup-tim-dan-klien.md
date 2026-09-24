# Skenario 2 (S2, normal) — update tim startup + versi klien

## Skenario
Startup kecil: 6 poin progres tim campur ID/EN → minta update tim nada santai-profesional
+ versi untuk klien (tanpa info internal sensitif).

## Input pengguna (persis)
> "eh bikinin update mingguan buat tim ya, santai aja gaya startup gitu. terus sekalian
> versi yang bisa dikirim ke klien kita, PT Maju Bersama, tapi jangan ada info internal
> yang sensitif. ini poin2nya: 1) landing page udah deploy ke production, 2) API
> integration sama payment gateway masih blocked nunggu vendor, ETA gak jelas, 3) ada 2
> orang tim resign minggu ini jadi rada kacau workload-nya, 4) fitur dashboard analytics
> buat klien on track, target selesai minggu depan, 5) budget server bulan ini over dikit
> gara2 traffic naik, 6) mau mulai testing fitur baru minggu depan. nama tim: Tim Produk."

## Output (mengikuti SKILL.md)

### Versi tim (WA/Telegram, santai-profesional, template `3p-ke-tim.md`)
```
🚀 *Tim Produk* — Update internal, 21–25 Sep 2026
*Progres:* Landing page udah deploy ke production. Dashboard analytics untuk klien on
track, target kelar minggu depan.
*Rencana:* Mulai testing fitur baru minggu depan.
*Kendala:* API integration ke payment gateway masih blocked, nunggu vendor dan ETA-nya
belum jelas. Ada 2 orang tim resign minggu ini jadi workload rada berat — butuh diskusi
soal redistribusi tugas. Budget server bulan ini juga sedikit over gara-gara traffic naik,
perlu di-review.

_Asumsi: periode minggu berjalan (21–25 Sep 2026), penerima tim internal. Ganti jika
perlu._
```

### Versi klien (email, sopan-formal wajib, template `3p-ke-klien.md`)
```
Yth. Bapak/Ibu PT Maju Bersama,

Berikut update progres proyek untuk periode 21–25 Sep 2026.

Progres:
- Landing page telah selesai dan sudah tayang di production.
- Dashboard analytics sedang berjalan sesuai rencana, ditargetkan selesai minggu depan.

Rencana selanjutnya:
- Mulai proses testing untuk fitur baru minggu depan.

Catatan:
- Integrasi payment gateway masih menunggu proses dari pihak vendor terkait; kami akan
  menginformasikan estimasi waktu penyelesaian segera setelah ada kepastian dari vendor.

Mohon informasikan bila ada pertanyaan. Terima kasih atas kepercayaannya.

Hormat kami,
Tim Produk
```

## Catatan penguji

**Bagus:**
- Versi klien dengan benar **menghapus** info resign karyawan dan over-budget server —
  persis sesuai aturan `3p-ke-klien.md`: "Jangan pernah menyertakan: masalah SDM internal,
  masalah keuangan internal perusahaan sendiri". Ini poin krusial dan lolos.
- Versi klien otomatis sopan-formal walau versi tim santai — sesuai instruksi "Selalu
  sopan-formal [ke klien], apa pun budaya kantor internal".
- Ketidakpastian ETA vendor pada versi klien ditulis solutif ("akan menginformasikan
  estimasi...") bukan mengarang tanggal, sesuai aturan "jangan menyalahkan vendor secara
  terbuka ... cukup jelaskan dampak + langkah mitigasi". Baik.
- Campuran ID/EN pada bahan mentah ("blocked", "ETA", "on track") dipertahankan secara
  wajar di versi tim (istilah kerja lazim), diterjemahkan halus di versi klien formal.
- Bahasa keseluruhan tetap Bahasa Indonesia (bukan permintaan bilingual ID+EN penuh — user
  tidak minta versi Inggris terpisah, jadi benar tidak dibuatkan).

**Temuan:**
- Tidak ada cacat berat. Satu catatan RINGAN: SKILL.md tidak secara eksplisit
  mengingatkan agen untuk **memeriksa ulang versi klien demi memastikan tidak ada
  kebocoran** sebelum diserahkan — pada praktiknya berhasil di sini, tapi checklist akhir
  SKILL.md tidak punya butir khusus "versi klien sudah disaring dari info internal
  sensitif" (checklist yang ada lebih umum ke "data sensitif karyawan"). Saran: tambah
  butir checklist eksplisit untuk kasus dual-audience seperti ini.
