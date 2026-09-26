const api = require('@actual-app/api'); const fs = require('fs'); const path = require('path');
const dataDir = path.join(__dirname, 'data-tracking'); fs.rmSync(dataDir, { recursive: true, force: true }); fs.mkdirSync(dataDir);
const rp = n => Math.round(n * 100);
(async () => {
  const lib = await api.init({ dataDir });
  await api.runImport('Toko Kue Sari (fiktif, tracking)', async () => {
    await lib.send('preferences/save', { id: 'budgetType', value: 'tracking' });
    const bank = await api.createAccount({ name: 'BRI Toko', offbudget: false }, rp(2000000));
    const g = await api.createCategoryGroup({ name: 'Operasional' });
    const bahan = await api.createCategory({ name: 'Bahan Kue', group_id: g });
    const kemas = await api.createCategory({ name: 'Kemasan', group_id: g });
    const inc = (await api.getCategories()).find(c => c.is_income && c.name === 'Income');
    for (const t of await api.getTransactions(bank, '2000-01-01', '2100-01-01')) if (t.starting_balance_flag) await api.updateTransaction(t.id, { date: '2026-08-01' });
    for (const m of ['2026-08', '2026-09']) { await api.setBudgetAmount(m, bahan, rp(3000000)); await api.setBudgetAmount(m, kemas, rp(500000)); }
    await api.setBudgetCarryover('2026-08', kemas, true);
    const tx = [['2026-08-03', 6000000, 'Pelanggan', inc.id], ['2026-08-05', -3400000, 'Toko Bahan', bahan], ['2026-08-07', -300000, 'Plastik', kemas],
      ['2026-09-03', 5000000, 'Pelanggan', inc.id], ['2026-09-05', -2800000, 'Toko Bahan', bahan], ['2026-09-07', -650000, 'Plastik', kemas]];
    for (const [date, a, p, c] of tx) await api.addTransactions(bank, [{ date, amount: rp(a), payee_name: p, category: c }]);
  });
  const b = (await api.getBudgets())[0]; await api.loadBudget(b.id);
  const prefs = await lib.send('preferences/get');
  const out = { prefs, months: {} };
  for (const m of ['2026-08', '2026-09']) out.months[m] = await api.getBudgetMonth(m);
  fs.writeFileSync(path.join(__dirname, 'acuan-tracking.json'), JSON.stringify(out, null, 1));
  await api.shutdown();
})().catch(e => { console.error(e); process.exit(1); });
