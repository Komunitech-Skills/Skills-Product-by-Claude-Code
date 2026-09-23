# HASIL UJI — cek-privasi-openclaw

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** OpenClaw 2026.9.5 (ec9c1a1), beberapa HOME uji terisolasi (baru, "berisiko",
  "dokter", salinan untuk uji perubahan), tanpa login kanal. Skill dipasang dengan
  `openclaw skills install ./cek-privasi-openclaw --global` → Ready, visible, available as command.

## Verifikasi perintah & kunci config
| Perintah / path | Hasil |
|---|---|
| `openclaw security audit --json` / `--deep` / `--fix` (help) | ✅ ada. **Baca saja terbukti**: sidik `openclaw.json` sama sebelum dan sesudah; hanya mtime folder `state/` (SQLite) yang berubah |
| Bentuk JSON: `findings[]` berisi `severity`, `title`, `detail`, `remediation` | ⚠️ ada, tapi `remediation` **opsional** (tidak ada pada `summary.attack_surface`); ada juga `checkId` |
| `openclaw config get <path> --json` | ✅. Untuk path yang belum diatur: **exit 1**, "Config path is valid but unset" (tidak dijelaskan skill) |
| Path: `tools.profile`, `tools.exec.mode` (deny/allowlist/ask/auto/full), `tools.exec.security`, `agents.defaults.sandbox.mode`, `session.dmScope`, `channels.<kanal>.dmPolicy/allowFrom/groupPolicy`, `messages.groupChat.historyLimit`, `commands.ownerAllowFrom`, `security.installPolicy`, `approvals.exec` | ✅ semua ada di `openclaw config schema` dan diterima `config get` |
| Default skema: dmPolicy `pairing`, groupPolicy `allowlist` | ✅ |
| `openclaw approvals get --json` | ✅ dan berguna: menampilkan **nilai efektif** exec (bawaan: mode `full`, ask `off`) |
| `openclaw approvals pending --json` | ⚠️ ada, tapi butuh Gateway berkredensial (gagal tanpa Gateway; skill tidak menyebut) |
| `openclaw sandbox explain` | ✅ baca saja |
| `openclaw telemetry show/on/off` | ✅. Statistik nonaktif bawaan ("consent has not been requested"); cek versi harian tetap ada |
| `openclaw config set` / `config unset` (+ `--dry-run`) | ✅ jalan, perubahan terverifikasi dengan `config get`; OpenClaw membuat `openclaw.json.bak` otomatis |

## Audit keamanan skill
Tidak ada script, panggilan jaringan, perintah destruktif, pembacaan kredensial, atau prompt
injection. Skill secara eksplisit melarang perubahan tanpa izin. ✅

## Skor
| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 8 | Kata kunci ID/EN pas, batas dengan karyawan-ai-mulai jelas |
| Kemudahan awam | 8 | Lampu lalu lintas, bahasa sehari-hari, langsung jalan |
| Kualitas output | 7 | Format rapi, UU PDP, cara batal; menang A/B |
| Akurasi | 6 | Perintah/path benar. Tapi: `auto` ditulis "jalan tanpa tanya" (sebenarnya ditinjau AI reviewer, jatuh ke manusia); bawaan exec = `full` tidak disebut; `--fix` digambarkan hanya "rapikan izin file" padahal mengubah `groupPolicy` |
| Penanganan input kurang | 7 | Default aman, bulk approval dengan daftar dulu; belum bertanya "bot dipakai untuk apa" |
| Penanganan di luar cakupan | 7 | Hukum → konsultan. Permintaan memantau orang lain tidak diatur |
| Keamanan (tidak merusak) | 5 | Izin per butir ada, tapi tanpa peringatan dampak perubahan yang bisa mematikan fungsi OpenClaw |

## SKOR AKHIR: 6 / 10 — **REVISI**
Alur baca-dulu, izin per butir, dan bahasa awam sudah kuat, dan menang di A/B maupun uji banding
secara keseluruhan. Skor dibatasi karena ada cacat berat: rekomendasi perubahan tidak disertai
pengetahuan dampaknya. Pembeli awam yang menjawab "ya" bisa kehilangan layanan pelanggan, bot
grup, atau laporan otomatis tanpa sadar. Ini persis kriteria "tidak mematikan sesuatu tanpa
peringatan" dari pemilik.

## Daftar cacat & saran perbaikan

### Berat
1. **Tidak ada peta dampak perubahan** (SKILL.md Langkah 4 baris 84–96, contoh baris 136–139,
   references §6). Terbukti di mesin uji / docs 2026.9.5:
   - `groupPolicy open → allowlist` dengan `groupAllowFrom` kosong → bot **diam di semua grup**.
   - `dmPolicy open → pairing/allowlist` → pelanggan/pasien **baru tidak dilayani**.
   - `tools.exec.mode → ask` (contoh utama skill) → automation/cron yang menjalankan script
     **ditolak** bila tidak ada klien persetujuan (docs `tools/exec-approvals.md`: "chat channels
     never receive automation approvals… denied immediately"). Ini merusak laporan otomatis yang
     disarankan `karyawan-ai-mulai`/`laporan-otomatis-terjadwal`.
   - Remediasi audit yang akan dibaca agent: `tools.profile="messaging"` (menghapus exec/read/write,
     sehingga semua skill ber-script Komunitech berhenti) dan `sandbox.mode="all"` (butuh Docker).
   - Auth Gateway: perubahan mode perlu restart + token di klien.
   - `audit --fix` mengubah `channels.whatsapp.groupPolicy` (terverifikasi), bukan hanya izin file.

   **Perbaikan:** tambah tabel "Perubahan → apa yang akan berhenti → kapan aman" di references,
   wajibkan kolom "Efek yang berhenti bekerja" di setiap tawaran, larang menawarkan
   `messaging`/sandbox `all`/perubahan auth Gateway tanpa peringatan khusus, dan jelaskan `--fix` apa adanya.

### Sedang
2. **Nilai efektif tidak dibaca dengan benar**: tambahkan aturan "`config get` exit 1 'valid but
   unset' = pakai bawaan", lalu pakai `openclaw approvals get --json` (effectivePolicy) dan
   `openclaw sandbox explain`. Tulis di tabel references §2: bawaan `tools.exec.mode` = **`full`,
   tanpa persetujuan**, dan `auto` = ditinjau AI reviewer (bukan "tanpa tanya"; jangan otomatis merah).
3. **Belum selaras dengan keputusan pemilik jalur 3**: tidak ada rekomendasi WA **nomor terpisah**,
   agen CS WA = **mode Copilot**, dan penandaan `dmPolicy: open` di WA sebagai bertentangan dengan
   Copilot. Tambahkan juga pertanyaan profil pemakaian di awal (pribadi / pelanggan / grup), ide dari `healthcheck`.
4. **Data kesehatan**: references/uu-pdp.md sebaiknya menyebut data kesehatan sebagai "data pribadi
   yang bersifat spesifik" (UU PDP Pasal 4) dan menambahkan langkah manual (enkripsi disk, kunci layar, backup).

### Ringan
5. Telemetri (SKILL.md baris 69–70): bedakan statistik anonim (mati bawaan) dari cek versi harian (tetap jalan, kirim versi/OS).
6. `approvals pending` butuh Gateway. Sebutkan, atau hapus dari langkah dasar.
7. Sebutkan jaring pengaman bawaan: `openclaw config set … --dry-run`, `openclaw.json.bak`, `openclaw backup create`.
8. Hak hapus data (UU PDP): sebutkan `openclaw memory forget` / lokasi sesi sebagai cara praktis.
9. "Kapan TIDAK digunakan": tambahkan "memantau/menyadap perangkat atau chat orang lain → tolak".
10. `findings[].remediation` bersifat opsional. Perbaiki kalimat di references §1.

## Verifikasi angka
Tidak ada script dan tidak ada perhitungan angka. Ringkasan jumlah temuan (`critical 4 → 1`
setelah 3 perubahan) diambil dari keluaran audit nyata.
