# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Tidak mengandung kode atau teks dari skill/pustaka pihak ketiga. Pembacaan XLSX ditulis sendiri
memakai modul standar Python (`zipfile`, `xml.etree`) berdasarkan struktur format Office Open XML
(ECMA-376 / ISO/IEC 29500) sebagai fakta format file; tidak memakai openpyxl/pandas.

Pola parsing angka format Indonesia/Inggris sengaja mengikuti perilaku skill Komunitech sendiri
`rekap-penjualan-csv` agar konsisten satu library, tetapi ditulis ulang dengan Decimal dan deteksi
gaya desimal per kolom.

Metode outlier (IQR 1,5× dengan kuartil inklusif, setara Excel `QUARTILE.INC`) adalah metode
statistik umum.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian.
