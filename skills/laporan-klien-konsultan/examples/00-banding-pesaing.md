# Uji banding pesaing

> Dicari via web search (WebSearch), sesuai Tahap 6 CLAUDE.md. Kata kunci: "weekly client update"
> prompt/skill freelancer consultant github; ClawHub/skills.sh "client status report" freelancer
> consultant. Pesaing **hanya dibaca untuk dinilai**, tidak disalin isinya.

## Pesaing yang ditemukan
**`client-reporting` (author: reighlan)** — OpenClaw skill, terdaftar di clawskills.sh
(https://clawskills.sh/skills/reighlan-client-reporting). Halaman skill langsung (clawskills.sh)
diblokir oleh proxy egress lingkungan pengujian ini (`EGRESS_BLOCKED`), sehingga dinilai dari
cuplikan hasil pencarian (ringkasan clawskills.sh + referensi silang artikel lain tentang skill
sejenis), bukan dari isi SKILL.md penuhnya — catatan ini transparan soal keterbatasan itu.

Deskripsi dari cuplikan: "Automated client reporting for agencies and freelancers using OpenClaw.
Pulls metrics from Google Analytics 4, Google Search Console, and social media platforms to
generate branded weekly, monthly, or quarterly reports. Reports are delivered automatically via
email or Slack on a configurable per-client schedule."

Skill lain yang ditemukan tapi tidak relevan langsung (beda kebutuhan): `client-discovery` dan
`client-retention` (staybased, clawskills.sh) — soal percakapan discovery/retensi prospek, bukan
laporan progres berbasis log kerja.

## Penilaian berdampingan

| Aspek | `reighlan-client-reporting` (pesaing) | `laporan-klien-konsultan` (kita) |
|---|---|---|
| Sumber data | Google Analytics 4, Search Console, social media API | Log kerja harian yang dicatat konsultan sendiri (CSV lokal) |
| Cocok untuk | Agensi marketing/SEO yang melapor metrik traffic/sosial | Konsultan/freelancer lintas bidang (pajak, hukum, IT, desain, dll.) yang melapor **progres pekerjaan**, bukan metrik traffic |
| Setup | Perlu akun & kredensial GA4/Search Console/Slack/email terhubung | Tanpa API key/akun — hanya Python standar, sesuai prinsip "instan tanpa setup" |
| Pengiriman ke klien | **Otomatis** terkirim ke klien via email/Slack sesuai jadwal | **Tidak pernah otomatis** — draf selalu untuk ditinjau & dikirim manual oleh konsultan (keputusan pemilik 2026-09-23/26) |
| Perhitungan jam kerja | Tidak relevan (berbasis metrik traffic, bukan jam) | Total jam **dihitung script**, dengan penanda entri tanpa jam, bukan diasumsikan 0 |
| Deteksi data pribadi/rahasia | Tidak disebutkan di cuplikan | Ada (`POLA_SENSITIF`: NIK/KTP/HP/email/kata sandi), exit kode 3 sebagai peringatan tinjau |
| Lokalisasi Indonesia | Tidak ada (produk global, bahasa Inggris) | Bahasa Indonesia penuh, format tanggal Indonesia, UU PDP disebut eksplisit sebagai dasar aturan |
| Bukti pemakaian nyata | Terdaftar di direktori kurasi (clawskills.sh) — sinyal popularitas/umur belum bisa diverifikasi penuh dari halaman yang diblokir | Skill baru (v1.0.0), belum ada bukti pemakaian eksternal — wajar untuk skill orisinal baru |

## Kesimpulan
Kedua skill sama-sama menyasar "laporan rutin ke klien", tapi **beda kebutuhan inti**: pesaing
mengotomasi laporan **metrik marketing** dan sengaja mengirim langsung ke klien tanpa tinjauan
manusia — ini justru bertentangan dengan keputusan pemilik Komunitech (Tahap 6, "laporan ke klien
= draf yang ditinjau manusia, tidak pernah otomatis ke klien"), jadi arsitektur pesaing **tidak
bisa dan tidak seharusnya ditiru langsung** untuk pasar sasaran kita. Nilai tambah yang jelas dari
skill kita: nol setup (tanpa API key), cakupan lintas profesi (bukan cuma marketing), progres
kerja berbasis jam (bukan traffic), dan pagar keamanan tinjau-manual + deteksi data pribadi sesuai
UU PDP. Skill kita **tidak kalah** pada uji banding ini (tidak dibatasi skor maks. 6) — justru
mengisi kebutuhan yang secara sengaja tidak dipenuhi pesaing (pengiriman otomatis tanpa tinjauan).
