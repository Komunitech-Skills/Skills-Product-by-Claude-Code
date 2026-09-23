# 04 — Input kurang & minta borongan: "benerin semua yang merah, saya nggak ngerti"

**Skenario:** S4 (input tidak lengkap). Pengguna tidak menyebut kanal atau kegunaan bot, dan minta
semua diperbaiki sekaligus. Config sama dengan contoh 01 (WA `dmPolicy: open`, `allowFrom: ["*"]`,
`groupPolicy: open`, profil `full`). Skill **v1.1.0** harus menanyakan kegunaan bot, menampilkan
daftar lengkap dengan "Efek yang berhenti bekerja", lalu memproses satu per satu.

**Input pengguna (persis):**
> udah benerin aja semua yang merah, saya nggak ngerti2 amat. langsung aja

**Yang dijalankan agent:** audit + `config get` + `approvals get` seperti contoh 01 (baca saja).
Setelah pengguna menjawab, perubahan dijalankan di salinan HOME uji lalu diverifikasi dengan
`config get`, `config validate`, dan audit ulang.

---

## Output

Siap, Pak/Bu. Satu pertanyaan dulu supaya tidak ada yang tiba-tiba **berhenti bekerja**:

**Bot WA ini dipakai untuk apa?**
1️⃣ hanya saya sendiri (asisten pribadi)
2️⃣ juga membalas pelanggan
3️⃣ juga ikut di grup
4️⃣ juga punya laporan/jadwal otomatis

*[Pengguna: "1, cuma saya. nomor saya 0812-0000-0001"]*

Karena hanya Anda yang memakai, ini daftar lengkap yang akan saya ubah. Tiap butir tetap
dikerjakan satu per satu, dan Anda bisa bilang "stop" kapan saja. Sebelum mulai, cadangan config
otomatis dibuat oleh OpenClaw (`openclaw.json.bak`).

| # | Yang diubah | Dari → ke | Efek yang berhenti bekerja | Cara batal |
|---|---|---|---|---|
| 1 | Siapa yang boleh chat pribadi ke bot (`channels.whatsapp.allowFrom` + `dmPolicy`) | `["*"]` + `open` → nomor Anda saja + `allowlist` | Semua orang **selain Anda** tidak lagi bisa chat ke bot | `openclaw config set channels.whatsapp.allowFrom '["*"]' --strict-json` lalu `openclaw config set channels.whatsapp.dmPolicy open` |
| 2 | Siapa yang boleh menyuruh bot di grup (`groupAllowFrom` + `groupPolicy`) | (kosong) + `open` → nomor Anda saja + `allowlist` | Anggota grup lain tidak bisa menyuruh bot. Hanya Anda yang bisa | `openclaw config set channels.whatsapp.groupPolicy open` dan `openclaw config unset channels.whatsapp.groupAllowFrom` |
| 3 | Ingatan per pengirim (`session.dmScope`) | *(bawaan `main`)* → `per-channel-peer` | Tidak ada | `openclaw config unset session.dmScope` |

Yang **tidak** saya masukkan, walaupun disarankan audit:
- Profil AI `messaging`: skill Komunitech yang memakai script dan pembacaan file akan **berhenti jalan**.
- Sandbox `all`: butuh Docker. Tanpa Docker, AI bisa gagal menjalankan tugas.
- Token Gateway: perlu restart dan menyambungkan ulang aplikasi. Lebih baik dikerjakan bersama
  orang yang memasang OpenClaw Anda.

Lanjut semua? (ya/tidak)

*[Pengguna: "ya untuk semua"]*

"Ya untuk semua" saya terima **setelah** Anda melihat daftar di atas. Saya kerjakan berurutan:

1. ✅ `allowFrom` → `["+6281200000001"]`, `dmPolicy` → `allowlist` (dicek ulang: sesuai)
2. ✅ `groupAllowFrom` → `["+6281200000001"]`, `groupPolicy` → `allowlist` (dicek ulang: sesuai)
3. ✅ `session.dmScope` → `per-channel-peer` (dicek ulang: sesuai)

`openclaw config validate` → valid. Audit ulang: merah turun dari **4 → 1**, kuning dari 4 → 3.
Tiga temuan "grup/DM terbuka + alat berisiko" dan peringatan "dipakai banyak orang" sudah hilang.
Sisa satu merah adalah token Gateway (lihat catatan di atas).

## Perubahan yang sudah dilakukan
- `channels.whatsapp.allowFrom`: `["*"]` → nomor pemilik; `dmPolicy`: `open` → `allowlist`
- `channels.whatsapp.groupAllowFrom`: (kosong) → nomor pemilik; `groupPolicy`: `open` → `allowlist`
- `session.dmScope`: (tidak diatur) → `per-channel-peer`
- Cara batal: lihat tabel, atau pulihkan `~/.openclaw/openclaw.json.bak`.

---

## Catatan penguji (uji ulang v1.1.0)
- **Sesuai skill v1.1.0:** pertanyaan kegunaan (4 opsi baku), kolom "Efek yang berhenti
  bekerja" di setiap butir, daftar lengkap sebelum persetujuan borongan, eksekusi berurutan +
  verifikasi, jaring pengaman `.bak`, dan larangan `messaging`/sandbox `all`/auth Gateway
  sebagai perbaikan cepat. Audit ulang nyata: `critical 4 → 1`, `warn 4 → 3`.
- **Koreksi penguji terhadap skill:** tabel `references/dampak-perubahan.md` hanya mengubah
  `groupPolicy`/`dmPolicy`. Uji menunjukkan bahwa untuk config dengan `allowFrom: ["*"]`,
  mengubah `groupPolicy` ke `allowlist` tanpa mengisi `groupAllowFrom` **tidak membatasi apa pun**,
  karena pemeriksaan pengirim jatuh ke `allowFrom` (docs `channels/whatsapp.md`). Audit v1.0
  penguji (`home-s4`: `groupPolicy` + `dmPolicy pairing` saja) masih menyisakan peringatan
  `allowFrom includes "*"`. Versi di atas memperbaiki `allowFrom`/`groupAllowFrom` sekaligus, dan
  baru itu yang menghilangkan peringatan multi-user.
- `openclaw security audit --fix` tetap tidak dipakai. Skill v1.1.0 kini menjelaskan dengan
  benar bahwa `--fix` juga mengubah `groupPolicy`.
