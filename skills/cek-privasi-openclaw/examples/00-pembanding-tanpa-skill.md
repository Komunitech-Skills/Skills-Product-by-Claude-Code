# 00 — Uji A/B: S1 tanpa skill vs dengan skill

**Input (sama dengan S1):**
> tolong cek OpenClaw saya aman nggak. saya takut data pelanggan bocor, bot saya ada di WA toko sama beberapa grup reseller

## A. Tanpa skill (agent biasa, tanpa membaca skill apa pun)
Agent menjalankan `openclaw security audit` lalu menjawab:

> Saya sudah menjalankan audit keamanan. Hasilnya: **4 critical, 4 warn, 1 info**.
>
> **Critical:**
> - gateway.loopback_no_auth — Gateway auth missing on loopback
> - security.exposure.open_groups_with_elevated — Open group/DM policy with elevated tools enabled
> - security.exposure.open_groups_with_runtime_or_fs — Open group/DM policy with runtime/filesystem tools exposed
> - security.exposure.open_groups_with_control_plane_tools — …
>
> **Rekomendasi:** set `tools.profile="messaging"`, `agents.defaults.sandbox.mode="all"`,
> `tools.fs.workspaceOnly=true`, ubah dmPolicy/groupPolicy ke allowlist, dan set gateway.auth token.
> Saya bisa langsung menjalankan `openclaw security audit --fix` untuk memperbaiki otomatis. Mau saya jalankan?

## B. Dengan skill `cek-privasi-openclaw`
Lihat `01-pengusaha-khawatir-data-pelanggan.md`: laporan 🔴🟡🟢 dalam bahasa awam ("orang asing
bisa mengirim pesan jebakan…"), ringkasan data & model (data di `~/.openclaw`, isi pesan ke
penyedia model), UU PDP singkat + disclaimer, perbaikan **satu per satu** dengan efek + cara
batal + verifikasi, dan satu perubahan dijalankan setelah "ya".

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Bahasa untuk awam 50+ | Istilah mentah Inggris (loopback, control plane) | Bahasa sehari-hari + path dalam kurung |
| Keamanan tindakan | Menawarkan `--fix` borongan dan profil `messaging`/sandbox `all`. Bisa mematikan skill ber-script & butuh Docker | Satu butir per izin, ada cara batal, dicek ulang |
| Konteks data & model | Tidak ada | Lokasi data, penyedia model, telemetri |
| UU PDP | Tidak ada | Ada, dengan disclaimer |
| Akurasi temuan | Sama (dari audit nyata) | Sama + nilai efektif exec |

**Kesimpulan:** dengan skill **jelas lebih baik**, terutama pada keamanan tindakan dan bahasa.
Catatan: sebagian peringatan dampak (grup jadi diam, profil messaging mematikan exec) berasal
dari penguji, bukan dari skill. Tanpa itu, skill hanya menang pada format dan izin, belum pada
"tidak merusak" (lihat HASIL-UJI).

## Pembaruan uji ulang v1.1.0
Di v1.1.0, peringatan dampak (profil `messaging` mematikan skill ber-script, sandbox `all` butuh
Docker, `exec.mode → ask` menolak automation, `--fix` mengubah `groupPolicy`) sudah **tertulis
di skill** (`references/dampak-perubahan.md`). Keunggulan "tidak merusak" kini berasal dari
skill, bukan dari penguji. Kesimpulan A/B tetap: **dengan skill jelas lebih baik**. Sisa cacat
kunci grup WA (`groupAllowFrom` vs `groups`) dijelaskan di HASIL-UJI.

## Pembaruan uji ulang v1.1.1
Diuji ulang dengan S1 baru (grup reseller tetap jalan, hanya pemilik + 2 admin yang boleh
menyuruh bot). Agent **tanpa skill** di atas menawarkan `security audit --fix`. Diverifikasi
nyata: `--fix` hanya mengubah `groupPolicy` `open` → `allowlist` dan membiarkan `allowFrom: ["*"]`,
`groups`, dan `groupAllowFrom` apa adanya. Akibatnya **grup tetap bisa disuruh siapa saja**
(pengirim jatuh ke `allowFrom: ["*"]`), DM tetap terbuka, dan audit masih critical 4. Pengguna
tidak mendapat hasil yang dimintanya. Dengan skill v1.1.1 (contoh 01), pembatasan admin tercapai
dengan kunci yang benar, dan setiap butir menyebut apa yang berhenti bekerja. Kesimpulan: **dengan
skill jelas lebih baik**, dan keunggulan "tidak merusak / tidak memberi rasa aman palsu" kini
sepenuhnya berasal dari skill.
