# 00 — Uji banding pesaing (S1)

## Pencarian
- **github.com/VoltAgent/awesome-openclaw-skills** (README + kategori): kata kunci onboard, starter,
  getting started, business, employee, persona, assistant setup.
- **ClawHub API** (clawhub.ai/api/v1/skills/...): membaca SKILL.md pesaing (hanya dibaca, tidak dijalankan).
- **Skill bawaan OpenClaw 2026.9.5** (`node_modules/openclaw/skills`, custodian-skills) dan perintah `openclaw onboard`/`setup`.
- **anthropics/skills**: tidak ada skill onboarding bisnis.
- **manairalabs/bicara-skills** (invoice-extract-id, wa-reply-id) dan **alvinindra/bahasa-skills**
  (gaya bahasa): tidak ada skill onboarding/starter kit.

**Pesaing paling relevan:** **AI Persona OS** (`jeffjhunter/ai-persona-os`), ClawHub
https://clawhub.ai/jeffjhunter/ai-persona-os, 12.167 unduhan, 95 bintang, v2.0.0. **Lisensi:
tidak dicantumkan** (hanya dibaca untuk dinilai, tidak disalin). Isinya: "zero-terminal
agent-driven setup" dengan menu preset (Coding/Executive/Marketing Assistant, 24 "soul"),
wawancara 4–8 pertanyaan, lalu membuat file workspace (SOUL.md, USER.md, MEMORY.md, dll.).
Pembanding kedua: **`openclaw onboard`** (wizard bawaan). Ini mengurus model/kanal/Gateway,
bukan kebutuhan bisnis, jadi tidak sebanding.

## S1 dengan instruksi pesaing (agent berperan memuat AI Persona OS)
> 👋 Welcome to AI Persona OS! I'm going to build your complete AI workspace — identity, memory,
> security, daily operations… What kind of AI Persona are you building?
> 1. 💻 Coding Assistant 2. 📋 Executive Assistant 3. 📣 Marketing Assistant 4. 🔥 SOUL.md Maker 5. 🔧 Custom
>
> *[pengguna menjawab dengan kalimat panjang soal rumah makan → aturan pesaing: jawaban tidak jelas → default `coding-assistant`, atau dipilih "2" oleh agent]*
>
> Great choice! 1. What's YOUR name? 2. What should I call you? 3. What's your role? 4. What's your main goal right now?
>
> *[setelah dijawab]* 🎉 Your AI Persona is ready! ✅ SOUL.md ✅ USER.md ✅ MEMORY.md ✅ AGENTS.md ✅ SECURITY.md ✅ HEARTBEAT.md … Try: "status", "show persona", "health check".

## Output skill kita
Lihat `01-owner-resto-50-karyawan-laporan.md`.

## Penilaian
| Kriteria | AI Persona OS | karyawan-ai-mulai |
|---|---|---|
| Kualitas (hasil nyata untuk bisnis) | 4: membangun "kepribadian" & file workspace, tanpa tugas bisnis yang selesai | 8: rekap omzet nyata + 3 skill kerja + rencana 7 hari |
| Kesesuaian konteks Indonesia | 2: bahasa Inggris, persona developer/eksekutif, contoh Discord | 9: bahasa awam, Rupiah, F&B, Telegram, UU PDP |
| Akurasi | 6: pesaing mengandalkan `exec` + `sed`; aturan jawaban tidak jelas → "coding-assistant" keliru untuk owner resto | 6: perintah OpenClaw benar, tapi script pemetaan punya salah cocok (lihat 03) |
| Siap pakai untuk awam 50+ | 3: 24 soul, istilah SOUL/HEARTBEAT membingungkan | 8: satu pesan, pilihan bernomor, izin jelas |

**Kesimpulan:** skill kita **unggul** untuk persona member VIP.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Teks menu baku** yang harus ditampilkan persis, dengan pilihan bernomor. Ini membuat
   pengalaman konsisten antar sesi. Skill kita bisa punya satu template pesan wawancara baku.
2. **Aturan default untuk jawaban samar** yang eksplisit per pertanyaan (skill kita sudah punya
   sebagian di tabel Input).
3. **Cek prasyarat tools.profile**: pesaing memperingatkan bahwa profil `messaging` tidak punya
   `exec`, sehingga setup gagal diam-diam. Skill kita juga butuh `exec`, untuk install dan untuk
   script rekap. Tambahkan cek ini, karena `cek-privasi-openclaw` bisa menyarankan profil yang
   lebih ketat.
4. **Langkah verifikasi setelah setup** (pesaing: `ls` semua file). Padanan kita: `openclaw skills
   check` atau `openclaw skills info <nama>` setelah install. Keduanya terverifikasi ada di 2026.9.5.
