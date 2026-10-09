# Uji banding pesaing (skenario normal 1)

Penguji independen, 2026-09-29. Pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Pesaing yang dicari
Kata kunci: "PRD skill", "product spec skill", "create-prd", "product requirements agent skill" di GitHub, skills.sh, ClawHub, anthropics/skills.
- **phuryn/pm-skills `create-prd`** - pesaing terkuat: 26.657 bintang, 2.839 fork, dibuat 2026-03-01, push terakhir 2026-09-14, MIT (dicek via GitHub API 2026-09-29).
- product-on-purpose/pm-skills `deliver-prd` - 700 bintang, 90 fork, Apache-2.0, v3.0.0 (2026-08-21); fokus serah terima ke tim engineering.
- anthropics/skills: tidak ada skill PRD khusus (tidak ditemukan).
- Keduanya juga **sumber ATM** skill ini, jadi banding ini sekaligus menguji apakah nilai tambahnya nyata.

## Hasil pada prompt keripik tempe (simulasi agent mengikuti masing-masing skill)
| Kriteria (bobot) | create-prd (phuryn) | deliver-prd (PoP) | spesifikasi-produk-usaha |
|---|---|---|---|
| Relevan untuk produk fisik UMKM (20) | 8 - struktur OKR, stakeholder, "Contacts", "Technology"; tidak ada resep/kemasan/label | 6 - orientasi software, FR-n, "AI behavior", kontrak eksekutor | 19 - resep, kemasan, label, standar mutu |
| Angka dihitung & bisa diaudit (15) | 5 - tidak ada prioritas terhitung | 5 | 14 - script RICE/ICE, Decimal, penolakan baris rusak (dikurangi bug keyakinan pecahan) |
| Siap kirim ke pihak luar (15) | 6 | 9 | 14 - brief tanpa HPP/margin |
| Bahasa & konteks Indonesia (15) | 3 - bahasa Inggris | 3 | 14 |
| Legalitas/kepatuhan (15) | 0 | 0 | 9 - ada PIRT/BPOM/halal/notifkos + tautan, tapi tanpa SNI & tenggat halal 2026 |
| Metrik sukses & asumsi (10) | 9 - OKR SMART, asumsi eksplisit | 9 - baseline & target | 6 - asumsi ditandai, **tidak ada metrik sukses** |
| Jejak versi (10) | 2 | 5 | 9 |
| **Total (100)** | **33** | **37** | **85** |

## Kelebihan pesaing yang patut dipelajari (tulis ulang dengan cara sendiri)
1. **Metrik keberhasilan** (target terukur, mis. "repeat order 30% dalam 2 bulan", "rating rasa >= 4,5"). Skill kita tidak punya bagian ini.
2. "Why now / latar belakang" singkat - berguna saat dokumen dibaca investor/mitra.
3. Pertanyaan terbuka (open questions) sebagai bagian terpisah dari risiko.

**Kesimpulan:** skill kita **menang jelas** untuk audiens UMKM Indonesia. Tidak ada batas skor 6 dari banding pesaing.
