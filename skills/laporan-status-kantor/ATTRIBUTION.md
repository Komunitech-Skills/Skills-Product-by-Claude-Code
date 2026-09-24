# Atribusi

Skill `laporan-status-kantor` **terinspirasi dari struktur** skill **internal-comms** karya
**Anthropic, PBC**, dan **diubah/diperluas secara substansial**:

- Sumber: https://github.com/anthropics/skills/tree/main/skills/internal-comms
- Commit yang diambil: `34040c9c568585f6929bedeaad110ad08f079624` (commit terbaru repo saat
  diambil via `git clone --depth 1`, 2026-09-10), diambil dan ditinjau 2026-09-24
- Lisensi sumber: Apache License, Version 2.0 (teks lengkap di bawah). Diverifikasi langsung
  dari `LICENSE.txt` di folder skill sumber (bukan diasumsikan dari README) — isinya teks
  Apache-2.0 standar, hak cipta "Copyright 2026 Anthropic, PBC." Tidak ada file `NOTICE`
  terpisah di folder sumber.

**Pemberitahuan perubahan file (sesuai Bagian 4(b) Apache License 2.0): file-file yang
berasal dari atau terinspirasi struktur sumber TELAH DIUBAH** — lihat rincian di bawah.
Tidak ada kode/teks sumber yang disalin verbatim; seluruh isi SKILL.md, README, template,
dan referensi ditulis ulang dari nol dalam Bahasa Indonesia.

Adaptasi oleh Komunitech (komunitech.com). Penggunaan versi adaptasi ini tunduk pada
`LISENSI.txt` yang disertakan dalam paket pembelian, **tanpa mengurangi** ketentuan lisensi
Apache-2.0 di bawah untuk bagian yang berasal dari karya asli.

## Proporsi isi sumber vs baru
Skill sumber sangat ringkas: `SKILL.md` 32 baris + 4 file `examples/` (3p-updates.md 46
baris, company-newsletter.md 65 baris, faq-answers.md 29 baris, general-comms.md 15 baris)
= sekitar 187 baris total, mencakup 4 jenis komunikasi (3P, newsletter, FAQ, "general
comms"). Versi ini menghasilkan SKILL.md + README + 9 file `templates/` + 1 file
`references/` = jauh lebih dari 1.000 baris, mencakup **9 jenis** komunikasi (3 varian
audiens 3P — atasan/pemilik, tim, klien — masing dipisah karena aturan isinya berbeda;
laporan harian WFH/WFO; newsletter kantor kecil; pengumuman internal termasuk
libur/jam kerja/THR; FAQ karyawan; memo/surat edaran; laporan insiden 5W1H). **Mayoritas
isi (isi konkret template, aturan lokal, contoh) adalah tulisan baru Komunitech**; yang
diambil dari sumber murni gagasan struktural tingkat tinggi (lihat bawah).

## Yang diambil dari sumber (gagasan, bukan teks)
- Gagasan mengelompokkan komunikasi internal ke beberapa jenis baku dengan file panduan
  terpisah per jenis, dimuat sesuai kebutuhan (pola "load file panduan yang sesuai jenis
  permintaan").
- Format 3P (Progress/Plans/Problems) sebagai salah satu jenis laporan status internal,
  termasuk gagasan "ringkas, 30-60 detik dibaca" dan pembagian tiga bagian.
- Gagasan newsletter internal sebagai rangkuman periodik dengan beberapa bagian bertema.
- Gagasan FAQ sebagai kumpulan pertanyaan berulang + jawaban terstandardisasi.
- Gagasan menyarankan sumber data (di sumber: Slack/Drive/Email/Calendar perusahaan besar)
  sebagai bahan — di versi ini diganti total karena target pembeli kami adalah UMKM/kantor
  kecil Indonesia yang umumnya **tidak** punya integrasi Slack/Google Workspace berbayar;
  versi ini bekerja murni dari bahan yang ditempel/diketik pengguna (chat WA, poin, voice
  note), sesuai prinsip "tanpa setup" perpustakaan skill ini.

## Yang diubah / ditambahkan oleh Komunitech
1. **Audiens 3P dipecah jadi 3 template terpisah dengan aturan isi berbeda**
   (`templates/3p-ke-atasan-pemilik.md`, `3p-ke-tim.md`, `3p-ke-klien.md`) — sumber hanya
   punya SATU file 3P generik untuk "executives, leadership, teammates" tanpa membedakan
   aturan konten. Versi ini menambahkan aturan eksplisit: versi klien melarang membocorkan
   masalah internal (SDM, keuangan internal) dan wajib sopan-formal; versi tim boleh lebih
   teknis dan menyebut nama/tugas; versi atasan fokus hasil selesai + kendala yang perlu
   keputusan saja.
2. **5 jenis komunikasi baru yang tidak ada sama sekali di sumber**: laporan harian
   WFH/WFO, pengumuman internal (libur nasional/cuti bersama/jam kerja/THR), memo/surat
   edaran internal bergaya kop surat Indonesia, laporan insiden 5W1H ke pemilik. Sumber
   hanya mencakup 3P, newsletter, FAQ, dan satu file umum ("general-comms" tanpa format
   baku).
3. **Lokalisasi penuh Indonesia**: 100% Bahasa Indonesia; format WhatsApp/Telegram
   (`*tebal*`, bullet pendek, batas panjang baris untuk layar HP) sebagai kanal DEFAULT
   (`references/panduan-nada-dan-kanal.md`) — sumber ditulis untuk Slack/email perusahaan
   AS berbahasa Inggris dan tidak membahas format WA sama sekali.
4. **Dua nada budaya kantor Indonesia** (sopan-formal vs santai-profesional) dengan
   panduan kapan memakai masing-masing dan contoh berdampingan — sumber tidak membahas
   perbedaan nada formal/informal sama sekali, hanya "matter-of-fact, not prose-heavy".
5. **Dukungan bilingual ID/EN** dengan aturan penulisan (versi ID lengkap dulu, lalu EN,
   tidak dicampur) — tidak ada di sumber (sumber berbahasa Inggris tunggal).
6. **Pagar anti-mengarang data** eksplisit di setiap langkah dan checklist SKILL.md:
   dilarang mengarang progres/angka/tanggal, tandai `[isi: ...]` untuk info hilang, tanya
   sekali bukan berulang. Sumber tidak membahas risiko mengarang data sama sekali.
7. **Rujukan silang ke skill lain di library** untuk hal di luar cakupan (perhitungan THR
   → `hitung-thr`, notulen rapat → `notulen-rapat`, surat resmi ke pihak luar →
   `surat-resmi`, komunikasi ke pelanggan → `caption-sosmed-umkm`/`broadcast-wa`/
   `balas-chat-cs`/`follow-up-prospek`, kontrak → `perjanjian-sederhana`, surat peringatan
   karyawan → `surat-peringatan-karyawan`) — konsep "skill lain dalam satu perpustakaan"
   tidak relevan untuk sumber yang berdiri sendiri.
8. **Perlindungan data pribadi karyawan** eksplisit (larangan mencantumkan gaji individu,
   kondisi kesehatan, alasan cuti pribadi tanpa izin) sesuai prinsip UU PDP di CLAUDE.md
   — tidak dibahas di sumber.
9. **Panduan khusus pengumuman THR/libur nasional/cuti bersama**: penegasan tanggal resmi
   (SKB 3 Menteri) dan nominal THR TIDAK dihitung/dikarang oleh skill ini, wajib diisi
   pengguna atau diarahkan ke skill hitung terpisah — konsep ini spesifik konteks Indonesia
   dan tidak ada di sumber (perusahaan AS tidak punya THR/cuti bersama).
10. **Dihapus**: rujukan ke `license: Complete terms in LICENSE.txt` di frontmatter (repo
    ini memakai frontmatter hanya `name`+`description` sesuai standar CLAUDE.md), dan
    seluruh rujukan ke tool internal perusahaan besar (Slack/Google Drive/Email/Calendar
    korporat) yang tidak relevan untuk UMKM/kantor kecil Indonesia.

## Audit keamanan sumber (Tahap 3 CLAUDE.md)
- Seluruh isi `SKILL.md` dan 4 file `examples/*.md` sumber dibaca penuh sebelum digunakan.
  Tidak ada script (`scripts/` kosong/tidak ada) — murni instruksi teks.
- Tidak ditemukan perintah shell destruktif, pola unduh-lalu-eksekusi langsung dari
  internet, kode ter-obfuskasi, atau dependensi mencurigakan (tidak ada script sama
  sekali).
- Tidak ditemukan pengiriman data ke server pihak ketiga di luar sepengetahuan pengguna;
  rujukan ke "Slack/Google Drive/Email/Calendar" di sumber adalah instruksi ke AGENT untuk
  memakai *tool/konektor yang sudah dimiliki pengguna sendiri* (bukan panggilan jaringan
  tersembunyi milik skill), sama seperti pola tool-use biasa.
- Tidak ditemukan pola prompt injection tersembunyi (dicek pola "ignore previous
  instructions", "disregard", "secretly", "without informing the user", "do not tell the
  user" — nihil kecocokan di kelima file).
- Tidak ditemukan API key, token, atau data pribadi tertanam.
- **Hasil: LULUS audit keamanan**, sesuai catatan awal di
  `research/sources/kurasi-terbukti-2026-09-23.md` §4.

## Teks lisensi asli (Apache License, Version 2.0)

Disalin persis dari
`https://raw.githubusercontent.com/anthropics/skills/main/skills/internal-comms/LICENSE.txt`:

```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright 2026 Anthropic, PBC.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```
