// Membuat budget Actual ASLI (lewat @actual-app/api 26.9.0) berisi data fiktif,
// lalu mencetak hasil getBudgetMonth sebagai acuan angka.
const api = require('@actual-app/api');
const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');
fs.rmSync(dataDir, { recursive: true, force: true });
fs.mkdirSync(dataDir, { recursive: true });

const rp = n => Math.round(n * 100); // Rupiah -> integer sen

(async () => {
  await api.init({ dataDir });
  await api.runImport('Studio Rina (fiktif)', async () => {
    const bca = await api.createAccount({ name: 'BCA Usaha', offbudget: false }, rp(5000000));
    const kas = await api.createAccount({ name: 'Kas Tunai', offbudget: false }, rp(500000));
    const tab = await api.createAccount({ name: 'Tabungan Pajak', offbudget: true }, 0);

    const grp = await api.getCategoryGroups();
    const gInc = grp.find(g => g.is_income).id;
    await api.updateCategoryGroup(gInc, { name: 'Pemasukan' });
    const gUsaha = await api.createCategoryGroup({ name: 'Biaya Usaha' });
    const gPribadi = await api.createCategoryGroup({ name: 'Kebutuhan Pribadi' });
    const gCad = await api.createCategoryGroup({ name: 'Dana Cadangan' });

    const c = {};
    c.proyek = await api.createCategory({ name: 'Pendapatan Proyek', group_id: gInc, is_income: true });
    c.lain = await api.createCategory({ name: 'Pendapatan Lain', group_id: gInc, is_income: true });
    c.sewa = await api.createCategory({ name: 'Sewa Coworking', group_id: gUsaha });
    c.inet = await api.createCategory({ name: 'Internet & Pulsa', group_id: gUsaha });
    c.soft = await api.createCategory({ name: 'Software & Langganan', group_id: gUsaha });
    c.trans = await api.createCategory({ name: 'Transportasi', group_id: gUsaha });
    c.iklan = await api.createCategory({ name: 'Iklan', group_id: gUsaha });
    c.makan = await api.createCategory({ name: 'Makan', group_id: gPribadi });
    c.rumah = await api.createCategory({ name: 'Belanja Rumah', group_id: gPribadi });
    c.pajak = await api.createCategory({ name: 'Pajak', group_id: gCad });
    c.darurat = await api.createCategory({ name: 'Dana Darurat', group_id: gCad });
    c.lama = await api.createCategory({ name: 'Ojek Online', group_id: gUsaha });
    c.arsip = await api.createCategory({ name: 'Arsip Lama', group_id: gUsaha, hidden: true });

    // Saldo awal dibuat otomatis oleh createAccount (tanggal hari ini) -> pindahkan ke 1 Juli
    for (const a of [bca, kas]) {
      const ts = await api.getTransactions(a, '2000-01-01', '2100-01-01');
      for (const t of ts) if (t.starting_balance_flag) await api.updateTransaction(t.id, { date: '2026-07-01' });
    }

    // Anggaran
    const B = { sewa: 1500000, inet: 450000, soft: 600000, trans: 800000, iklan: 1000000, makan: 2500000, rumah: 1200000, pajak: 1000000, darurat: 500000, lama: 200000 };
    for (const m of ['2026-07', '2026-08', '2026-09']) {
      for (const [k, v] of Object.entries(B)) await api.setBudgetAmount(m, c[k], rp(v));
    }
    await api.setBudgetAmount('2026-09', c.trans, rp(900000));
    await api.setBudgetCarryover('2026-08', c.pajak, true); // sisa minus Pajak Agustus dibawa ke September

    const tx = [
      // Juli
      ['2026-07-03', 7500000, 'PT Maju Kreatif', 'proyek', bca],
      ['2026-07-05', -1500000, 'Coworking Hub', 'sewa', bca],
      ['2026-07-07', -350000, 'Telkomsel', 'inet', bca],
      ['2026-07-10', -250000, 'Adobe', 'soft', bca],
      ['2026-07-12', -620000, 'Pertamina', 'trans', bca],
      ['2026-07-15', -900000, 'Meta Ads', 'iklan', bca],
      ['2026-07-18', -2100000, 'Warung & Resto', 'makan', kas],
      ['2026-07-20', -800000, 'Superindo', 'rumah', bca],
      ['2026-07-25', -150000, 'Gojek', 'lama', bca],
      // Agustus
      ['2026-08-02', 9000000, 'CV Sinar Abadi', 'proyek', bca],
      ['2026-08-05', -1500000, 'Coworking Hub', 'sewa', bca],
      ['2026-08-07', -350000, 'Telkomsel', 'inet', bca],
      ['2026-08-10', -250000, 'Adobe', 'soft', bca],
      ['2026-08-12', -1150000, 'Pertamina', 'trans', bca],
      ['2026-08-14', -2600000, 'DJP (setoran PPh)', 'pajak', bca],
      ['2026-08-18', -2300000, 'Warung & Resto', 'makan', kas],
      ['2026-08-21', -1000000, 'Superindo', 'rumah', bca],
      ['2026-08-28', -120000, 'Gojek', 'lama', bca],
      // September
      ['2026-09-02', 8250000, 'PT Maju Kreatif', 'proyek', bca],
      ['2026-09-04', 150000, 'Bunga Bank', 'lain', bca],
      ['2026-09-05', -1500000, 'Coworking Hub', 'sewa', bca],
      ['2026-09-08', -380000, 'Telkomsel', 'inet', bca],
      ['2026-09-10', -890000, 'Figma & Adobe', 'soft', bca],
      ['2026-09-12', -450000, 'Pertamina', 'trans', bca],
      ['2026-09-13', -3200000, 'Meta Ads', 'iklan', bca],
      ['2026-09-16', -1800000, 'Warung & Resto', 'makan', kas],
      ['2026-09-20', -1350000.5, 'Superindo', 'rumah', bca],
      ['2026-09-22', -90000, 'Gojek', 'lama', bca],
    ];
    for (const [date, amt, payee, cat, acct] of tx) {
      await api.addTransactions(acct, [{ date, amount: rp(amt), payee_name: payee, category: c[cat] }]);
    }

    // Split September: belanja Tokopedia 700rb = 400rb Software + 300rb Belanja Rumah
    await api.addTransactions(bca, [{
      date: '2026-09-18', amount: rp(-700000), payee_name: 'Tokopedia',
      subtransactions: [
        { amount: rp(-400000), category: c.soft, notes: 'lisensi font' },
        { amount: rp(-300000), category: c.rumah, notes: 'alat dapur' },
      ],
    }]);

    // Transaksi tanpa kategori (September)
    await api.addTransactions(bca, [{ date: '2026-09-24', amount: rp(-275000), payee_name: 'QRIS Toko XYZ' }]);

    // Transaksi yang dihapus (tombstone) — tidak boleh terhitung
    const ids = await api.addTransactions(bca, [{ date: '2026-09-25', amount: rp(-5000000), payee_name: 'Salah Input', category: c.iklan }]);
    const all = await api.getTransactions(bca, '2026-09-25', '2026-09-25');
    for (const t of all) if (t.amount === rp(-5000000)) await api.deleteTransaction(t.id);

    // Transfer BCA -> Kas (tarik tunai): on-budget ke on-budget, tanpa kategori
    const payees = await api.getPayees();
    const toKas = payees.find(p => p.transfer_acct === kas);
    const toTab = payees.find(p => p.transfer_acct === tab);
    await api.addTransactions(bca, [{ date: '2026-09-15', amount: rp(-1000000), payee: toKas.id }], { runTransfers: true });
    // Transfer ke akun off-budget (Tabungan Pajak) — berkategori Pajak
    await api.addTransactions(bca, [{ date: '2026-09-26', amount: rp(-600000), payee: toTab.id, category: c.pajak }], { runTransfers: true });

    // Kategori 'Ojek Online' dihapus & dipindah ke 'Transportasi'
    await api.deleteCategory(c.lama, c.trans);
  });

  const budgets = await api.getBudgets();
  const out = { budgets, months: {} };
  for (const m of ['2026-07', '2026-08', '2026-09']) out.months[m] = await api.getBudgetMonth(m);
  fs.writeFileSync(path.join(__dirname, 'acuan.json'), JSON.stringify(out, null, 2));
  await api.shutdown();
  console.log('selesai', JSON.stringify(budgets));
})().catch(e => { console.error(e); process.exit(1); });
