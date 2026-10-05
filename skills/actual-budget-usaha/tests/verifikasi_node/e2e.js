// Uji ujung-ke-ujung: CSV hasil skill -> parser CSV Actual (server) -> pemetaan kolom seperti
// ImportTransactionsModal (looselyParseAmount, parseDate 'yyyy mm dd', parseCategoryFields) ->
// importTransactions ke SALINAN budget -> getBudgetMonth.
const api = require('@actual-app/api'); const path = require('path');
// port looselyParseAmount (Actual 26.9.0, packages/loot-core/src/shared/util.ts, MIT) untuk uji
function looselyParseAmount(amount) {
  const extract = v => v.replace(/[^0-9-]/g, '');
  amount = amount.trim();
  if (amount.startsWith('(') && amount.endsWith(')')) amount = amount.replace('(', '-').replace(')', '');
  const m = amount.match(/[.,]([^.,]{4,9}|[^.,]{1,2})$/);
  if (!m || m.index === undefined) return parseFloat(extract(amount));
  return parseFloat(extract(amount.slice(0, m.index)) + '.' + extract(amount.slice(m.index + 1)));
}
(async () => {
  const lib = await api.init({ dataDir: path.join(__dirname, 'e2e', 'data') });
  const b = (await api.getBudgets())[0]; await api.loadBudget(b.id);
  const before = await api.getBudgetMonth('2026-09');
  const parsed = await lib.send('transactions-parse-file', { filepath: process.argv[2], options: { hasHeaderRow: true, delimiter: ',' } });
  if (parsed.errors.length) { console.log('ERR', parsed.errors); process.exit(1); }
  const cats = await api.getCategories();
  const acct = (await api.getAccounts()).find(a => a.name === 'BCA Usaha');
  const tx = parsed.transactions.map(r => {
    const cat = cats.find(c => c.name === r.Category); // parseCategoryFields: nama persis
    return { date: r.Date, payee_name: r.Payee, notes: r.Notes, amount: api.utils.amountToInteger(looselyParseAmount(r.Amount)), category: cat ? cat.id : undefined, imported_payee: r.Payee };
  });
  const res = await api.importTransactions(acct.id, tx);
  const after = await api.getBudgetMonth('2026-09');
  const g = m => Object.fromEntries(m.categoryGroups.flatMap(x => x.categories).map(c => [c.name, c.spent ?? c.received]));
  require("fs").writeFileSync(path.join(__dirname,"e2e-hasil.json"), JSON.stringify({ header: Object.keys(parsed.transactions[0]), rows: parsed.transactions.length, added: res.added.length, updated: res.updated.length, errors: res.errors, amounts: tx.map(t => t.amount), before: g(before), after: g(after), toBudgetBefore: before.toBudget, toBudgetAfter: after.toBudget }, null, 1));
  await api.shutdown();
})().catch(e => { console.error(e); process.exit(1); });
