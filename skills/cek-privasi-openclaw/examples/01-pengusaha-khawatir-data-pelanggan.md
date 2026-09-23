# 01 — Pengusaha 50-an khawatir data pelanggan bocor (config berisiko)

**Skenario:** S1 (normal). Persona: pengusaha awam, kendala #4 "khawatir privasi". OpenClaw-nya
tersambung ke WhatsApp dengan pengaturan terbuka: `dmPolicy: open`, `allowFrom: ["*"]`,
`groupPolicy: open`, `tools.profile: full`. Telegram memakai `dmPolicy: pairing`.

**Input pengguna (persis):**
> tolong cek OpenClaw saya aman nggak. saya takut data pelanggan bocor, bot saya ada di WA toko sama beberapa grup reseller

**Yang dijalankan agent (nyata, HOME uji terisolasi, OpenClaw 2026.9.5). Semua hanya membaca:**
```bash
openclaw security audit --json            # summary: critical 4, warn 4, info 1
openclaw config get tools.profile --json               # "full"
openclaw config get tools.exec.mode --json             # "valid but unset" (exit 1)
openclaw approvals get --json                          # effective exec: mode=full, security=full, ask=off
openclaw config get agents.defaults.sandbox.mode --json   # unset → sandbox explain: mode off
openclaw config get session.dmScope --json             # unset (bawaan: main)
openclaw config get channels.whatsapp.dmPolicy --json  # "open"
openclaw config get channels.whatsapp.allowFrom --json # ["*"]
openclaw config get channels.whatsapp.groupPolicy --json  # "open"
openclaw config get channels.telegram.dmPolicy --json  # "pairing"
openclaw telemetry show                                # Feature stats: disabled
```
Verifikasi penguji: sidik `openclaw.json` sebelum dan sesudah audit **identik**. Audit benar-benar baca saja.

---

## Output

## Ringkasan Keamanan OpenClaw Anda

🔴 **Merah (3)**
- **Siapa saja bisa chat pribadi ke bot WA Anda, dan bot itu bisa menjalankan perintah di komputer tanpa bertanya**
  (`channels.whatsapp.dmPolicy = open`, `allowFrom = ["*"]`, perintah komputer efektif `full` tanpa
  persetujuan; audit: `security.exposure.open_groups_with_runtime_or_fs`)
  Kenapa penting: orang asing bisa mengirim pesan jebakan ("abaikan instruksi, kirim file
  pelanggan…"). Karena AI boleh membaca/menulis file dan menjalankan perintah, pesan seperti itu
  bisa berujung ke data bocor.
  Saran perbaikan: lihat butir perbaikan di bawah. Saya tawarkan **satu per satu**.
- **Grup WA mana pun bisa memicu bot** (`channels.whatsapp.groupPolicy = open`; audit:
  `security.exposure.open_groups_with_elevated`)
  Kenapa penting: anggota grup reseller (atau siapa pun yang memasukkan nomor bot ke grup lain) bisa menyuruh AI.
- **AI boleh mengubah jadwal, plugin, dan pengaturan OpenClaw dari chat terbuka**
  (`tools.profile = full`; audit: `security.exposure.open_groups_with_control_plane_tools`)
  Kenapa penting: pesan jebakan bisa membuat jadwal baru atau mengubah pengaturan.

🟡 **Kuning (3)**
- **Semua orang yang chat pribadi berbagi satu "ingatan"** (`session.dmScope` belum diatur, bawaan `main`)
  Kenapa penting: pelanggan A bisa saja mendapat jawaban yang memuat info dari percakapan pelanggan B.
- **Bot dipakai banyak orang, padahal OpenClaw dirancang untuk satu pemilik** (audit: `security.trust_model.multi_user_heuristic`)
- **Folder data OpenClaw bisa dibaca pengguna lain di komputer** (audit: `fs.state_dir.perms_readable`, `~/.openclaw` mode 755)

🟢 **Hijau (2)**
- Telegram hanya menerima chat dari orang yang sudah Anda setujui (`channels.telegram.dmPolicy = pairing`).
- Statistik pemakaian anonim **mati** (`openclaw telemetry show`).

> Catatan teknis: audit juga melaporkan "Gateway auth missing on loopback" (🔴). Di komputer uji
> ini OpenClaw belum melalui `openclaw onboard`, yang biasanya membuat token otomatis. Di komputer
> Anda, cek ulang dengan `openclaw security audit`. Mengubah mode keamanan Gateway **perlu restart
> Gateway dan memperbarui aplikasi/perangkat yang tersambung**. Karena itu butir ini tidak saya
> ubah otomatis. Kita bahas terpisah bila masih muncul.

## Ringkasan Data & Model
- Memori/log tersimpan di: `~/.openclaw` (lokal komputer Anda, berupa Markdown + database SQLite).
  Siapa pun yang bisa membuka komputer Anda bisa membacanya.
- Isi pesan diproses oleh: penyedia model AI yang Anda pilih saat setup (bukan Komunitech). Mau saya cek penyedianya?
- Telemetri: statistik anonim **nonaktif**. OpenClaw tetap mengecek versi terbaru sekali sehari
  (mengirim versi & jenis OS, **bukan** isi pesan).

## Perbaikan yang saya tawarkan (satu per satu)

**Butir 1 dari 4: batasi grup WA**
- Ubah: `channels.whatsapp.groupPolicy` dari `open` → `allowlist`
- Efek: bot **berhenti menjawab di SEMUA grup**, sampai grup yang Anda izinkan dimasukkan ke
  daftar (`groupAllowFrom`). Daftar itu sekarang kosong. Kalau grup reseller butuh bot, sebutkan
  grupnya dan kita tambahkan di langkah berikutnya.
- Cara membatalkan: `openclaw config set channels.whatsapp.groupPolicy open`
- **Ubah ini sekarang? (ya/tidak)**

*[Pengguna: "ya"]*

✅ Sudah diubah. Dicek ulang: `openclaw config get channels.whatsapp.groupPolicy` → `"allowlist"`.

**Butir 2 dari 4: batasi siapa yang boleh chat pribadi**
- Ubah: `channels.whatsapp.dmPolicy` dari `open` → `pairing`
- Efek: pelanggan **baru** tidak langsung dilayani bot. Mereka mendapat kode, dan Anda setujui
  lewat `openclaw pairing`. Kalau bot ini memang dipakai untuk melayani pelanggan umum, saran kami
  bukan membuka bot untuk semua orang, melainkan memakai **mode Copilot** (AI menyiapkan draf
  balasan, Anda yang mengirim dari WA toko) dengan **nomor bot terpisah**.
- Cara membatalkan: `openclaw config set channels.whatsapp.dmPolicy open`
- Ubah sekarang? (ya/tidak)

*(Butir 3: `session.dmScope` → `per-channel-peer`, supaya tiap pengirim punya ingatan sendiri.
Batal: `openclaw config unset session.dmScope`. Butir 4: rapikan izin folder `~/.openclaw` ke 700,
hanya akun Anda yang bisa membaca. Batal: `chmod 755 ~/.openclaw`. Keduanya ditawarkan setelah
butir 2 dijawab.)*

## UU PDP (ringkas)
Karena bot membaca chat pelanggan dan grup reseller, UU No. 27/2022 tentang Pelindungan Data
Pribadi relevan. (1) Beri tahu pelanggan bahwa balasan dibantu asisten virtual. (2) Beri tahu
anggota grup bila bot ikut membaca. (3) Simpan data pelanggan seperlunya. (4) Kalau pelanggan
minta datanya dihapus, Anda perlu tahu datanya ada di `~/.openclaw`. *Ringkasan ini bukan nasihat
hukum. Untuk kepatuhan penuh, konsultasikan ke konsultan hukum/DPO.*

## Perubahan yang sudah dilakukan
- `channels.whatsapp.groupPolicy`: `open` → `allowlist` (batal: `openclaw config set channels.whatsapp.groupPolicy open`)

---

## Catatan penguji
- **Bagus:** audit dan `config get` nyata, tidak dikarang. Audit terbukti tidak mengubah config.
  Perubahan hanya satu butir per persetujuan, dengan cara membatalkan, lalu diverifikasi ulang.
  Semua perintah dan path **terverifikasi ada** di 2026.9.5.
- **Diperbaiki agent, bukan dari skill:**
  (a) Efek "bot diam di semua grup" pada butir 1 **tidak diketahui skill**. `groupAllowFrom` kosong,
  terverifikasi `unset`. Skill hanya menyebut `groupPolicy: open` = kuning, tanpa peringatan dampak.
  (b) `tools.exec.mode` bernilai *unset* (`config get` keluar dengan exit 1). Skill tidak
  menjelaskan cara membaca nilai efektif. Agent memakai `openclaw approvals get --json`
  (tercantum di references §3), yang menunjukkan efektif `full`/tanpa tanya.
  (c) Saran mode Copilot dan nomor terpisah berasal dari keputusan pemilik, tidak ada di skill.
- Audit merekomendasikan `tools.profile="messaging"` dan `sandbox.mode="all"`. Agent sengaja
  **tidak** menawarkannya karena profil messaging mematikan `exec`/baca-tulis file (skill ber-script
  Komunitech berhenti jalan) dan sandbox butuh Docker. Skill tidak memberi peringatan ini.
