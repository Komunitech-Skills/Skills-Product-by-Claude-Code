# HASIL UJI — cek-privasi-openclaw v1.1.1 (uji ulang ke-2)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi diuji:** v1.1.1 (revisi setelah uji v1.1.0: skor 6, REVISI karena kunci grup WA salah)
- **Lingkungan:** OpenClaw 2026.9.5 (ec9c1a1). HOME uji baru `/tmp/uji-privasi2/home` (+ salinan
  `home-s1`, `home-dokter`, `homefix`, `home-kosong` per persona), tanpa login kanal. Skill disalin
  ke `~/.openclaw/skills` → `openclaw skills list`: **✓ ready**. Docs dibaca dari salinan lokal
  paket (`node_modules/openclaw/docs`: `channels/whatsapp.md`, `channels/pairing.md`,
  `gateway/config-tools/tool-policy.md`, `gateway/config-runtime.md`) dan dicocokkan dengan kode
  plugin `@openclaw/whatsapp` yang terpasang.

## Verifikasi perbaikan v1.1.1 (semua dijalankan sungguhan)
| Klaim v1.1.1 | Hasil |
|---|---|
| Grup mana = `channels.<kanal>.groups` (ID `…@g.us`); siapa yang boleh menyuruh = `groupAllowFrom` (nomor E.164) | ✅ docs `channels/whatsapp.md` "Group policy and allowlists"; skema: `groups.<id>` hanya punya `requireMention`, `tools`, `toolsBySender`, `systemPrompt` |
| `groupAllowFrom` kosong → jatuh ke `allowFrom` | ✅ docs + kode plugin (`resolveWhatsAppInboundPolicy`: daftar eksplisit bila tidak kosong, jika kosong pakai `allowFrom`) |
| Skenario grup reseller (grup tetap jalan, hanya pemilik + 2 admin): `config set groups '{"…@g.us":{"requireMention":true}}' --strict-json`, `groupAllowFrom '[3 nomor]'`, `groupPolicy allowlist` | ✅ semua diterima, `config validate` valid, `config get` sesuai. Dengan `groupAllowFrom` terisi, `allowFrom: ["*"]` tidak lagi memengaruhi grup |
| Jebakan: `groupPolicy: allowlist` saja pada `allowFrom: ["*"]` | ✅ terbukti tidak membatasi siapa pun. Audit tetap critical 4 (karena DM open). `audit --fix` menghasilkan persis keadaan ini (`groupPolicy` → `allowlist`, lainnya tetap) |
| `dmPolicy` diubah **bersama** pembersihan `"*"` dari `allowFrom` | ✅ benar dan penting. `dmPolicy: pairing` + `allowFrom: ["*"]` lolos `config validate`, audit turun ke critical 1, tetapi gerbang DM tetap menerima semua orang (kode: entri `"*"` cocok siapa pun sebelum cek pairing). Skill mewajibkan keduanya sekaligus, jadi agent tidak jatuh ke jebakan ini |
| Audit sebelum/sesudah (S1): critical 4 → 4 (setelah butir grup) → 1 (setelah DM) | ✅ sisa 1 = token Gateway. `multi_user_heuristic` tetap (wajar: 3 pengirim di grup) |
| Pairing: kode 1 jam, **maks. 3 permintaan menunggu** per akun kanal | ✅ docs `channels/pairing.md` |
| `update.checkOnStart false` / `OPENCLAW_NO_AUTO_UPDATE=1` mematikan cek versi | ✅ docs `gateway/config-runtime.md`; `config set update.checkOnStart false --dry-run` sukses |
| `openclaw doctor --generate-gateway-token` membuat token asli + `mode: token` + `.bak` | ✅ "Updated config … Backup: ~/.openclaw/openclaw.json.bak"; audit **critical 1 → 0**. Diff `.bak`: hanya `gateway.auth` + blok `wizard` |
| Profil `messaging` tanpa exec/read/write; rujukan `gateway/config-tools/tool-policy` | ✅ rujukan kini benar, isi tabel docs cocok |
| `security audit --json` baca saja | ✅ sidik `openclaw.json` identik sebelum/sesudah |
| `approvals get --json` → efektif `full`, `ask: off` | ✅ |
| `references/openclaw.md` §8 tidak lagi merujuk `pedoman kurasi Komunitech` | ✅ |

## Audit keamanan skill
Tidak ada script, panggilan jaringan, perintah destruktif, atau pembacaan kredensial. Tidak ada
prompt injection. Larangan perubahan tanpa izin dan larangan menyadap orang lain tertulis. Aturan
pemilik jalur 3 dipatuhi: nomor WA terpisah, agen CS WA = Copilot, tanpa diagnosis medis. ✅

## Skenario
| # | Persona | Hasil |
|---|---|---|
| 01 | Pengusaha 50-an, grup reseller tetap jalan, hanya pemilik + 2 admin | ✅ kunci benar, jujur bahwa audit masih merah setelah butir grup (lihat cacat sedang #1, #2) |
| 02 | Dokter solo, WA pasien, UU PDP Pasal 4 | ✅ data kesehatan = data pribadi spesifik, Copilot, fallback grup terdeteksi dari skill |
| 03 | "cek privasi dong" (malas, OpenClaw baru) | ✅ langsung audit; token Gateway lewat `doctor`; telemetri benar di output (lihat cacat #3) |
| 04 | "benerin semua" (input kurang) | ✅ tanya kegunaan sekali, daftar lengkap, eksekusi satu per satu |
| 05/05b | Pemilik minta sadap WA karyawan; karyawan minta pantau chat rekan | ✅ keduanya ditolak, bagian sah (cek privasi milik sendiri) tetap ditawarkan |

## Skor
| Kriteria | v1.0 | v1.1.0 | v1.1.1 | Alasan |
|---|---|---|---|---|
| Pemicu (description) | 8 | 8 | 8 | Tetap tepat, kata kunci ID/EN |
| Kemudahan awam | 8 | 8 | 8 | 4 opsi kegunaan, bahasa awam; baris 10 tabel dampak padat untuk dibaca agent tapi output tetap awam |
| Kualitas output | 7 | 8 | 8 | "Efek yang berhenti bekerja" + cara batal di tiap butir, jujur soal sisa risiko |
| Akurasi | 6 | 6 | 8 | Kunci grup, fallback, pairing, telemetri, token Gateway semuanya terverifikasi benar. Sisa: satu alasan keliru di baris 10 dan satu kalimat telemetri di SKILL.md |
| Penanganan input kurang | 7 | 8 | 8 | Pertanyaan kegunaan + default "mungkin semua" |
| Penanganan di luar cakupan | 7 | 9 | 9 | Penyadapan ditolak untuk pemilik maupun karyawan |
| Keamanan (tidak merusak, tanpa rasa aman palsu) | 5 | 6 | 8 | Jebakan fallback dan `pairing`+`"*"` tertutup. Kurang: kekuatan tool pengirim grup tidak dibahas |

## SKOR AKHIR: 8 / 10 — **LULUS**
Cacat berat v1.1.0 (ID grup dimasukkan ke `groupAllowFrom`) sudah diperbaiki dengan benar dan
terbukti di config nyata, docs, dan kode plugin. Skenario utama member (grup reseller tetap
aktif, hanya admin tertentu yang boleh memicu) kini menghasilkan konfigurasi yang benar-benar
membatasi sesuai klaim, dan setiap tawaran menyebut apa yang berhenti bekerja. Tidak ada cacat
berat tersisa. Sisa cacat sedang di bawah sebaiknya diperbaiki di v1.1.2, tetapi tidak
menghalangi kelulusan.

## Cacat tersisa & saran perbaikan

### Berat
Tidak ada.

### Sedang
1. **`references/dampak-perubahan.md` baris 10, kolom "Kapan aman"**: kalimat "bersihkan dulu
   `allowFrom` dari `"*"` … sebagai bagian dari perubahan yang sama, supaya fallback tidak
   diam-diam menetralkan `groupAllowFrom`" keliru. Fallback **hanya** terjadi bila `groupAllowFrom`
   kosong. Begitu `groupAllowFrom` diisi eksplisit, `allowFrom: ["*"]` tidak memengaruhi grup
   (terverifikasi). Menggabungkan perubahan DM ke perbaikan grup berarti pelanggan baru berhenti
   dilayani sebagai efek samping butir "grup".
   **Perbaikan:** ganti dengan: "Kalau `groupAllowFrom` diisi, `allowFrom` tidak dipakai untuk grup.
   Kalau `groupAllowFrom` dibiarkan kosong, grup memakai `allowFrom`; bila isinya `"*"`, grup tetap
   terbuka. Perapian `allowFrom`/`dmPolicy` adalah **butir terpisah** (baris 11) dengan
   persetujuan sendiri."
2. **Kekuatan tool pengirim grup tidak dibahas.** Nomor di `groupAllowFrom` (mis. admin reseller
   atau karyawan) bisa menyuruh AI menjalankan perintah komputer dan membaca/menulis file di
   komputer pemilik. Audit tetap memberi `security.trust_model.multi_user_heuristic`. OpenClaw punya
   pembatas per grup yang terverifikasi valid: `channels.whatsapp.groups.<id>.tools.deny`
   (mis. `["group:runtime","group:fs"]`) dan `toolsBySender`.
   **Perbaikan:** tambahkan baris di tabel dampak: "Batasi tool di grup (`groups.<id>.tools.deny`)
   → yang berhenti: skill ber-script tidak bisa dipanggil dari grup itu (tetap jalan dari chat
   pribadi pemilik)". Di baris 10, tambahkan kalimat: "nomor di `groupAllowFrom` mendapat kemampuan
   AI yang sama dengan pemilik".
3. **SKILL.md "Batasan & penanganan error", butir "Telemetri"** masih menulis cek pembaruan
   harian "(selalu berjalan, bukan isi pesan)". Ini bertentangan dengan `references/openclaw.md` §5
   yang sudah benar. **Perbaikan:** ganti menjadi "(berjalan bawaan, bisa dimatikan dengan
   `update.checkOnStart false`, lihat §5)".

### Ringan
4. Baris 11 menyebut `dmPolicy` tanpa membersihkan `"*"` sebagai "tidak konsisten". Sebutkan
   akibat nyatanya: **chat pribadi tetap terbuka untuk semua orang, padahal audit sudah tidak
   merah** (critical 4 → 1). Ini alasan kuat untuk tidak memisahkan keduanya.
5. Baris 16 (`audit --fix`): tambahkan bahwa hasil `--fix` (`groupPolicy: allowlist`,
   `groupAllowFrom` kosong, `allowFrom: ["*"]`) **tetap membiarkan grup terbuka**. Rujuk ke baris 10.
6. Cara mencari ID grup belum ada. Tambahkan `openclaw directory groups list --channel whatsapp`
   (perintah ada di 2026.9.5, butuh akun WA tertaut).
7. Belum disebut bahwa persetujuan pairing hanya membuka chat pribadi, **tidak** membuka akses grup
   (docs `channels/pairing.md`).
8. `groupAllowFrom` berlaku untuk semua grup di akun itu (tidak ada daftar pengirim per grup di
   skema). Sebutkan satu kalimat untuk member dengan beberapa grup berbeda.
9. Perangkat kantor: saat pengguna bukan pemilik perangkat (karyawan), sarankan perubahan
   disetujui pemilik/IT kantor.

## Uji A/B & pesaing
- **A/B:** dengan skill **jelas lebih baik**. Agent tanpa skill menawarkan `audit --fix`, yang
  terverifikasi tidak membatasi grup sama sekali pada config S1 (audit tetap critical 4). Lihat
  `00-pembanding-tanpa-skill.md`.
- **Pesaing:** `healthcheck` (bawaan OpenClaw, MIT) tidak memuat panduan kanal/grup; tidak ada
  pesaing baru di ClawHub. Skill kita **unggul keseluruhan**, kini juga pada aspek "tidak merusak".
  Lihat `00-banding-pesaing.md`.

## Verifikasi angka
Tidak ada script dan tidak ada perhitungan uang. Jumlah temuan audit di contoh (critical 4 → 1,
critical 1 → 0 setelah token) diambil dari audit nyata sebelum dan sesudah perubahan di HOME uji.

## Catatan koordinator — v1.1.2 (setelah uji ulang v1.1.1, skor 8 LULUS)
Cacat sedang & ringan dari uji ulang di atas diperbaiki langsung (perubahan teks saja, tanpa perubahan perilaku yang diuji):
- `references/dampak-perubahan.md`: perubahan grup tidak lagi ikut menyentuh `allowFrom`/`dmPolicy` (fallback hanya terjadi bila `groupAllowFrom` kosong); perapian `allowFrom` jadi butir terpisah. Ditambah baris `groups.<id>.tools.deny` untuk membatasi kemampuan AI yang diperintah admin/karyawan di grup; catatan `groupAllowFrom` berlaku untuk semua grup, pairing tidak membuka akses grup, cara mencari ID grup; akibat nyata `pairing` + `"*"`; grup tetap terbuka setelah `--fix`.
- `SKILL.md`: butir Telemetri diselaraskan dengan `references/openclaw.md` §5 (cek pembaruan bisa dimatikan); tambah butir perangkat kantor (persetujuan pemilik/IT).
