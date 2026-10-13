# Uji kabar HILANG/TERLAMBAT ke Telegram (2026-10-13, C18)

**Skill:** `pantau-cron-openclaw` v1.0.2 (catalog; SKILL.md tidak diubah)  
**Penguji:** penguji otomatis Komunitech, independen  
**Bot:** bot uji Komunitech (gateway uji internal)  
**Grup uji:** grup uji Telegram internal, topik forum **C18 pantau-cron — uji kabar**  
**Verdik:** **LOLOS** (kabarnya; lihat catatan alur chat)

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Job tes tanpa lapor selesai terdaftar? | Ya — job fiktif `uji-alarm`, jadwal ±06.41 WIB, toleransi 1 menit |
| Pengawas jadwal otomatis jalan? | Ya — job perintah `pantau_cron.py cek --openclaw` tiap menit, pengiriman ke topik uji |
| Kabar **HILANG** tiba di Telegram? | Ya — pesan bot berisi blok `PANTAU CRON` dan baris `HILANG uji-alarm` |
| Isi sesuai (tanpa data pribadi)? | Ya — hanya nama job uji dan waktu jadwal terlewat |

## Cuplikan pesan kabar (Telegram)

```
PANTAU CRON - 14 Okt 06.43 WIB
BERMASALAH (1 dari 1):

• HILANG uji-alarm: belum pernah lapor selesai sejak didaftarkan (1 jadwal terlewat, terakhir 14 Okt 06.41 WIB). Cek apakah langkah "lapor selesai" sudah ditambahkan di akhir jadwal otomatis itu.
```

## Langkah uji (ringkas)

1. Skill dipasang di home gateway uji; topik forum baru untuk C18; skill aktif hanya di topik itu.  
2. Pesan ke bot (mention): minta rencana pantau + job tes `uji-alarm` ~4 menit ke depan. Bot membalas **Working** lama (gangguan API Telegram/getUpdates); rencana utuh via chat **tidak** selesai dalam run ini.  
3. Penguji melengkapi langkah teknis sesuai SKILL.md §5 & `references/openclaw-jadwal.md`: daftar `uji-alarm`, buat job pengawas perintah dengan `--announce` ke topik uji.  
4. Setelah jadwal + toleransi lewat, pengawas mengirim kabar **HILANG** (cuplikan di atas).

## Cacat / catatan

- Alur **rencana → balas "ya" → pasang otomatis lewat bot** belum terbukti end-to-end di run ini karena balasan bot terhenti di *Working* (konflik polling / error jaringan Telegram di log gateway). Kabar HILANG tetap terbukti lewat job pengawas yang sama seperti panduan skill.  
- Job pengawas uji (`C18 pengawas uji-alarm`) dan data folder `pantau-cron` di home gateway **dihapus/dimatikan** setelah uji agar tidak mengganggu gelombang lain.

## Pesan uji penguji (≤4)

1. Permintaan pasang pantau + job tes peringatan (mention bot).  
2. *(Rencana bot via chat tidak sampai — hanya Working.)*  
3. —  
4. —  

Kabar HILANG = pesan bot terpisah (bukan balasan langsung ke pesan 1).
