# QA panduan beta (C4) — 2026-10-17

Cakupan: `docs/program-beta.md`, `docs/panduan-beta-tester.md` (+ `.html`), `koordinasi/beta-vip-2026-10-13.md` (draf rekrut), dicocokkan dengan `docs/instalasi.md` (= `CARA-INSTAL.md` di ZIP) dan `scripts/build.py`. Sudut pandang: pemilik usaha awam teknologi yang menerima ZIP di Telegram. Berkas lain tidak diubah; semua usulan di bawah menunggu penerapan.

Fakta build.py yang dipakai (dibaca dari kode): `--vip --beta` memaketkan semua skill berstatus `rilis`/`beta` (kini 123 skill, bukan hanya 10) + `solusi-vip/*.md` + `templates/openclaw-AGENTS-komunitech.md` + `docs/<panduan>.md` yang dirujuk skill + `CARA-INSTAL.md` (salinan `docs/instalasi.md`) + `LISENSI.txt`. `docs/program-beta.md`, `docs/uji-platform.md` ada di `DOCS_INTERNAL` (tidak ikut). `docs/panduan-beta-tester.md/.html` tidak pernah ikut ZIP. Nama file: `komunitech-vip-beta-<slug>-<12 hex>.zip` (sesuai contoh di panduan).

## P1 (harus diperbaiki sebelum tester berikutnya)

**1. CARA-INSTAL.md bertentangan dengan panduan beta (risiko pasang 123 skill sekaligus).**
Panduan §2: "`CARA-INSTAL.md` — panduan pasang lengkap per platform". Tetapi CARA-INSTAL bagian "Cara cepat: satu perintah" menyuruh `Expand-Archive NAMA-FILE.zip "$env:USERPROFILE\.claude\skills"` / `unzip -o NAMA-FILE.zip -d ~/.claude/skills`, sedangkan panduan §3 melarang mengekstrak seluruh ZIP ke folder skills. Tester awam yang membuka CARA-INSTAL (disebut "lengkap") akan mengikuti yang cepat.
Usulan (ganti kalimat di panduan §2): "`CARA-INSTAL.md` — panduan umum untuk semua paket Komunitech. **Untuk paket beta ini, abaikan bagian 'Cara cepat: satu perintah' di dalamnya**: itu memasang semua skill sekaligus. Ikuti bagian 3 panduan ini (salin hanya folder skill yang Anda pilih)."

**2. Panduan beta tidak ada di dalam ZIP, tetapi program-beta menyatakan sebaliknya.**
`program-beta.md` langkah 3: "seluruh library + panduan tester". Faktanya build.py tidak menyertakan `panduan-beta-tester.md/.html`; panduan dikirim terpisah (teks + .html di topik). Operator yang percaya kalimat itu mengirim ZIP saja, dan tester tidak punya panduan.
Usulan: "Kirim paket: ... (ZIP berisi seluruh library; **panduan tester TIDAK ikut ZIP**, kirim terpisah sebagai berkas `panduan-beta-tester-komunitech.html` + teks ringkas di topik yang sama)."

**3. Klaim anonim tidak sesuai alur kirim masukan.**
Panduan §7 dan §6: "Jawaban diteruskan ke tim tanpa nama/kontak Anda" dan "yang kami terima hanya jawaban formulir". Padahal masukan dikirim sebagai pesan Telegram di topik 1349 (nama/akun tampak, dan tester lain di topik yang sama ikut membaca) atau japri ke pemilik. Yang benar: dirangkum anonim di laporan, bukan anonim saat dikirim.
Usulan: "Jawaban Anda dikirim sebagai pesan di Telegram, jadi pemilik Komunitech (dan peserta lain di topik itu, bila Anda memakai topik) bisa melihat nama akun Anda. Di laporan tim, jawaban Anda ditulis tanpa nama (Beta 1, Beta 2, dst.). Ingin jawaban tidak terlihat peserta lain? Kirim lewat pesan pribadi." Juga putuskan: bila beberapa tester berbagi satu topik, ZIP ber-watermark tiap orang terlihat peserta lain; usulkan satu topik/obrolan pribadi per tester.

**4. Tempat mengirim masukan tidak pasti untuk tester berikutnya.**
Panduan: "di topik Telegram tempat Anda menerima paket ini … di grup Telegram Komunitech tempat Anda diundang". Draf rekrut (beta-vip) justru menyuruh kirim lewat "WA/Telegram pribadi, bukan grup uji", dan paket dikirim lewat sana. Tester yang menerima paket via WA tidak punya "topik". Tidak ada cara bergabung/ID topik/handle pemilik.
Usulan: tambah satu kalimat tetap di §7: "Kirim masukan ke: [isi: nama grup/tautan undangan atau @handle pemilik]. Bila Anda menerima paket lewat WhatsApp, kirim balasan di obrolan WhatsApp yang sama." Operator wajib mengisi satu jalur per tester sebelum kirim.

**5. Imbalan "gratis selamanya" menyesatkan bagi member VIP.**
Panduan §1/§8: "10 skill yang diuji gratis selamanya + 1 skill lain pilihan Anda". Penerima adalah member VIP yang sudah punya akses penuh ke library (dan ZIP beta sendiri berisi 123 skill termasuk 2 skill tier VIP). Jadi imbalan tampak kosong, atau memicu salah paham (apakah tetap boleh dipakai bila VIP berhenti?). `program-beta.md` menulis versi lain: "1 skill lain gratis / diskon perpanjangan VIP" (tidak sama).
Usulan: tentukan satu imbalan nyata, lalu tulis jelas, mis.: "Imbalan: 10 skill ini tetap boleh Anda pakai **walau langganan VIP berakhir**, ditambah [isian pemilik: 1 skill ecer pilihan / diskon perpanjangan VIP X%]. Diberikan setelah formulir diterima." Samakan di `program-beta.md`, panduan §1, §8, dan draf rekrut.

**6. Draf rekrut meremehkan beban kerja.**
Draf pesan: "Syaratnya cuma pakai untuk pekerjaan sungguhan minimal 3 kali dan isi formulir 5 menit di hari ke-7." Panduan sebenarnya: minimal 3 skill × minimal 3 pakai (9 pakai), catatan tiap pemakaian, satu formulir per skill (≥15 menit), serta pasang sendiri lewat Terminal untuk OpenClaw. Tester merasa dijebak.
Usulan: "Syaratnya: pilih minimal 3 dari 10 skill, pakai tiap skill minimal 3 kali untuk pekerjaan sungguhan selama 7 hari, catat singkat tiap pemakaian, lalu isi formulir ±5 menit per skill. Total sekitar 15–20 menit untuk formulir, dan pemasangan sekitar 10–20 menit."

**7. Pemasangan OpenClaw untuk member yang OpenClaw-nya di VPS/mini PC tidak tercakup.**
CLAUDE.md menyebut mesin 24 jam bisa VPS milik member. Panduan §3 berasumsi ZIP diekstrak di komputer yang sama dengan OpenClaw (`cd` ke folder hasil ekstrak, seret folder). Tester dengan OpenClaw di VPS tidak diberi jalur (unggah folder, `scp`, atau minta bot memasang). Windows non-WSL: "belum kami uji" tanpa alternatif.
Usulan (sisipkan di §3 OpenClaw): "OpenClaw Anda jalan di komputer lain (VPS/mini PC)? Kirim folder skill ke komputer itu (cara yang biasa Anda pakai untuk memindah file), lalu jalankan langkah 3–4 di sana. Tidak tahu caranya? Tulis 'Perlu bantuan' di topik, kami pandu." Untuk Windows non-WSL, tulis folder tujuan yang dipakai OpenClaw-mu atau tanya tim; jangan diam.

## P2 (rapikan)

**8. Tenggat tanggal kaku; tester yang direkrut belakangan kehabisan waktu.** Panduan: "7 hari, 13–19 Oktober … paling lambat 20 Oktober". Hari ini 17 Oktober; tester baru praktis hanya punya 2–3 hari. Usulan: "Masa uji: 7 hari sejak Anda menerima ZIP (Tester 1: 13–19 Oktober). Kirim masukan paling lambat 1 hari sesudah hari ke-7." Bila tanggal tetap, tulis "tanggal ini khusus penerima paket 13 Oktober".

**9. Rujukan `docs/instalasi.md` di README skill salah nama di dalam ZIP.** README skill (mis. pantau-cron-openclaw): "ada di `docs/instalasi.md` dalam paket". Di ZIP namanya `CARA-INSTAL.md` (tidak ada folder docs/instalasi.md). Usulan di panduan §2: "README beberapa skill menyebut `docs/instalasi.md`; di paket Anda berkas itu bernama `CARA-INSTAL.md`." (perbaikan permanen: ubah teks README atau build.py, di luar cakupan QA ini).

**10. Jargon belum dijelaskan untuk awam.** Kutipan lalu usulan:
- "pasang pengawas" (§5 no. 1): "pasang pengawas, yaitu pencatat yang memberi kabar ke Telegram bila jadwal otomatis bot terlambat".
- "WSL" (dijelaskan sekali, tapi diulang tanpa penjelasan di FAQ): ulangi "(fitur Windows untuk menjalankan Linux)" atau tulis "bila Anda tidak tahu apa itu WSL, anggap tidak memakainya dan tulis 'Perlu bantuan'".
- "Terminal", "`cd`", "`ls`": tambah "Terminal = jendela tempat mengetik perintah" dan "`ls` = melihat isi folder".
- "watermark" (§2, §6): "tanda pengenal tersembunyi berisi nama dan kode lisensi Anda".
- "script/skrip", "Python 3", "PATH": cukup "program pembantu hitung (Python)".
- "CSV" (§5 no. 5 tambahan): "berkas tabel (CSV, bisa dibuat dari Excel: Save As → CSV)".
- "japri": tulis "pesan pribadi (japri)".
- "bot" vs "agent" vs "OpenClaw": tambah satu kalimat di §1 "Bot Anda = agen OpenClaw yang Anda ajak bicara lewat Telegram".

**11. Klaim lintas platform belum teruji.** §5 "Tambahan": "Semua berformat sama di OpenClaw, Claude Code, Codex, dan Cursor" (3 skill tambahan) dan "delapan skill lain berformat sama sehingga bisa dipasang di Claude Code, Codex, atau Cursor". Hanya format yang sama yang pasti; keberhasilan dipakai belum diuji di tiga platform itu (hanya OpenClaw). Usulan: "Format filenya sama sehingga seharusnya bisa dipasang di platform lain, tetapi kami baru menguji di OpenClaw." Juga "dicoba langsung lewat bot Telegram OpenClaw" (§1) cukup untuk 10 skill; tiga skill tambahan tidak terbukti di bot asli, tambah "(tiga skill tambahan belum diuji di bot Telegram)".

**12. Klaim "Cursor … ketik `/` di chat" vs instalasi.** `CARA-INSTAL.md` untuk Cursor menyebut cek lewat `/nama-skill` atau Settings → Rules, dan catatan Cursor Cloud tidak memuat skill dari folder user; panduan beta tidak menyebut Cloud. Usulan satu kalimat di bagian Cursor: "Pakai chat Agent di aplikasi Cursor di komputer Anda (bukan Cloud Agent atau jadwal otomatis); di sana skill dari folder pribadi tidak otomatis terbaca."

**13. Kalimat uji Hari 1 bisa membingungkan hasilnya.** "bot menjawab tegas layak / kurang layak / tidak layak … (Bila muncul 'dihitung manual, mohon dicek' berarti Python belum terpasang)". Contoh mesin kopi 25 jt / 4 jt = jelas layak; tester tidak tahu apa yang harus dilakukan bila bot malah bertanya balik. Usulan: "Bila bot bertanya balik (mis. biaya bulanan), jawab semuanya dalam satu pesan. Tanda berhasil tetap: ada jawaban layak/kurang layak/tidak layak. Bila bot tidak memakai skill sama sekali (jawaban umum tanpa kata 'balik modal'), tulis 'skill tidak terpanggil' di catatan."

**14. Ukuran/isi ZIP bisa basi.** "sekitar 9,8 MB", "lebih dari 100 folder" dihitung 13 Oktober; ZIP kini memuat 123 skill. Usulan: "ukuran sekitar 10 MB (bisa berubah)". Tambahkan: unduh dan ekstrak di komputer, bukan di HP (ZIP berisi ratusan folder; sulit dibuka di ponsel). Panduan tidak menyebut tester yang hanya punya Telegram di HP.

**15. Duplikasi formulir dan sumber kebenaran ganda.** Formulir 11 pertanyaan ada di `program-beta.md` dan panduan §7 (kini identik, tetapi pasti menyimpang). Usulan: `program-beta.md` merujuk "formulir ada di `docs/panduan-beta-tester.md` §7" sebagai satu-satunya sumber. Juga `.html` panduan perlu dibuat ulang bila `.md` berubah (artifact masih privat; tester tidak bisa membuka tautan Artifact tanpa dibagikan).

**16. Tanda "[isian: ...]" di panduan §5 (no. 9, 10) berbeda dari kalimat tempel `[produk] Rp[harga]`.** Dua gaya kurung membingungkan. Usulan: satu aturan di §5 awal: "Bagian dalam [kurung siku] adalah isian; ganti seluruhnya, termasuk kurungnya."

## Ringkasan prioritas
P1: 7 temuan (1 konflik cara pasang, 2 panduan tak ikut ZIP, 3 anonimitas, 4 jalur kirim masukan, 5 imbalan, 6 draf rekrut, 7 OpenClaw di VPS). P2: 9 temuan (8–16).
Tidak diubah: semua berkas panduan (sesuai instruksi). Perubahan `docs/program-beta.md` dan `docs/panduan-beta-tester.md` menunggu giliran penerapan; no. 5 (imbalan) dan no. 3 (cara kirim) perlu keputusan pemilik.
