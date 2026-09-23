# 00 — Uji banding pesaing (S1)

Dicari 2026-09-23 oleh agent penguji independen (simulasi, Claude Code). Isi pesaing dibaca lewat raw.githubusercontent.com;
**tidak ada script pihak ketiga yang dijalankan** dan tidak ada teks pesaing yang disalin ke skill kita.

## Pencarian
| Sumber | Kata kunci / jalur | Hasil |
|---|---|---|
| Web search | `SKILL.md whatsapp broadcast message skill github`; `"SKILL.md" broadcast WhatsApp promosi pelanggan UMKM skill` | 2ChatCo/agent-skills, Whatsable/whatsapp-business-agent-skills (Notifyer), abdul-haadi/chatdaddy-agent-skills (`send-broadcast`), eddmann/whatsapp-cli, serejaris/kimi-skills (whatsapp-integration); sisanya artikel blog, bukan skill |
| github.com/VoltAgent/awesome-openclaw-skills | grep README: whatsapp, broadcast, bulk message, opt-out | Hanya skill memori/enkripsi yang menyebut WhatsApp; tidak ada skill penulisan broadcast |
| github.com/anthropics/skills | pohon repo | Tidak bisa dibuka lewat API di sesi ini (403 — sesi dibatasi ke repo yang dikonfigurasi); pencarian web tidak menemukan skill broadcast/WA di sana |
| ClawHub / skills.sh | lewat pencarian web | Hanya Notifyer (WhatsAble) — alat operasional API, perlu login & token |
| manairalabs/bicara-skills (MIT) | README | `invoice-extract-id`, `wa-reply-id` (balas chat CS satu pelanggan) — **bukan** broadcast; lebih dekat ke `balas-chat-cs` |
| alvinindra/bahasa-skills | README + `skills/bahasa-marketing/SKILL.md` | Skill copywriting pemasaran bahasa Indonesia (caption, iklan, email blast, naskah promo). Tidak khusus WA, tanpa script |

**Pesaing yang dipakai untuk banding:**
1. **ChatDaddy `send-broadcast`** — https://github.com/abdul-haadi/chatdaddy-agent-skills/blob/main/skills/send-broadcast/SKILL.md
   (lisensi: file LICENSE tidak ditemukan di root → anggap *all rights reserved*). Paling dekat secara **tugas** (broadcast WA).
2. **bahasa-skills `bahasa-marketing`** — https://github.com/alvinindra/bahasa-skills/blob/main/skills/bahasa-marketing/SKILL.md
   (lisensi: file LICENSE tidak ditemukan di root; plugin.json tanpa lisensi). Paling dekat secara **konteks Indonesia & mutu copy**.

Notifyer/2Chat tidak dibandingkan: keduanya adalah pembungkus API berbayar yang butuh akun & kredensial (tidak cocok untuk
pembeli awam, dan menjalankan script-nya dilarang oleh brief).

## Input S1 (sama persis dengan 01 & 00-pembanding)
> Tolong bikinin broadcast WA buat pelanggan toko roti saya, Roti Hangat Mbak Sri di Solo. Promo gajian 25-30 September: roti sobek cokelat 25rb jadi 20rb, terus roti manis beli 2 gratis 1. Order tinggal bales chat, bisa diantar buat area Laweyan. Aku ada file pelanggan.csv, mulai kirim Jumat 25 Sept jam 10 pagi ya. Yang udah bilang stop aku taruh di stop.txt.

## Output pesaing 1 — agent yang memuat ChatDaddy `send-broadcast`
```
Siap! Sebelum saya jalankan broadcast di ChatDaddy, saya perlu:
1. CAMPAIGN_NAME — nama kampanye, mis. "Promo Gajian Sept 2026"
2. AUDIENCE_TAG — tag kontak di ChatDaddy yang dituju (mis. "customer")
3. Pastikan kamu sudah login ke https://app.chatdaddy.tech di Chrome.

Catatan: file pelanggan.csv dan stop.txt tidak bisa saya pakai langsung — kontak harus sudah ada di
ChatDaddy dengan tag. Draf pesan:

Hi {{name}}! Promo gajian Roti Hangat Mbak Sri 25–30 September: roti sobek cokelat Rp20.000 (dari Rp25.000),
roti manis beli 2 gratis 1. Order balas chat ini, bisa diantar area Laweyan.

Jadwal: 2026-09-25 10:00. Sebelum kirim saya akan berhenti dan menampilkan jumlah penerima untuk kamu konfirmasi.
```
(Langkah berikutnya menurut skill itu: membuka Chrome, membuat kampanye, memilih tag, menjadwalkan, lalu *kirim* — di luar
kemampuan & keinginan pembeli kita, dan butuh akun ChatDaddy.)

## Output pesaing 2 — agent yang memuat `bahasa-marketing` (+ `bahasa-inti`)
```
Roti sobek cokelat Rp20 ribu, cuma sampai 30 September.

Halo, Kak. Gajian kali ini, Roti Hangat Mbak Sri kasih harga khusus: roti sobek cokelat dari Rp25 ribu jadi Rp20 ribu,
dan roti manis beli 2 gratis 1. Berlaku 25–30 September.

Tinggal balas chat ini untuk pesan. Kalau kamu di Laweyan, kami antar.
```
(Satu pesan, satu sapaan, hook di baris pertama, satu CTA, tanpa superlatif/urgensi palsu. Skill ini tidak membahas
file kontak, stop.txt, persetujuan, opt-out, atau jadwal.)

## Output skill kita (broadcast-wa v1.0.1)
Lihat `01-promo-gajian-toko-roti-dengan-csv.md`: 3 variasi personal `{sapaan} {nama}` + versi daftar siaran, teks berhenti
di setiap variasi, jadwal bertahap yang menghindari salat Jumat, `broadcast_siap.csv` (25 dari 40 kontak — hanya yang setuju,
tanpa yang berhenti/dobel/rusak, terverifikasi independen) dengan link wa.me per kontak, dan checklist UU PDP.

## Tabel penilaian (1–10)
| Aspek | ChatDaddy `send-broadcast` | `bahasa-marketing` | **broadcast-wa v1.0.1** |
|---|---|---|---|
| Kualitas pesan | 5 — satu draf datar, "Hi {{name}}" | **9** — copy rapi, hook kuat, bebas klise | 8 — 3 variasi natural; V2 mencampur sapaan ("Bu …" lalu "Kamu menerima …") |
| Kesesuaian konteks Indonesia | 3 — Inggris, tanpa UU PDP, tanpa sapaan lokal | 8 — ragam & sapaan Indonesia tepat, EPI | **9** — sapaan Bu/Pak/Mbak/Teh/Koh, UU PDP, salat Jumat, WIB/WITA/WIT |
| Akurasi (angka/fakta) | 7 — angka benar | 8 — angka benar, tanpa klaim tambahan | **9** — angka persis; daftar kirim 25/40 & 26/55 (uji nakal) identik dengan hitungan penguji |
| Kepatuhan izin & opt-out | 2 — tidak ada opt-out, tidak menyaring persetujuan (hanya konfirmasi jumlah penerima) | 1 — tidak dibahas | **8** — opt-out wajib & dicek script, filter persetujuan/berhenti; celah: daftar berhenti bercatatan diabaikan (B3) |
| Siap pakai untuk awam | 3 — butuh akun ChatDaddy + Chrome + tag kontak | 5 — teks siap tempel, sisanya manual | **9** — teks + file berisi jadwal & link wa.me, tanpa akun apa pun |
| **Keseluruhan** | 3 | 6 | **8** |

**Kesimpulan:** skill kita **menang secara keseluruhan**. `bahasa-marketing` lebih unggul pada mutu kalimat satu pesan,
tetapi tidak menyentuh inti tugas broadcast (izin, berhenti, daftar kirim, jadwal). ChatDaddy unggul pada satu kebiasaan
keselamatan (konfirmasi jumlah penerima sebelum kirim) tetapi bergantung pada platform berbayar dan tidak punya opt-out.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
- **Satu materi satu sapaan** (bahasa-marketing): variasi yang memakai `{sapaan}` ("Bu Sri") jangan ditutup dengan "Kamu
  menerima pesan ini …" — ganti rumusan teks berhenti ke bentuk tanpa kata ganti atau `{sapaan}` (SKILL.md contoh Variasi 2
  dan `references/aturan-pdp-wa.md` §5 butir 3).
- **Hook di baris pertama** & "uji tempel logo kompetitor" (bahasa-marketing): minta minimal satu variasi membuka dengan
  fakta promo paling spesifik (harga/tenggat), bukan salam saja.
- **Konfirmasi jumlah penerima sebelum menyerahkan file** (ChatDaddy): agent menyebut "26 kontak akan dikirimi, 29 dilewati
  — sudah sesuai?" dan menyoroti baris bernilai tidak baku sebelum pengguna mulai klik link.
- **Segmentasi dengan tag** (ChatDaddy): opsi menyaring kolom (mis. `--filter "Kota=Solo"`) agar promo antar-area hanya ke
  area yang relevan.
