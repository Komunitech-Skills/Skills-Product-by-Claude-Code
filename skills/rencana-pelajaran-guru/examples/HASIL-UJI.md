# HASIL UJI — rencana-pelajaran-guru v1.0.0

- **Tanggal:** 2026-09-24
- **Penguji:** agent penguji independen (simulasi, Claude Code), bukan pembuat skill. Hanya
  membaca folder `skills/rencana-pelajaran-guru/` (SKILL.md, references/, templates/,
  scripts/, ATTRIBUTION.md) + sumber ATM di GitHub (dibaca, tidak dijalankan) + pencarian
  web untuk verifikasi regulasi.
- **Lingkungan:** Linux, Python 3.11.15. Skill disalin ke scratchpad terpisah
  (`uji-rpg/skills/rencana-pelajaran-guru`), tidak dipasang di `.claude/skills` repo ini.
- **Uji muat OpenClaw:** `bash scripts/uji_openclaw.sh` (dari `/home/user/Skills`) →
  **OpenClaw 2026.9.6**: `eligible 55/55`, `modelVisible 55/55`, `commandVisible 55/55` —
  `rencana-pelajaran-guru` lulus semua 3 kriteria bersama 54 skill lain.
- **Platform teruji:** `claude-code (simulasi agent)`; `openclaw (uji muat otomatis)`.
  Perilaku agent sungguhan di OpenClaw/Codex/Cursor **belum** diuji manusia.

## Verifikasi fakta regulasi (independen, sumber resmi/liputan resmi)
| Klaim di `references/dasar-kurikulum.md` | Status | Sumber |
|---|---|---|
| Permendikdasmen No. 13/2025 = penguatan Pembelajaran Mendalam, bukan kurikulum baru | **Benar** | [kemendikdasmen.go.id](https://www.kemendikdasmen.go.id/siaran-pers/13278-permendikdasmen-nomor-13-tahun-2025-menguatkan-arah-kebijakan-melalui-pembelajaran-mendalam), [hypeabis.id](https://hypeabis.id/read/50791/kurikulum-2025-tak-berubah-ini-isi-permendikdasmen-nomor-13) |
| Profil Pelajar Pancasila (6 dimensi) → Profil Lulusan (8 dimensi) | **Benar**, dimensi terverifikasi: keimanan-ketakwaan, kewargaan, penalaran kritis, kreativitas, kolaborasi, kemandirian, kesehatan, komunikasi | [detikEdu](https://www.detik.com/edu/sekolah/d-8024208/profil-pelajar-pancasila-kini-ganti-istilah-jadi-profil-lulusan-apa-bedanya), pencarian independen sesi ini |
| BSKAP No. 046/H/KR/2025 mencabut BSKAP No. 032/H/KR/2024, CP tetap 6 fase A–F | **Benar** (dicek ulang, judul di guru.kemendikdasmen.go.id memakai kata "Perubahan atas" tapi isi kebijakan mencabut & menyatakan tidak berlaku CP 2024 — sudah konsisten dgn skill) | [guru.kemendikdasmen.go.id](https://guru.kemendikdasmen.go.id/dokumen/74r6Yln0zK), [komunitasbelajar.id](https://www.komunitasbelajar.id/2025/07/keputusan-kepala-bskap-nomor-046hkr2025.html) |
| Fase A–F ↔ kelas (A: 1–2, B: 3–4, C: 5–6, D: SMP 7–9, E: SMA 10, F: SMA 11–12) | **Benar** | Konsisten di seluruh sumber yang dicek |
| 1 JP: SD/MI 35’, SMP/MTs 40’, SMA/MA/SMK 45’ | **Benar** | [blogsusanto.com](https://blogsusanto.com/jam-pelajaran-kurikulum-merdeka-tahun-ajaran-2025-2026-berdasarkan-permendikdasmen-nomor-13-2025/), dikonfirmasi ulang lewat pencarian independen sesi ini |
| Tidak ada CP resmi yang dikutip/dikarang di SKILL.md/references/templates/examples | **Benar** — setiap CP di seluruh skenario ditandai "(cek CP resmi)" | Diperiksa manual seluruh berkas |

**Tidak ditemukan fakta regulasi yang salah.** Semua nomor peraturan, istilah, dan angka JP
di `references/dasar-kurikulum.md` cocok dengan sumber resmi/liputan resmi independen.

## Verifikasi script `hitung_alokasi_waktu.py`
Dijalankan dengan data normal (3 kombinasi jenjang/JP/pertemuan, hasil COCOK, dicocokkan
manual: 15+90+15=120=3×40, 10+50+10=70=2×35, 10+65+15=90=2×45 — **0 beda**) dan data rusak
(9 kasus: `--jp 0`, `--jp` negatif, jenjang tidak valid, format pertemuan salah jumlah
kolom, nilai non-angka, menit negatif, input kosong, hanya titik-koma, desimal) — semua
gagal **dengan pesan error yang jelas & ramah guru**, tidak ada crash tak terduga, tidak
ada angka salah yang lolos. Kasus banyak-pertemuan campur cocok/tidak cocok (KEKURANGAN)
juga terverifikasi benar. **Lulus penuh.**

## Kepatuhan lisensi (CLAUDE.md Tahap 2 — Apache-2.0)
| Syarat Apache-2.0 | Terpenuhi? |
|---|---|
| Teks lisensi lengkap disertakan | ✓ `LICENSE-APACHE.txt` — teks Apache 2.0 lengkap & benar |
| `NOTICE` asli disalin | ✓ `NOTICE-UPSTREAM.txt` sesuai isi `NOTICE` repo sumber |
| Atribusi jelas (sumber, pembuat, commit, tanggal) | ✓ `ATTRIBUTION.md` sangat rinci: URL, commit hash `281eb8d4...`, tanggal akses |
| Keterangan file telah diubah | ✓ `ATTRIBUTION.md` §"Yang diubah/ditambahkan" merinci per poin apa yang ditulis ulang vs ditiru polanya |
| Tidak ada frontmatter/field bergaya sumber yang tersisa | ✓ frontmatter hanya `name`+`description` (diverifikasi: `name: rencana-pelajaran-guru`, deskripsi 657 karakter, < batas 1024) |
| Tidak ada konten kurikulum sumber (CCSS/NGSS) tersalin | ✓ dicek manual seluruh `references/`, `templates/`, `examples/` — nihil |
| Nilai tambah signifikan vs skill sumber gratis | ✓ lihat `examples/00-banding-pesaing.md` — lokalisasi total + script verifikasi baru + RPP 1 lembar (tidak ada di sumber) |
**Lisensi: patuh, tidak ada temuan.**

## Skenario
| No | Berkas | Isi | Hasil |
|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | A/B skenario IPA ekosistem | Skill **jelas lebih baik** (CP karangan vs jujur, menit tidak cocok vs terverifikasi) |
| 00 | `00-banding-pesaing.md` | vs `k12-lesson-plan-creation` (Anthropic) & prompt publik ID terbaik | Skill **menang telak** kedua pesaing untuk pasar Indonesia |
| 01 | `01-uji-independen-modul-ajar-ipa-kelas7-ekosistem.md` | Modul Ajar penuh, IPA kelas 7, 2 pertemuan | **Lulus**; 1 cacat sedang (CACAT-01) |
| 02 | `02-rpp-1-lembar-matematika-kelas4-pecahan-pasar.md` | RPP 1 lembar saja, Matematika kelas 4 SD, konteks pasar | **Lulus**; 0 cacat |
| 03 | `03-lkpd-soal-rubrik-bindo-kelas10-eksposisi.md` | LKPD + 10 soal + kunci + rubrik, Bahasa Indonesia kelas 10 | **Lulus**; 0 cacat |
| 04 | `04-input-tidak-lengkap.md` | "bikin RPP buat besok" (mapel & jenjang tak disebut) | **Lulus**; 1 cacat rendah (CACAT-02) |
| 05 | `05-di-luar-cakupan.md` | Bocoran ANBK/TKA + minta kode CP resmi persis tanpa sumber | **Lulus, kuat**; 0 cacat |

## Verifikasi angka independen (dihitung ulang manual/Python, bukan pakai kode skill)
| Diuji | Hasil |
|---|---|
| Total menit tiap skenario (01: 80×2, 02: 70, 03: 90) vs JP×menit/JP jenjang | **0 beda** |
| Rantai makanan ekosistem (padi→tikus→ular→elang) urut produsen→konsumen1→2→3 | Benar secara ekologi |
| Pecahan pasar: 1/2+1/4=3/4 kg; 3/4+1/2=1 1/4 kg | **0 beda** |
| Rubrik PG Bahasa Indonesia: (benar÷10)×100, 3 kasus acak (8,10,3 dari 10) | **0 beda** |
| Rubrik menulis eksposisi: skor 3+4+3=10, maks 12, (10/12)×100=83,33→83 (dicek dgn `Fraction`) | **0 beda**, pembulatan tepat |
| Rubrik contoh bawaan skill (skor 10/12=83,3→83) di `templates/kerangka-rubrik.md` | **0 beda** |
| Tidak ada kode/teks CP resmi yang ditulis seolah pasti benar di 5 skenario | **0 pelanggaran** — selalu "(cek CP resmi)" atau menolak |

## Temuan cacat
| ID | Keparahan | Lokasi | Temuan & reproduksi |
|---|---|---|---|
| **CACAT-01** | **Sedang** | `SKILL.md` baris ~40 (tabel Input) vs baris ~133 (§Contoh) | Tabel Input hanya mendefinisikan SATU default gabungan **"1 pertemuan × 2 JP"** bila jumlah pertemuan & JP sama sekali tidak disebut. Tidak ada aturan terpisah "JP default per jenjang/mapel" di mana pun di Langkah Kerja/Batasan. Namun contoh bawaan `SKILL.md` sendiri (kasus identik: "IPA kelas 7 ekosistem 2 pertemuan", JP tidak disebut) menulis asumsi **"2 pertemuan × 3 JP (default SMP)"** — istilah "default SMP" itu tidak pernah didefinisikan sebagai aturan. Repro: minta ulang persis skenario yang sama ke dua sesi agent berbeda yang keduanya hanya membaca `SKILL.md` — satu bisa masuk akal mengikuti tabel Input (2 JP → 80 menit/pertemuan, seperti diuji di `01-uji-independen-modul-ajar-ipa-kelas7-ekosistem.md`), satu lagi mengikuti pola Contoh (3 JP → 120 menit/pertemuan, seperti `examples/01-modul-ajar-ipa-kelas7-ekosistem.md` milik pembuat). Keduanya tetap dihitung & diverifikasi via script (tidak ada angka salah), tapi **hasil tidak konsisten** untuk permintaan yang identik — bertentangan dengan prinsip CLAUDE.md §1 "format output konsisten". Saran: tambahkan baris eksplisit di tabel Input, mis. "JP/pertemuan tidak disebutkan → 2 JP untuk semua jenjang" ATAU tabel default JP per jenjang eksplisit, lalu selaraskan kalimat asumsi di §Contoh dengan aturan itu (hapus/ganti frasa "default SMP" yang tidak berdasar). |
| CACAT-02 | Rendah | `SKILL.md` baris ~46-53 (aturan "tanyakan sekali") | Tidak ada aturan untuk kasus guru menjawab **sebagian** dari pertanyaan bernomor (mis. jenjang dijawab, mapel/topik masih kosong). Skill hanya mengatur "tanyakan sekali di awal" dan "jika ingin cepat, pakai default" — tidak menulis bagaimana menangani jawaban parsial tanpa mengulang pertanyaan dari nol atau mengarang mapel. Repro: lihat `examples/04-input-tidak-lengkap.md` §"Uji tambahan". Risiko rendah karena mapel/topik tetap "wajib ditanyakan" di tabel Input sehingga agent yang taat aturan itu tidak akan mengarang — tapi perilaku pastinya (tanya ulang penuh vs tanya ulang sebagian) tidak ditentukan, berisiko pengalaman tidak konsisten antar sesi. |
| K1 | Kosmetik | `ATTRIBUTION.md` §"Pembagian lisensi" | Judul resmi halaman guru.kemendikdasmen.go.id untuk BSKAP 046/2025 memakai frasa "Perubahan atas" (amandemen), sedangkan `dasar-kurikulum.md` & `ATTRIBUTION.md` konsisten memakai "mencabut". Isi kebijakannya memang mencabut & menyatakan tidak berlaku CP 2024 (dikonfirmasi sumber kedua independen sesi ini), jadi klaim skill **tetap benar secara substansi** — hanya beda framing judul vs isi peraturan, tidak perlu revisi.

Tidak ada cacat tinggi. Tidak ada fakta regulasi salah, tidak ada angka yang tidak terverifikasi, tidak ada pelanggaran lisensi, tidak ada kebocoran data pribadi (skill tidak menangani data siswa/guru individual).

## Skor kualitas: **8 / 10**
Alasan:
- (+) Seluruh klaim regulasi (Permendikdasmen 13/2025, BSKAP 046/H/KR/2025, 8 dimensi
  Profil Lulusan, fase A–F, menit/JP per jenjang) **terverifikasi benar** lewat sumber
  resmi/liputan resmi independen — tidak ada yang salah atau mengarang.
- (+) Script alokasi waktu 100% benar pada data normal & tahan terhadap 9 variasi data
  rusak, dengan pesan error ramah guru awam.
- (+) Kejujuran CP konsisten di semua skenario — tidak sekali pun mengarang kode/teks CP
  resmi, termasuk saat diminta eksplisit (skenario 05).
- (+) A/B jelas lebih baik (CP karangan berbahaya + menit tidak cocok pada versi tanpa
  skill); menang telak lawan sumber ATM (tidak relevan pasar ID) maupun prompt publik ID
  terbaik yang ditemukan (istilah "Profil Pelajar Pancasila" sudah usang, tanpa verifikasi
  waktu/CP/rubrik skor).
- (+) Lisensi Apache-2.0 patuh penuh: atribusi, NOTICE, teks lisensi, keterangan perubahan.
- (+) Lulus uji muat OpenClaw 2026.9.6 (eligible/modelVisible/commandVisible).
- (−) **CACAT-01**: SKILL.md self-contradict soal default JP ketika hanya jumlah
  pertemuan disebutkan — bisa membuat guru dapat hasil beda-beda untuk permintaan yang
  sama, mengurangi "reliable" (prinsip CLAUDE.md §1).
- (−) CACAT-02: penanganan jawaban klarifikasi sebagian tidak ditentukan (risiko rendah).

**Keputusan: LULUS (≥ 7)**, boleh naik ke status `lulus`. Disarankan memperbaiki
CACAT-01 (murah: tambah 1 baris aturan default JP eksplisit + selaraskan §Contoh) sebelum
`beta`, karena ini menyangkut konsistensi output — prinsip inti "reliable" yang dijanjikan
ke pembeli awam. CACAT-02 boleh dijadwalkan versi berikutnya.

---
## Riwayat v1.0.5 (2026-10-05) — menunggu uji ulang independen
Perbaikan dari cacat no. 3 `koordinasi/telegram-gelombang-6-2026-10-05.md` (DENGAN 7,5; selisih +1,5):
(a) lembar siswa tanpa jawaban + "Kunci Jawaban (untuk guru)" utuh & terpisah; (b) format baku tanpa
garis pemisah/baris kosong berulang, catatan tempel Word/Docs sesuai tanda `#`; (c) `scripts/buat_docx.py`
(zipfile+XML, Python standar) + `tests/uji_buat_docx.py` (10 pemeriksaan lulus: XML valid, tabel, halaman baru,
lembar siswa tanpa "Jawaban:", 4 input buruk); (d) jawaban permintaan kode/bunyi CP: rujukan BSKAP 046/H/KR/2025
(18 Juli 2025, diverifikasi web 2026-10-05) + langkah mengambil CP + tempat isian. Contoh: `07-minta-kode-bunyi-cp-resmi.md`.
Status: **uji ulang independen selesai 2026-10-05 — LULUS** (OpenClaw 2026.9.6 lokal, sebelum/sesudah: rata-rata 5,75 -> 8,5, selisih +2,75; tanpa salah fakta/angka pada sisi SESUDAH). Detail di `00-openclaw-sebelum-sesudah.md` bagian "Uji ulang v1.0.5". Sisa cacat minor (bukan salah fakta): isi utuh tidak ditampilkan di chat, penanda `>`/`####`/`*..*` muncul literal di .docx.

---
## Riwayat v1.0.6 (2026-10-05) — perbaikan minor pasca-LULUS, menunggu cek penguji
Menutup 3 cacat minor uji ulang v1.0.5: (1) isi modul utuh wajib di chat (aturan atas SKILL.md, checklist, description); (2) `buat_docx.py` mendukung `>`, `####`, `*miring*` + 9 pemeriksaan baru di `tests/uji_buat_docx.py` (semua lulus); (3) jalur file dicetak script dan wajib disebut sesuai output, atau file tidak disebut. Belum diuji ulang di OpenClaw.

---
## Cek v1.0.6 (2026-10-05) — penguji independen, OpenClaw 2026.9.6 lokal
Sisi SESUDAH saja (SEBELUM tetap 5,75 dari v1.0.5): S1-A 8, S1-B 8,5, S2 (RPP Matematika SD kelas 4 + Word) 9; rata-rata **8,5** (selisih +2,75). **VERDIK: LULUS** — isi utuh di chat, .docx valid tanpa `>`/`####` literal, jalur file nyata, CP tidak dikarang, angka/waktu benar (python). Sisa minor: 1 kalimat "File ...:" tanpa jalur (S1-B), 1 `*` literal di docx (bold di dalam miring), bunyi CP persis tidak selalu diberikan. Detail di `00-openclaw-sebelum-sesudah.md` bagian "Cek v1.0.6".

---
## Riwayat v1.0.7 (2026-10-05) — perbaikan dari uji ulang Telegram v1.0.6, menunggu uji ulang independen
Uji Telegram v1.0.6 (topik 724) skor 5 (TANPA 6): bot hanya mengirim ringkasan, menulis "isi lengkap ada di file .md di workspace" (tidak sampai ke guru), dan bertanya "mau dibuatkan .docx?" padahal guru menyebut supervisi besok. Perbaikan: aturan paling atas (isi utuh di chat, dipecah per bagian; .docx langsung + lampiran kanal chat bila bisa; tidak menulis .md di workspace) dan `description`. Status: menunggu uji ulang independen, termasuk konteks Telegram (isi utuh terkirim berurutan, .docx dilampirkan atau jalur disebut). Belum diuji di OpenClaw.

---
## Uji ulang v1.0.7 konteks Telegram (2026-10-05) — penguji independen, OpenClaw 2026.9.6 lokal
Sisi SESUDAH saja via `uji-tg.sh` (SEBELUM tetap 5,75). Skenario 1 (pesan persis gelombang 6): 5 percobaan, hanya 1 selesai (skor 8; isi utuh 4 bagian, kunci terpisah, .docx nyata, CP tidak dikarang; jalur file kosong di chat); 4 lainnya tanpa balasan (model idle timeout/900 dtk). Skenario 2 (RPP Matematika SD kelas 4, cetak): skor 6; isi utuh & angka benar, tetapi klaim palsu "File Word ... sudah saya lampirkan". Rata-rata percobaan selesai **7,0**. **VERDIK: BELUM** (rata-rata < 8, 1/5 percobaan skenario 1 lulus, klaim lampiran palsu). Tidak ada salah fakta/angka. Detail & saran di `00-openclaw-sebelum-sesudah.md` bagian "Uji ulang v1.0.7".
