const api = require('@actual-app/api'); const fs=require('fs'); const path=require('path');
(async()=>{ await api.init({dataDir: path.join(__dirname,'data')});
 const b=(await api.getBudgets())[0]; await api.loadBudget(b.id);
 const out={budgets:[b],months:{}};
 for (const m of ['2026-07','2026-08','2026-09','2026-10']) out.months[m]=await api.getBudgetMonth(m);
 fs.writeFileSync(path.join(__dirname,'acuan-segar.json'),JSON.stringify(out,null,2)); await api.shutdown();})().catch(e=>{console.error(e);process.exit(1)});
