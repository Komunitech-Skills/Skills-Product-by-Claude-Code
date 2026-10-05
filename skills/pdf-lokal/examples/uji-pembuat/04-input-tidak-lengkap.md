# Contoh 4 (input tidak lengkap)

**Input pengguna:** "Gabungin PDF ini dong" (hanya menyebut 1 file, tidak ada file kedua)

**Respons agent yang benar:** tanyakan sekali - "File PDF mana saja yang mau digabung
(minimal 2), dan urutannya bagaimana?" - jangan langsung menjalankan `gabung` dengan
1 file, karena scriptnya memang menolak:

```
$ python3 scripts/pdf.py gabung resi1.pdf
GAGAL: Butuh minimal 2 file PDF untuk digabung.
```

Kasus lain: kunci PDF tanpa menyebut kata sandi → agent WAJIB tanya kata sandinya
ke pengguna, tidak boleh mengarang kata sandi sendiri (data sensitif).
