# 00 — Uji banding pesaing (S1)

## Pencarian
- Skill bawaan OpenClaw 2026.9.5 (`node_modules/openclaw/skills`, `custodian-skills`): kata kunci security, audit, harden.
- **github.com/VoltAgent/awesome-openclaw-skills**: bagian "Security & Config Auditing" dan kategori "Security & Passwords".
- **ClawHub API** (SKILL.md dibaca saja, tidak dijalankan).
- anthropics/skills, manairalabs/bicara-skills, alvinindra/bahasa-skills: tidak ada skill audit privasi OpenClaw.

**Pesaing relevan:**
1. **`healthcheck`**: skill **bawaan OpenClaw** (sudah ada di OpenClaw semua member), lisensi
   **MIT** (OpenClaw Foundation). Isinya audit & hardening host: read-only dulu, profil risiko
   (Convenience/Balanced/Strict), rencana bertahap dan bisa dibatalkan, "without breaking access".
2. **`clawdbot-security-check`** (thesethrose, ClawHub, ±7,1 rb unduhan). **Lisensi tidak
   dicantumkan**, berstatus **"Suspicious" (VirusTotal/OpenClaw)** di clawskills.sh. Isinya
   kerangka 13 domain dalam bahasa Inggris. Perintahnya memakai CLI lama `clawdbot security
   audit` dan kunci config lama (`gateway.auth_token`), yang **tidak ada** di OpenClaw 2026.9.5
   (CLI hanya punya alias `clawbot`). Tidak disimulasikan penuh: tidak layak dipakai member.

## S1 dengan instruksi pesaing utama (`healthcheck`)
> Before I start: I'd like to run read-only checks (`openclaw security audit --deep`, `openclaw gateway status --deep`, `openclaw doctor --lint`, and OS checks like firewall and disk encryption). OK?
>
> *[ya]* **Current posture:** personal workstation, gateway loopback, no gateway auth, WhatsApp open DM + open groups, exec full, sandbox off.
> **Findings:** CRITICAL gateway.loopback_no_auth; CRITICAL open_groups_with_runtime_or_fs / elevated / control_plane_tools; WARN state dir readable; disk encryption: unknown; backups: none.
> Which posture do you want? 1. Convenience 2. Balanced 3. Strict
> **Recommended plan (staged, reversible):** 1) require gateway auth 2) tighten dmPolicy/groupPolicy 3) enable disk encryption 4) verify backups 5) schedule `openclaw security audit --deep`. I'll confirm each exact action before applying.

## Penilaian
| Kriteria | healthcheck (bawaan, MIT) | cek-privasi-openclaw |
|---|---|---|
| Kualitas | 7: rencana bertahap, mencakup OS (firewall, enkripsi disk, backup) | 7: fokus kanal/siapa-boleh-menyuruh, lampu lalu lintas, cara batal per butir |
| Kesesuaian konteks Indonesia | 2: Inggris, istilah teknis, tanpa UU PDP | 9: bahasa awam, UU PDP, contoh WA toko |
| Akurasi | 7: perintah valid (`doctor --lint` terverifikasi ada), tapi `--deep` butuh Gateway | 7: semua perintah/path valid; kurang soal nilai efektif exec & dampak perubahan |
| Siap pakai untuk awam | 3 | 8 |
| "Tidak merusak" | 8: prinsip eksplisit: konfirmasi jalur akses, rollback notes, profil risiko | 5: izin per butir ada, tapi tanpa pengetahuan dampak (grup diam, exec→ask memblokir cron, messaging mematikan exec) |

**Kesimpulan:** secara keseluruhan skill kita **unggul untuk persona member** (bahasa, UU PDP,
fokus kanal chat). **Pada aspek keselamatan perubahan, pesaing lebih baik.** Ini perlu diperbaiki.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Tanyakan profil risiko dulu** (nyaman/seimbang/ketat, atau "bot untuk saya sendiri / pelanggan
   / grup"). Rekomendasi kemudian disesuaikan agar tidak mematikan pemakaian yang sah.
2. **Catatan rollback eksplisit** dan prinsip "jangan ubah akses sebelum jalur akses dipastikan".
   Untuk kita: jangan mengubah token Gateway, dmPolicy, atau profil tool tanpa menjelaskan apa
   yang akan berhenti bekerja.
3. **Langkah manual di luar OpenClaw**: enkripsi disk, backup (`openclaw backup create`
   terverifikasi ada), kunci layar. Penting untuk data pasien/pelanggan.
4. **`openclaw doctor --lint`** sebagai pemeriksaan baca-saja tambahan (flag terverifikasi ada di 2026.9.5).
5. **Laporan "Gaps"**: sebutkan apa yang tidak bisa dicek (mis. `--deep` tanpa Gateway).
