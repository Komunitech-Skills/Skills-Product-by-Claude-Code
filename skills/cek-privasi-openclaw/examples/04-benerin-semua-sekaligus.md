# 04 — Input kurang & minta borongan: "benerin semua yang merah, saya nggak ngerti"

**Skenario:** S4 (input tidak lengkap). Pengguna tidak menyebut kanal atau kegunaan bot, dan minta
semua diperbaiki sekaligus. Config sama dengan contoh 01 (WA terbuka, grup terbuka, profil full).
Skill harus menampilkan daftar lengkap dulu, meminta satu info penting, lalu memproses satu per
satu (SKILL.md baris 157–159).

**Input pengguna (persis):**
> udah benerin aja semua yang merah, saya nggak ngerti2 amat. langsung aja

**Yang dijalankan agent:** audit + `config get` seperti contoh 01 (baca saja). Setelah pengguna
menjawab, perubahan dijalankan di salinan HOME uji (`/tmp/uji-vip/home-s4`) lalu audit diulang.

---

## Output

Siap, Pak/Bu. Supaya tidak ada yang tiba-tiba **berhenti bekerja**, ini dulu daftar lengkap yang
akan saya ubah. Tiap butir tetap saya kerjakan satu per satu, dan Anda bisa bilang "stop" kapan saja.

| # | Yang diubah | Dari → ke | Efek yang perlu Anda tahu | Cara batal |
|---|---|---|---|---|
| 1 | Grup WA yang boleh memicu bot (`channels.whatsapp.groupPolicy`) | `open` → `allowlist` | Bot **diam di semua grup** sampai grup tertentu diizinkan | `openclaw config set channels.whatsapp.groupPolicy open` |
| 2 | Siapa yang boleh chat pribadi (`channels.whatsapp.dmPolicy`) | `open` → `pairing` | Pelanggan **baru** tidak langsung dibalas bot, harus Anda setujui dulu | `openclaw config set channels.whatsapp.dmPolicy open` |
| 3 | Ingatan per pengirim (`session.dmScope`) | *(bawaan `main`)* → `per-channel-peer` | Tidak ada yang rusak. Tiap orang punya riwayat sendiri | `openclaw config unset session.dmScope` |

Yang **tidak** saya masukkan ke daftar, meskipun disarankan audit:
- Ganti profil AI ke `messaging`: skill Komunitech yang memakai script (rekap penjualan, dll.)
  dan pembacaan file akan **berhenti jalan**.
- Sandbox `all`: butuh Docker terpasang. Tanpa Docker, AI gagal menjalankan tugas.
- Kunci token Gateway: perlu restart dan menyambungkan ulang aplikasi. Lebih baik dikerjakan
  bersama orang yang memasang OpenClaw Anda.

**Satu pertanyaan saja sebelum mulai:** bot WA ini dipakai untuk apa?
1️⃣ hanya saya sendiri (asisten pribadi)
2️⃣ membalas pelanggan
3️⃣ ikut di grup (mis. grup reseller)

Kalau jawabannya 2 atau 3, butir 1–2 akan menghentikan layanan itu, dan kita cari jalan yang lebih
aman (nomor bot terpisah + AI menyiapkan draf, Anda yang kirim).

*[Pengguna: "1, cuma saya. ya untuk semua"]*

Baik, "ya untuk semua" saya terima **setelah** Anda melihat daftar di atas. Saya kerjakan berurutan:

1. ✅ `channels.whatsapp.groupPolicy`: `open` → `allowlist` (dicek ulang: `"allowlist"`)
2. ✅ `channels.whatsapp.dmPolicy`: `open` → `pairing` (dicek ulang: `"pairing"`)
3. ✅ `session.dmScope`: *(tidak diatur)* → `per-channel-peer` (dicek ulang: `"per-channel-peer"`)

Audit ulang: merah turun dari **4 → 1**. Sisa satu merah adalah token Gateway (lihat catatan di
atas). Tiga temuan "grup/DM terbuka + alat berisiko" sudah hilang.

## Perubahan yang sudah dilakukan
- `channels.whatsapp.groupPolicy`: open → allowlist (batal: `openclaw config set channels.whatsapp.groupPolicy open`)
- `channels.whatsapp.dmPolicy`: open → pairing (batal: `openclaw config set channels.whatsapp.dmPolicy open`)
- `session.dmScope`: (tidak diatur) → per-channel-peer (batal: `openclaw config unset session.dmScope`)
- Cadangan otomatis config lama dibuat OpenClaw di `~/.openclaw/openclaw.json.bak`.

---

## Catatan penguji
- **Bagus (sesuai skill):** daftar lengkap sebelum persetujuan borongan, eksekusi berurutan dengan
  verifikasi, dan cara batal per butir. Audit ulang nyata: `critical 4 → 1`.
- **Ditambahkan agent, tidak ada di skill:** kolom "Efek yang perlu Anda tahu" dan pertanyaan
  kegunaan bot. Tanpa itu, "benerin semua" memutus layanan pelanggan/grup tanpa peringatan.
  Daftar "yang tidak saya masukkan" (profil messaging mematikan exec; sandbox butuh Docker) juga
  berasal dari docs OpenClaw, bukan dari skill. Skill juga tidak menyebut cadangan otomatis
  `openclaw.json.bak` (terverifikasi dibuat) dan `config set --dry-run` (terverifikasi ada), yang
  berguna sebagai jaring pengaman.
- `openclaw security audit --fix` **tidak** dipakai. Uji di salinan HOME menunjukkan `--fix` juga
  mengubah `channels.whatsapp.groupPolicy open → allowlist`, bukan hanya izin file seperti kesan
  SKILL.md baris 94–96 ("rapikan izin file dsb.").
