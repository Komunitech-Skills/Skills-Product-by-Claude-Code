# Skenario 04 — Input tidak lengkap — "bikin RPP buat besok"

## Input pengguna
> "bikin RPP buat besok"

## Langkah yang diikuti
Mapel/topik **tidak disebut** dan jenjang/kelas **tidak disebut** — keduanya wajib
("Wajib: Ya — tanyakan", tidak ada default) di tabel Input `SKILL.md`. Sesuai aturan:
"Jika mapel/topik atau jenjang tidak disebut, tanyakan **sekali** dalam satu pesan
bernomor, sekaligus tawarkan opsi cepat." Skill **tidak** boleh menebak mapel/topik
sendiri (beda dengan JP/pertemuan yang memang punya default eksplisit).

## Output (satu pesan, tidak lebih)

```
Baik, saya bantu buatkan RPP untuk besok. Supaya cepat dan pas, tolong jawab 3 hal ini
(boleh singkat):

1. Mapel & topiknya apa? (mis. "Matematika, pecahan" atau "IPA, ekosistem")
2. Untuk kelas/jenjang berapa? (mis. "SD kelas 4" atau "SMP kelas 8")
3. Berapa pertemuan & JP? — boleh dijawab "1 saja" atau "langsung pakai default 1
   pertemuan 2 JP" kalau kamu terburu-buru.

Kalau kamu benar-benar buru-buru dan belum tahu jawabannya, cukup balas "buatkan saja
contoh umum" — nanti saya pakai topik & jenjang paling umum sebagai contoh, tapi hasilnya
kurang pas dipakai langsung karena saya tidak tahu kelas dan topik yang sebenarnya kamu
ajarkan besok.
```

## Verifikasi kepatuhan
| Aturan SKILL.md | Terpenuhi? |
|---|---|
| Tanya **sekali** (bukan bertahap 3 pesan terpisah) | ✓ satu pesan, 3 pertanyaan bernomor |
| Tawarkan opsi cepat/default | ✓ opsi "1 saja"/"default 1 pertemuan 2 JP" untuk pertanyaan 3 |
| Tidak menebak mapel/topik/jenjang sendiri | ✓ — tidak ada yang bisa didefault untuk 2 info wajib ini |
| Tidak memberi Modul Ajar generik yang mengarang mapel | ✓ — skill dengan jujur bilang hasil "contoh umum" kurang pas dipakai |

## Uji tambahan — bila guru menjawab singkat "terserah, yang penting cepat"
Simulasi lanjutan: pengguna membalas "terserah, kelas 5 SD aja, cepetan". Mapel/topik
**masih** tidak disebut (hanya jenjang yang dijawab). Sesuai SKILL.md, mapel/topik tetap
wajib — skill **seharusnya** menanyakan ulang HANYA butir yang masih kosong (mapel/topik),
bukan mengulang ke-3 pertanyaan dari awal, dan bukan pula mengarang mapel sendiri. SKILL.md
tidak menulis eksplisit aturan "tanya ulang hanya bagian yang kosong" untuk kasus jawaban
sebagian — ini **celah kecil** (tidak dites `SKILL.md` bagaimana menangani jawaban
sebagian), tapi perilaku paling aman & sesuai prinsip "tanya sekali, jangan mengarang info
wajib" tetap: tanya ulang singkat "Mapel & topiknya apa, Bu/Pak? (kelas 5 SD sudah
dicatat)" — bukan pertanyaan bernomor lengkap lagi, dan bukan asumsi mapel sembarangan.

## Penilaian
**Lulus untuk kasus utama** (mapel+jenjang sama sekali tidak disebut) — skill mengikuti
instruksi "tanya sekali dalam satu pesan bernomor + opsi cepat" dengan tepat, tidak
langsung mengarang Modul Ajar acak. **Cacat rendah**: SKILL.md tidak punya aturan
eksplisit untuk kasus jawaban SEBAGIAN (mis. jenjang dijawab, mapel masih kosong) —
berisiko agent lain menafsirkan beda (mengulang 3 pertanyaan dari nol, atau malah menebak
mapel karena mengira "sudah pernah tanya"). Lihat CACAT-04 di `HASIL-UJI.md`.
