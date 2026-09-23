# 02 — Dokter memakai OpenClaw untuk balas WA pasien: aman & patuh UU PDP?

**Skenario:** S2 (normal, data kesehatan). Config nyata di HOME uji: WA `dmPolicy: open`,
`allowFrom: ["*"]`, `groupPolicy: allowlist`, `tools.profile: full`. Exec, sandbox, dan dmScope
tidak diatur.

**Input pengguna (persis):**
> saya dokter, openclaw saya pasang di WA praktik biar balas pasien otomatis. aman nggak buat data pasien? udah sesuai UU PDP belum?

**Yang dijalankan agent (baca saja):** `openclaw security audit --json` (critical 4, warn 4, info 1),
`config get` untuk path di references §2, `openclaw approvals get --json` (exec efektif `full`, ask `off`),
`openclaw sandbox explain` (mode `off`).

---

## Output

## Ringkasan Keamanan OpenClaw Anda

🔴 **Merah (3)**
- **Semua nomor bisa chat ke bot praktik, dan bot membalas sendiri** (`channels.whatsapp.dmPolicy = open`, `allowFrom = ["*"]`)
  Kenapa penting: chat pasien berisi **data kesehatan**, jenis data pribadi yang paling sensitif.
  Bot yang membalas sendiri bisa (1) memberi jawaban yang terdengar seperti saran medis, dan (2)
  dipancing orang asing dengan pesan jebakan untuk membuka isi percakapan lain.
- **AI boleh menjalankan perintah komputer & membaca/menulis file tanpa bertanya** (exec efektif `full`,
  sandbox `off`; audit: `security.exposure.open_groups_with_runtime_or_fs`)
  Kenapa penting: kalau komputer praktik juga menyimpan berkas pasien, pesan jebakan dari WA bisa menyentuhnya.
- **AI boleh mengubah jadwal/plugin dari chat terbuka** (`tools.profile = full`; audit: `…control_plane_tools`)

🟡 **Kuning (2)**
- **Semua pasien berbagi satu ingatan percakapan** (`session.dmScope` bawaan `main`). Info pasien
  A bisa ikut terbawa saat membalas pasien B. Untuk praktik dokter, butir ini sebaiknya diperbaiki.
- **Bot dipakai banyak orang** (audit: `security.trust_model.multi_user_heuristic`).

🟢 **Hijau (2)**
- Grup WA dibatasi (`groupPolicy = allowlist`).
- Statistik pemakaian anonim nonaktif.

## Ringkasan Data & Model
- Riwayat chat pasien tersimpan di `~/.openclaw` di laptop praktik. Pasang kunci layar dan
  enkripsi disk (FileVault di Mac, BitLocker di Windows). Ini langkah manual, bukan pengaturan OpenClaw.
- Isi chat pasien **dikirim ke penyedia model AI** yang Anda pilih. Pastikan Anda nyaman dengan
  kebijakan data penyedia tersebut, atau tanyakan opsi model lokal.

## Saran utama (bukan sekadar pengaturan)
Untuk praktik dokter, saran kami: **jangan biarkan AI membalas pasien sendiri.** Pakai **mode
Copilot**: AI menyiapkan draf balasan untuk pertanyaan umum (jadwal, biaya, lokasi), lalu Anda
atau asisten yang membaca dan menekan kirim. Pertanyaan keluhan/obat selalu dijawab dokter.
Alasannya: data kesehatan sensitif, larangan saran medis oleh AI, dan WhatsApp Web di OpenClaw
bukan jalur resmi (nomor bisa diblokir).

## Perbaikan yang saya tawarkan (satu per satu)
**Butir 1 dari 3: pisahkan ingatan tiap pasien**
- Ubah: `session.dmScope` dari *(belum diatur, bawaan `main`)* → `per-channel-peer`
- Efek: setiap pasien punya riwayat percakapan sendiri. Tidak ada yang rusak.
- Cara membatalkan: `openclaw config unset session.dmScope`
- **Ubah sekarang? (ya/tidak)**

*(Butir 2: `channels.whatsapp.dmPolicy` `open` → `pairing`. **Efek: pasien baru tidak dilayani bot
sampai Anda setujui**, sehingga balasan otomatis ke pasien baru berhenti. Ini sejalan dengan mode
Copilot. Batal: `openclaw config set channels.whatsapp.dmPolicy open`. Butir 3: minta persetujuan
setiap kali AI menjalankan perintah komputer (`tools.exec.mode` → `ask`). **Efek: laporan/jadwal
otomatis yang menjalankan script bisa gagal** bila tidak ada layar persetujuan yang terbuka.
Batal: `openclaw config unset tools.exec.mode`. Masing-masing ditanyakan terpisah.)*

## UU PDP
- UU No. 27/2022 (berlaku penuh Oktober 2024) memperlakukan **data kesehatan sebagai data pribadi
  yang bersifat spesifik**, sehingga perlindungannya lebih ketat.
- Praktis: beri tahu pasien di pesan pertama bahwa balasan dibantu asisten virtual dan dicek tim.
  Minta persetujuan sebelum data dipakai di luar keperluan layanan. Simpan seperlunya. Tahu cara
  menghapus bila pasien meminta.
- Kewajiban kerahasiaan rekam medis dan etika profesi juga berlaku. Konsultasikan ke IDI/penasihat hukum.
- *Ringkasan ini bukan nasihat hukum. Untuk kepatuhan penuh, konsultasikan ke konsultan hukum/DPO.*

---

## Catatan penguji
- **Bagus:** UU PDP disertakan dengan disclaimer, dan data kesehatan diarahkan ke profesional
  sesuai references/uu-pdp.md. Temuan berasal dari audit nyata.
- **Kurang:** skill tidak memuat aturan pemilik "agen CS WA = mode Copilot" maupun "nomor WA
  terpisah". Kalimat "jangan biarkan AI membalas pasien sendiri" berasal dari penguji. Skill juga
  tidak menyebut dampak `dmPolicy → pairing` (balasan ke pasien baru berhenti) dan dampak
  `exec.mode → ask` (automation/cron ditolak bila tidak ada klien persetujuan; docs
  `tools/exec-approvals.md`: "chat channels never receive automation approvals… With no approval
  surface connected, the request is denied immediately"). Tanpa peringatan itu, agent yang
  mengikuti contoh di SKILL.md (baris 136–139, "ubah ke `ask`") bisa merusak laporan otomatis
  tanpa pengguna sadar.
- Frasa "data spesifik" untuk data kesehatan (Pasal 4 UU PDP) sebaiknya dimasukkan ke references/uu-pdp.md, yang sekarang hanya menyebut "kategori data sensitif".
