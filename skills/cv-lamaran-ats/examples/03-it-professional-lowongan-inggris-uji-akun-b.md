# Skenario 3 (Akun B) — Normal: Profesional IT Melamar Posisi Berbahasa Inggris (Perusahaan Asing)

## Input pengguna
```
Saya IT professional, ada lowongan bahasa Inggris dari perusahaan asing, tolong bantu:

Backend Engineer (Remote, Singapore HQ)
Requirements:
- 3+ years experience in backend development
- Proficient in Python or Go, and SQL databases
- Experience with REST API design and microservices
- Familiar with Docker and CI/CD pipelines
- Good written English for async communication with global team
- Bachelor's degree in Computer Science or related field

Data saya: Farhan Ramadhan, Jakarta, 0821xxxxxxx, farhan.dev@email.com,
linkedin.com/in/farhanramadhan. S1 Teknik Informatika, lulus 2019. Backend
Engineer di PT Teknologi Maju (2020-sekarang): bangun REST API pakai Python
(Django/FastAPI), pakai PostgreSQL, deploy pakai Docker, ikut setup CI/CD
GitHub Actions. Pernah kerja remote dengan tim campuran WNI/asing, komunikasi
tertulis Inggris rutin. Belum pernah pakai Go. Ekspektasi gaji 25 juta.
```

## Output (ringkas)
```
## Evaluasi Kecocokan Lowongan: Backend Engineer di [perusahaan tidak disebutkan
nama resminya di teks lowongan] (HQ Singapura, remote)
**Saringan wajib:** LULUS — S1 Teknik Informatika sesuai "related field"; lokasi
remote sesuai; gaji tidak dicantumkan lowongan → "belum diketahui, tanyakan saat
proses" (kompensasi lintas negara/HQ asing sering dibahas terpisah di tahap
wawancara, disebutkan sebagai catatan tambahan ke pengguna).

| Dimensi | Skor | Catatan |
|---|---|---|
| Keahlian & alat kerja | 85/100 | Python, SQL (PostgreSQL), REST API, Docker, CI/CD semua ada; Go belum dikuasai (lowongan minta "Python OR Go" — salah satu cukup) |
| Pengalaman | 90/100 | 4+ tahun backend, di atas syarat 3+ tahun, fungsi kerja persis sama |
| Preferensi & arah karier | — | Belum cukup data, tidak dinilai |
| Syarat administratif | 100/100 | S1 Informatika sesuai |

**Skor akhir (dihitung dari 3 dimensi yang tersedia, bobot 35/30/15 dinormalisasi
ke total 0,80): (85×0,35 + 90×0,30 + 100×0,15) / 0,80 = (29,75+27+15)/0,80 =
71,75/0,80 = 89,7 → 90/100 — Sangat cocok**
### Kenapa cocok: hard requirement teknis terpenuhi lewat "Python ATAU Go"
(pengguna kuat di Python), kecuali microservices yang belum tercatat di data pengguna;
pengalaman remote lintas negara & komunikasi Inggris tertulis sudah biasa dijalani.
### Celah: belum pernah pakai Go — tidak fatal karena lowongan bersifat "or";
pengalaman microservices belum disebut — tanyakan dulu, jangan dicantumkan bila belum pernah.
### Rekomendasi: Lamar segera — kecocokan sangat kuat.

## CV Versi ATS (Bahasa Inggris — mengikuti bahasa lowongan)
Farhan Ramadhan
Jakarta, Indonesia · +62 821xxxxxxx · farhan.dev@email.com ·
linkedin.com/in/farhanramadhan

PROFESSIONAL SUMMARY
Backend Engineer with 4+ years of experience building REST APIs
using Python (Django/FastAPI) and PostgreSQL, with hands-on experience in Docker
and CI/CD (GitHub Actions). Comfortable working remotely with distributed,
international teams and communicating in written English.

WORK EXPERIENCE
Backend Engineer — PT Teknologi Maju (2020-Present)
- Built and maintained REST APIs using Python (Django/FastAPI) for production services
- Worked with PostgreSQL for data storage [isi hanya bila benar-benar Anda kuasai:
  query optimization]
- Deployed services using Docker and contributed to CI/CD pipeline setup (GitHub Actions)
- Collaborated remotely with a mixed Indonesian/international team, communicating
  in written English

EDUCATION
Bachelor's Degree, Informatics Engineering — [nama universitas belum diisi
pengguna, ditandai [belum diisi]] (2019)

SKILLS
Python (Django, FastAPI), SQL/PostgreSQL, REST API design, Docker, CI/CD
(GitHub Actions), written English for async communication
[isi hanya bila benar-benar Anda kuasai: microservices]
[Go TIDAK dicantumkan — pengguna belum pernah pakai]

## Cover Letter (English, formal) + Short Email
(disusun, menyebut 4+ tahun pengalaman relevan, mengakui tidak menyembunyikan
belum pernah pakai Go tapi kuat di Python sebagai alternatif yang diminta lowongan)

## Checklist
- [x] Bahasa CV mengikuti bahasa lowongan (Inggris), sesuai Input SKILL.md
- [x] Go tidak dicantumkan sebagai skill yang dimiliki
- [x] "Microservices" dan "query optimization" (dari lowongan/karangan, tidak ada di
      data pelamar) tidak diklaim — dijadikan isian `[...]` untuk dikonfirmasi
- [x] Ekspektasi gaji 25 juta dari isian pengguna, tidak dibandingkan dengan
      kisaran pasar yang dikarang (skill tidak mengakses data gaji real-time)
- [x] Tidak ada NIK/agama/status pernikahan/foto
```

## Catatan penguji (audit contoh 2026-10-13)
- **Skill tidak boleh memasukkan keahlian/pengalaman yang tidak dimiliki pelamar.**
  Versi awal contoh ini menulis "microservices" (diambil dari lowongan) di ringkasan
  dan "query optimization" di pengalaman, padahal data pelamar hanya menyebut REST
  API Python (Django/FastAPI), PostgreSQL, Docker, dan CI/CD GitHub Actions. Kini
  diganti `[isi hanya bila benar-benar Anda kuasai: ...]` (SKILL.md Langkah 5 &
  checklist "tidak dikarang").
- Skor akhir dihitung ulang dengan rumus bobot `references/evaluasi-kecocokan.md`:
  89,6875 → 90/100, **tidak berubah** setelah perbaikan (skor Keahlian 85 sejak awal
  tidak menghitung microservices). Skill ini tidak punya script untuk skor evaluasi.

## Verifikasi manual (uji awal Akun B)
- Perhitungan skor akhir dicek ulang: (85×0,35+90×0,30+100×0,15)/0,80 = 89,69 →
  dibulatkan 90. **Cocok** dengan yang ditulis di atas (berbeda dari Skenario 2
  yang salah hitung — lihat catatan di file skenario 2).
- Bahasa lowongan Inggris diikuti untuk CV & cover letter sesuai default Input
  ("Ikuti bahasa lowongan") — **fitur ini teruji benar**.
- Nama perusahaan tidak disebut eksplisit di teks lowongan simulasi — agent
  (simulasi) menuliskan apa adanya "tidak disebutkan" alih-alih mengarang nama
  perusahaan, sesuai prinsip tidak mengarang.
