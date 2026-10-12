# Format impor Anki (ringkas)

Anki desktop (gratis di ankiweb.net) menerima berkas teks dengan **tab** sebagai pemisah kolom.

## Basic dan Cloze terpisah
Jangan campur baris Basic (depan/belakang) dan Cloze (`{{c1::...}}`) dalam satu impor tanpa pemisah. Di chat, tulis dua blok:

```
#separator:tab
#notetype:Basic
…baris basic…
#notetype:Cloze
…baris cloze…
```

Impor **dua kali** di Anki (pilih tipe catatan yang sesuai per blok).

## Basic (Front / Back)
- Kolom 1: pertanyaan atau prompt
- Kolom 2: jawaban
- Kolom 3 (opsional): tag (satu token, tanpa spasi)

Saat impor: pilih pemisah **Tab**, map kolom ke Front / Back / Tags.

## Cloze
- Satu kalimat dengan bagian yang disembunyikan: `{{c1::jawaban}}`
- Kolom 1 berisi kalimat cloze; kolom 2 boleh kosong
- Saat impor, pilih tipe catatan **Cloze** (bukan Basic)

## Tips awam
- Jangan gunakan koma sebagai pemisah kolom (Anki default = tab).
- Baris kosong diabaikan; baris diawali `#` diabaikan Anki.
- Deck name dipilih **saat impor** di Anki, bukan di berkas TSV.

Skill Komunitech **tidak** menginstal Anki; pengguna impor manual.
