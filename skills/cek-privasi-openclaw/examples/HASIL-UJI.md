# HASIL UJI — cek-privasi-openclaw v1.1.0 (uji ulang)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi diuji:** v1.1.0 (revisi setelah uji v1.0: skor 6, REVISI)
- **Lingkungan:** OpenClaw 2026.9.5 (ec9c1a1), **HOME uji baru** `/tmp/uji-vip/home-v11` + salinan
  config persona di `/tmp/uji-cek-privasi-openclaw/` (berisiko, dokter, borongan), tanpa login
  kanal. Skill dipasang dengan `openclaw skills install ./cek-privasi-openclaw --global` →
  Ready, visible, available as command.

## Verifikasi perintah & kunci config (ulang)
| Perintah / klaim v1.1.0 | Hasil |
|---|---|
| `openclaw security audit --json` baca saja | ✅ sidik `openclaw.json` identik sebelum dan sesudah |
| `findings[]`: `remediation` opsional, ada `checkId` | ✅ sesuai koreksi |
| `config get` path belum diatur → exit 1 "valid but unset" | ✅ persis |
| `openclaw approvals get --json` → nilai efektif bawaan `full`/`ask: off` | ✅ |
| `openclaw approvals pending` butuh Gateway | ✅ (gagal tanpa kredensial Gateway, sesuai tulisan skill) |
| `openclaw sandbox explain` → `mode: off` | ✅ |
| Semua path di tabel references §2 + `gateway.auth.mode`, `channels.whatsapp.groupAllowFrom`, `channels.whatsapp.groups` | ✅ valid di skema |
| `gateway.auth.mode` → "Restart the gateway to apply." | ✅ dicetak OpenClaw persis |
| `config set/unset --dry-run`, `.bak` otomatis, `openclaw backup create` (+`--dry-run`) | ✅ |
| `openclaw memory forget --session … --dry-run` (+ `--participant`, `--hook-source`, `--since`) | ✅ jalan, "Dry run: no memory files… were changed" |
| `audit --fix` mengubah `groupPolicy` | ✅ (terverifikasi di uji v1.0, kini ditulis benar) |
| `exec.mode → ask` menolak automation tanpa klien approval | ✅ kutipan docs cocok |
| Profil `messaging` tanpa exec/read/write | ✅ isinya benar. Rujukan docs keliru: ditulis `tools/permission-modes`, seharusnya `gateway/config-tools/tool-policy` |
| Kode pairing berlaku 1 jam | ✅ (docs `channels/pairing.md`). Batas **3 permintaan menunggu** belum disebut |
| Telemetri: cek versi harian "selalu berjalan, bukan bagian yang bisa dimatikan" (§5) | ❌ docs `gateway/config-runtime.md`: `update.checkOnStart: false` / `OPENCLAW_NO_AUTO_UPDATE=1` menghentikannya (path valid) |
| Dampak `groupPolicy open → allowlist`: "tambahkan **ID grup** ke `groupAllowFrom`" (dampak-perubahan.md baris 10) | ❌ lihat cacat berat #1 |

## Audit keamanan skill
Tidak ada script, panggilan jaringan, perintah destruktif, atau pembacaan kredensial. Tidak ada
prompt injection. Larangan perubahan tanpa izin dan larangan menyadap orang lain tertulis. ✅

## Skor
| Kriteria | v1.0 | v1.1.0 | Alasan |
|---|---|---|---|
| Pemicu (description) | 8 | 8 | Tetap tepat |
| Kemudahan awam | 8 | 8 | Pertanyaan kegunaan 4 opsi, bahasa awam |
| Kualitas output | 7 | 8 | Baris "Efek yang berhenti bekerja", jaring pengaman, aturan pemilik |
| Akurasi | 6 | 6 | Banyak koreksi benar (nilai efektif, `auto`, `--fix`, Pasal 4), tapi ada kesalahan baru pada kunci grup WA dan klaim telemetri |
| Penanganan input kurang | 7 | 8 | Pertanyaan kegunaan + default "mungkin semua" |
| Penanganan di luar cakupan | 7 | 9 | Penyadapan ditolak eksplisit, hukum → konsultan |
| Keamanan (tidak merusak) | 5 | 6 | Peta dampak besar-besaran sudah ada, tetapi baris grup WA justru memandu ke pengaturan yang mematikan grup yang ingin dipertahankan / memberi rasa aman palsu |

## SKOR AKHIR: 6 / 10 — **REVISI** (satu perbaikan kecil lagi menuju ≥ 8)
Revisi v1.1.0 menutup hampir semua cacat v1.0 dan membuat skill jauh lebih aman: peta dampak,
nilai efektif, larangan `messaging`/sandbox `all`, penjelasan `--fix`, aturan pemilik, UU PDP
Pasal 4, `.bak`/`--dry-run`, dan `memory forget`. Namun baris pertama tabel dampak, yang menjadi
"sumber kebenaran", memuat kesalahan konfigurasi yang persis menimbulkan kerusakan tanpa
peringatan pada skenario paling umum (bot di grup reseller). Karena ini cacat berat, skor
dibatasi ≤ 6. Perbaikannya sempit dan jelas (lihat #1). Setelah diperbaiki, skill layak dinilai 8.

## Cacat tersisa & saran perbaikan

### Berat
1. **Kunci grup WhatsApp salah di `references/dampak-perubahan.md` baris 10** ("sampai ID grup
   ditambahkan ke `groupAllowFrom`… ID grup itu ditambahkan bersamaan"). Menurut docs 2026.9.5
   (`channels/whatsapp.md` → "Group policy and allowlists"; `channels/groups.md`):
   - `groupAllowFrom` = daftar **pengirim** (nomor E.164) yang boleh memicu bot di grup. **ID grup
     (`…@g.us`) masuk ke `channels.whatsapp.groups`** (map; `"*"` = semua grup).
   - Bila `groupAllowFrom` kosong, pemeriksaan pengirim **jatuh ke `allowFrom`**. Dengan
     `allowFrom: ["*"]` (wajib untuk `dmPolicy: open`), `groupPolicy: allowlist` saja **tidak
     membatasi siapa pun**, padahal temuan grup hilang dari audit. Ini rasa aman palsu.
   - Mengikuti skill (ID grup dimasukkan ke `groupAllowFrom`) → tidak ada pengirim yang cocok →
     **bot diam di grup yang justru ingin dipertahankan**, sementara pengguna diberi tahu aman.

   **Perbaikan:** tulis ulang baris itu: (a) grup yang boleh = `channels.whatsapp.groups`
   (ID `…@g.us`); (b) siapa yang boleh menyuruh = `groupAllowFrom` (nomor); (c) peringatkan
   fallback ke `allowFrom`, dan bila berisi `"*"`, rapikan `allowFrom` dulu. Contoh perintah yang
   terverifikasi jalan (config valid, audit sesuai):
   `openclaw config set channels.whatsapp.groups '{"<id>@g.us":{"requireMention":true}}' --strict-json`,
   `openclaw config set channels.whatsapp.groupAllowFrom '["+62…"]' --strict-json`,
   `openclaw config set channels.whatsapp.groupPolicy allowlist`.

### Sedang
2. **`dmPolicy open → pairing/allowlist` tanpa merapikan `allowFrom: ["*"]`** (baris 11): audit
   tetap menandai `allowFrom includes "*"` (terverifikasi). Tambahkan langkah "ganti `["*"]` dengan
   nomor pemilik/asisten" dan urutannya: ubah `allowFrom` bersamaan dengan `dmPolicy`, karena
   `open` tanpa `"*"` membuat semua DM dibuang. Sebutkan juga batas 3 permintaan pairing menunggu.
3. **Telemetri** (`references/openclaw.md` §5, SKILL.md Batasan "Telemetri"): koreksi bahwa cek
   pembaruan harian **bisa** dimatikan (`openclaw config set update.checkOnStart false` atau env
   `OPENCLAW_NO_AUTO_UPDATE=1`), dengan konsekuensi tidak ada pemberitahuan versi baru. Bagi
   member yang khawatir privasi ini opsi sah, bukan "tidak bisa".
4. **Auth Gateway** (baris 15): `gateway.auth.mode: token` tanpa token nyata tidak memperbaiki
   apa pun. Uji: audit tetap `critical gateway.loopback_no_auth`. Tambahkan `openclaw doctor
   --generate-gateway-token` (flag terverifikasi) sebagai langkah yang benar.

### Ringan
5. Rujukan docs profil `messaging` keliru (baris 13): `tools/permission-modes` → `gateway/config-tools/tool-policy`.
6. `references/openclaw.md` §8 merujuk `CLAUDE.md` §1, yang tidak ada di paket pembeli.
7. Tabel §2 kolom "Nilai bawaan" untuk `channels.whatsapp.groupPolicy` = `allowlist`: sebutkan
   bahwa `allowlist` tanpa `groupAllowFrom` memakai `allowFrom` (lihat #1).

## Uji A/B & pesaing
Tetap: **dengan skill jelas lebih baik** daripada tanpa skill. Skill kita **unggul
keseluruhan** atas `healthcheck` (bawaan OpenClaw, MIT) dan `clawdbot-security-check`; di v1.1.0
aspek "tidak merusak" sudah setara `healthcheck`, kecuali cacat #1. Lihat `00-*.md`.

## Verifikasi angka
Tidak ada script dan tidak ada perhitungan uang. Jumlah temuan audit (mis. `critical 4 → 1`,
`warn 4 → 3` pada contoh 04) diambil dari audit nyata sebelum dan sesudah perubahan.
