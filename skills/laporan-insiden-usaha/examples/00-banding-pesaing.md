# Uji Banding Pesaing

Pesaing dibaca untuk dinilai saja (tidak disalin isinya). Skenario uji yang dipakai untuk perbandingan: skenario normal #1 (40 paket salah kirim saat flash sale 10.10 — sama dengan Uji 03).

## Pesaing yang dicek

### 1. `incident-postmortem` (github.com/mohitagw15856/pm-claude-skills)
Dikonfirmasi lewat pembacaan langsung `skills/incident-postmortem/SKILL.md` (raw file, 2026-09-26):
- **Tujuan:** postmortem insiden blameless dengan timeline forensik, root cause + contributing factors, action items dengan owner/due date, diprioritaskan berdasarkan "error budget".
- **Format:** ringkasan eksekutif, dampak kuantitatif, timeline (termasuk diagram Gantt teknis), root cause, safeguard yang gagal, resolusi, tabel action item, lessons learned, log komunikasi eksternal.
- **Bahasa/konteks:** Inggris, agnostik industri, berbasis praktik SRE/incident-response global (SLO, error budget) — **tidak** membahas UMKM, ritel fisik, Rupiah, WhatsApp, atau data pribadi Indonesia.
- **Tidak ada** draf permintaan maaf ke pelanggan maupun ringkasan siap tempel ke WA.

### 2. `customer-incident-update` (repo sama)
Dikonfirmasi lewat pembacaan langsung `skills/customer-incident-update/SKILL.md`:
- **Tujuan:** update status insiden ke pelanggan (status page/email), jujur tanpa janji berlebihan, satu permintaan maaf saja per update.
- **Format:** pos status-page dan email dengan tahapan investigasi → identifikasi → monitoring → resolusi.
- Eksplisit **tidak membahas** draf permintaan maaf formal terstruktur, Bahasa Indonesia, WhatsApp, atau UU PDP — berfokus komunikasi gangguan universal (mis. untuk SaaS/produk digital).

### 3. Pencarian skill publik lain sejenis
Dicari (tanpa akses langsung terverifikasi dalam sesi uji ini) dengan kata kunci: "incident report skill", "apology letter skill", "customer complaint response skill", "postmortem template Indonesia", "laporan insiden UMKM" di ClawHub/skills.sh/GitHub. Tidak ditemukan skill publik siap pakai berbahasa Indonesia yang secara khusus menyasar insiden operasional UMKM (retur massal, kasir/QRIS error, broadcast WA salah) dengan draf minta maaf + ringkasan WA + rujukan UU PDP. Mayoritas hasil pencarian mengarah balik ke ekosistem `pm-claude-skills` (incident/postmortem bergaya software engineering) atau template generik "how to write an apology letter" non-skill (artikel blog), bukan Agent Skill terstruktur.

## Perbandingan berdampingan (skenario: 40 paket salah kirim saat flash sale)

| Aspek | `incident-postmortem` + `customer-incident-update` (pesaing) | `laporan-insiden-usaha` (kita) |
|---|---|---|
| Bahasa | Inggris, istilah teknis (SLO, error budget, contributing factors) | Bahasa Indonesia sehari-hari, tanpa jargon teknis |
| Konteks | Software/SaaS (P1/P2, deployment, status page) | Operasional UMKM ritel/e-commerce (packing, kurir, kasir, promo) |
| Draf minta maaf ke pelanggan | Tidak ada di `incident-postmortem`; `customer-incident-update` hanya status-page/email gaya SaaS, bukan draf minta maaf personal | Ada, 2 versi (lengkap + pendek WA), eksplisit tanpa janji berlebihan |
| Ringkasan WA tim/pemilik | Tidak ada (tidak mengenal WhatsApp sebagai kanal) | Ada, format tebal-pendek siap tempel |
| Anti-mengarang angka | Tidak eksplisit dibahas | Eksplisit: `[isi: ...]` wajib untuk data yang tidak diberikan |
| Blameless/5 Kenapa | Ada (root cause + contributing factors ala SRE) — konsepnya dipakai kita, tapi versi kita dilengkapi `references/panduan-5-kenapa.md` dengan contoh & kalimat yang harus dihindari, ditulis untuk pengguna awam | Ada, dengan panduan konkret + contoh kalimat yang dihindari |
| Regulasi data pribadi Indonesia (UU PDP) | Tidak dibahas sama sekali | Ada bagian khusus, dengan disclaimer bukan nasihat hukum dan rujukan ke skill/khusus |
| Perlu digabung berapa skill | 2+ skill terpisah (postmortem, update pelanggan) + `apology-letter` di plugin lain untuk hasil setara | 1 skill tunggal, satu perintah |
| Butuh setup/API/istilah asing | Perlu paham SLO/error budget/status-page untuk hasil maksimal | Tidak — cukup cerita kejadian dengan bahasa biasa |

## Kesimpulan
Untuk konteks target pembeli (UMKM/profesional Indonesia awam teknologi), `laporan-insiden-usaha` **menang jelas** dibanding gabungan skill sumbernya: bahasa lokal, satu skill (bukan 2-3 skill berantai), ada draf minta maaf + ringkasan WA yang tidak dimiliki pesaing sama sekali, ada penanganan UU PDP yang relevan secara hukum lokal, dan disiplin anti-mengarang angka yang tidak eksplisit di sumber. Kelemahan pesaing yang **tidak** diwarisi: istilah SLO/error budget/Gantt teknis yang justru akan membingungkan pemilik UMKM — dengan sengaja dihapus (dicatat di `ATTRIBUTION.md` bagian "Dihapus total"). Tidak ditemukan skill publik Indonesia sejenis sebagai pembanding langsung, sehingga posisi skill ini relatif unik di pasar lokal saat ini.
