# -*- coding: utf-8 -*-
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Financial Dashboard</title>
<script src="/sol_financial_dashboard/static/lib/chart.umd.js"></script>
<script src="/sol_financial_dashboard/static/lib/chartjs-adapter-date-fns.bundle.min.js"></script>
<style>
  :root{
    --bg:#f4f6fb; --panel:#ffffff; --panel2:#f8f9fc; --border:#e3e7f0;
    --txt:#1b2236; --muted:#6b7280; --accent:#5b8cff; --accent2:#0891b2;
    --green:#16a34a; --red:#e11d48; --amber:#d97706;
    --divider:rgba(15,23,42,.06); --hover:rgba(15,23,42,.03); --bg-glow:#dde5fb;
    --radius:14px;
  }
  html[data-theme="dark"]{
    --bg:#0b1020; --panel:#11182e; --panel2:#0e1426; --border:#1f2a45;
    --txt:#e7ecf7; --muted:#8a93ab; --accent:#5b8cff; --accent2:#22d3ee;
    --green:#34d399; --red:#fb7185; --amber:#fbbf24;
    --divider:rgba(255,255,255,.04); --hover:rgba(255,255,255,.02); --bg-glow:#15224a;
  }
  *{box-sizing:border-box;}
  body{
    margin:0; font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,sans-serif;
    background:radial-gradient(1200px 600px at 10% -10%, var(--bg-glow) 0%, var(--bg) 55%) fixed;
    color:var(--txt); min-height:100vh; transition:background .2s, color .2s;
  }
  .theme-toggle{
    display:flex; align-items:center; gap:8px; cursor:pointer; user-select:none;
    background:var(--panel); border:1px solid var(--border); border-radius:999px;
    padding:8px 14px; font-size:12.5px; color:var(--muted); font-weight:600;
  }
  .theme-toggle:hover{color:var(--txt);}
  .wrap{max-width:1400px;margin:0 auto;padding:28px 28px 60px;}
  header{display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:16px; margin-bottom:28px;}
  .brand{display:flex; align-items:center; gap:14px;}
  .logo{
    width:46px;height:46px;border-radius:12px;
    background:linear-gradient(135deg,var(--accent),var(--accent2));
    display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px;color:#06122b;
    box-shadow:0 8px 24px rgba(91,140,255,.35);
  }
  h1{font-size:22px;margin:0;font-weight:700;letter-spacing:.2px;}
  .sub{color:var(--muted);font-size:13px;margin-top:2px;}
  .period-badge{
    background:var(--panel); border:1px solid var(--border); border-radius:999px;
    padding:8px 16px; font-size:12.5px; color:var(--muted); display:flex; gap:8px; align-items:center;
  }
  .period-badge b{color:var(--txt); font-weight:600;}
  .dot{width:7px;height:7px;border-radius:50%; background:var(--green); box-shadow:0 0 8px var(--green);}

  .kpis{display:grid; grid-template-columns:repeat(5,1fr); gap:16px; margin-bottom:24px;}
  .kpi{
    background:linear-gradient(180deg,var(--panel),var(--panel2));
    border:1px solid var(--border); border-radius:var(--radius); padding:18px 20px;
    position:relative; overflow:hidden;
  }
  .kpi .label{font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:.6px; font-weight:600;}
  .kpi .value{font-size:26px; font-weight:800; margin-top:8px; letter-spacing:-.3px;}
  .kpi .delta{font-size:12.5px; margin-top:6px; font-weight:600;}
  .delta.up{color:var(--green);} .delta.down{color:var(--red);} .delta.flat{color:var(--muted);}

  .grid{display:grid; grid-template-columns:1.4fr 1fr; gap:18px; margin-bottom:18px;}
  .card{
    background:linear-gradient(180deg,var(--panel),var(--panel2));
    border:1px solid var(--border); border-radius:var(--radius); padding:20px;
  }
  .card h3{margin:0 0 4px; font-size:14.5px; font-weight:700;}
  .card .hint{color:var(--muted); font-size:11.5px; margin-bottom:14px;}
  .card-head{display:flex; justify-content:space-between; align-items:baseline;}
  .pill{font-size:11px; padding:3px 9px; border-radius:999px; font-weight:700;}
  .pill.amber{background:rgba(251,191,36,.15); color:var(--amber);}
  canvas{max-height:280px;}

  table{width:100%; border-collapse:collapse; font-size:13px;}
  th{text-align:left; color:var(--muted); font-weight:600; font-size:11.5px; text-transform:uppercase; letter-spacing:.4px; padding:8px 6px; border-bottom:1px solid var(--border);}
  td{padding:9px 6px; border-bottom:1px solid var(--divider);}
  tr:hover td{background:var(--hover);}
  .num{text-align:right; font-variant-numeric:tabular-nums; font-weight:600;}
  .neg{color:var(--red);} .pos{color:var(--green);}
  .tag{font-size:10.5px; padding:2px 7px; border-radius:6px; background:rgba(91,140,255,.15); color:var(--accent2); font-weight:700;}

  .bank-row{display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid var(--divider);}
  .bank-row:last-child{border-bottom:none;}
  .bank-name{font-weight:700; font-size:14px;}
  .bank-acct{color:var(--muted); font-size:11px; margin-top:2px;}
  .bank-bal{font-size:20px; font-weight:800; text-align:right;}
  .bank-bal .small{display:block; font-size:11px; color:var(--muted); font-weight:500; margin-top:2px;}

  .flag-item{display:flex; gap:12px; padding:10px 0; border-bottom:1px solid var(--divider); align-items:flex-start;}
  .flag-item:last-child{border-bottom:none;}
  .flag-dot{width:8px;height:8px;border-radius:50%;background:var(--amber); margin-top:6px; flex-shrink:0; box-shadow:0 0 6px var(--amber);}
  .flag-doc{font-weight:700; font-size:13px;}
  .flag-meta{font-size:11.5px; color:var(--muted); margin-top:1px;}
  .flag-note{font-size:12px; color:var(--txt); opacity:.75; margin-top:3px;}
  .empty{color:var(--muted); font-size:13px; padding:20px 0; text-align:center;}

  footer{margin-top:30px; text-align:center; color:var(--muted); font-size:11.5px;}
  @media (max-width:1100px){ .kpis{grid-template-columns:repeat(2,1fr);} .grid{grid-template-columns:1fr;} }
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="brand">
      <div class="logo">SOL</div>
      <div>
        <h1 id="companyName">Financial Dashboard</h1>
        <div class="sub">Live data from Odoo Accounting</div>
      </div>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
      <div class="period-badge"><span class="dot"></span> <span id="refreshedAt">Loading…</span></div>
      <div class="theme-toggle" id="themeToggle"><span id="themeIcon">🌙</span> <span id="themeLabel">Dark mode</span></div>
    </div>
  </header>

  <div class="kpis" id="kpis"></div>

  <div class="grid">
    <div class="card">
      <div class="card-head">
        <div>
          <h3>Revenue vs. Expenses</h3>
          <div class="hint">Monthly, excl. VAT — posted invoices/bills vs. journal entries</div>
        </div>
      </div>
      <canvas id="revExpChart"></canvas>
    </div>
    <div class="card">
      <div class="card-head">
        <div>
          <h3>Expense Breakdown</h3>
          <div class="hint">By GL account (excl. VAT)</div>
        </div>
      </div>
      <canvas id="expPie"></canvas>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="card-head">
        <div>
          <h3>Bank Balance Trend</h3>
          <div class="hint">Running balance per bank journal</div>
        </div>
      </div>
      <canvas id="bankChart"></canvas>
    </div>
    <div class="card">
      <h3>Account Balances</h3>
      <div class="hint">Current closing balance per bank journal</div>
      <div id="bankBoxes"></div>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="card-head">
        <div>
          <h3>Top Vendors by Spend</h3>
          <div class="hint">Cumulative excl. VAT</div>
        </div>
      </div>
      <table id="vendorTable"></table>
    </div>
    <div class="card">
      <div class="card-head">
        <div>
          <h3>Data Quality Flags</h3>
          <div class="hint">Draft documents and refs tagged WARNING / REVIEW</div>
        </div>
        <span class="pill amber" id="flagCount"></span>
      </div>
      <div id="flagList"></div>
    </div>
  </div>

  <div class="card">
    <div class="card-head">
      <div>
        <h3>Customer Invoices &amp; Credit Notes</h3>
        <div class="hint">All posted AR documents</div>
      </div>
    </div>
    <table id="invoiceTable"></table>
  </div>

  <footer>SOL Financial Dashboard · live data from Odoo Accounting</footer>
</div>

<script>
const FMT = n => n.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});

(function initTheme(){
  const saved = localStorage.getItem('sol_dashboard_theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  document.getElementById('themeIcon').textContent = saved === 'dark' ? '☀️' : '🌙';
  document.getElementById('themeLabel').textContent = saved === 'dark' ? 'Light mode' : 'Dark mode';
  document.getElementById('themeToggle').addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem('sol_dashboard_theme', next);
    document.documentElement.setAttribute('data-theme', next);
    location.reload();
  });
})();

fetch('/sol_dashboard/data').then(r => r.json()).then(D => {
  const CUR = D.currency || '';
  const MONEY = n => CUR + ' ' + FMT(n);

  document.getElementById('companyName').textContent = D.company + ' — Financial Dashboard';
  document.getElementById('refreshedAt').innerHTML = 'Refreshed <b>' + new Date().toLocaleString() + '</b>';

  const grossProfit = D.total_revenue_excl - D.total_expense_excl;
  const margin = D.total_revenue_excl ? (grossProfit / D.total_revenue_excl * 100) : 0;
  const bankEntries = Object.entries(D.banks || {});
  const totalCash = bankEntries.reduce((s, [,b]) => s + b.net, 0);

  const kpis = [
    {label:'Total Revenue (excl. VAT)', value: MONEY(D.total_revenue_excl), delta:`${D.invoices_count} documents`, cls:'flat'},
    {label:'Total Expenses (excl. VAT)', value: MONEY(D.total_expense_excl), delta:`${D.bills_count} bills`, cls:'flat'},
    {label:'Net Result', value: MONEY(grossProfit), delta: (grossProfit>=0?'▲ ':'▼ ') + margin.toFixed(1)+'% margin', cls: grossProfit>=0?'up':'down'},
    {label:'Total Cash on Hand', value: MONEY(totalCash), delta: bankEntries.length + ' bank journal(s)', cls:'up'},
    {label:'Open Data Flags', value: D.flags.length, delta:'Review before posting', cls:'down'},
  ];
  document.getElementById('kpis').innerHTML = kpis.map(k => `
    <div class="kpi">
      <div class="label">${k.label}</div>
      <div class="value">${k.value}</div>
      <div class="delta ${k.cls}">${k.delta}</div>
    </div>`).join('');

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const gridColor = isDark ? 'rgba(255,255,255,.06)' : 'rgba(15,23,42,.06)';
  Chart.defaults.color = isDark ? '#8a93ab' : '#6b7280';
  Chart.defaults.font.family = "'Segoe UI', sans-serif";
  Chart.defaults.borderColor = gridColor;

  const months = Array.from(new Set([...Object.keys(D.revenue_by_month), ...Object.keys(D.expense_by_month)])).sort();
  const revData = months.map(m => D.revenue_by_month[m] || 0);
  const expData = months.map(m => D.expense_by_month[m] || 0);

  new Chart(document.getElementById('revExpChart'), {
    type:'bar',
    data:{ labels: months, datasets:[
      {label:'Revenue', data:revData, backgroundColor:'#5b8cff', borderRadius:6, maxBarThickness:34},
      {label:'Expenses', data:expData, backgroundColor:'#fb7185', borderRadius:6, maxBarThickness:34},
    ]},
    options:{
      responsive:true,
      plugins:{legend:{position:'top', labels:{boxWidth:10, usePointStyle:true, pointStyle:'circle'}}},
      scales:{
        y:{grid:{color:gridColor}, ticks:{callback:v=>(v/1000)+'k'}},
        x:{grid:{display:false}}
      }
    }
  });

  const accLabels = Object.keys(D.expense_by_account);
  const accVals = Object.values(D.expense_by_account);
  const palette = ['#5b8cff','#22d3ee','#34d399','#fbbf24','#fb7185','#a78bfa','#f472b6','#60a5fa','#4ade80','#facc15','#fb923c','#38bdf8','#c084fc','#f87171'];
  if (accLabels.length) {
    new Chart(document.getElementById('expPie'), {
      type:'doughnut',
      data:{labels:accLabels, datasets:[{data:accVals, backgroundColor:palette, borderWidth:0}]},
      options:{
        responsive:true,
        plugins:{legend:{position:'right', labels:{boxWidth:10, font:{size:10.5}, usePointStyle:true, pointStyle:'circle'}}},
        cutout:'62%'
      }
    });
  } else {
    document.getElementById('expPie').replaceWith(Object.assign(document.createElement('div'), {className:'empty', textContent:'No posted expense lines yet'}));
  }

  if (bankEntries.length) {
    const colors = ['#5b8cff','#22d3ee','#34d399','#fbbf24'];
    new Chart(document.getElementById('bankChart'), {
      type:'line',
      data:{datasets: bankEntries.map(([name, b], i) => ({
        label:name,
        data: b.timeline.map(t => ({x:t.date, y:t.balance})),
        borderColor: colors[i % colors.length],
        backgroundColor: colors[i % colors.length] + '22',
        fill:true, tension:.25, pointRadius:0, borderWidth:2.5,
      }))},
      options:{
        responsive:true,
        plugins:{legend:{position:'top', labels:{boxWidth:10, usePointStyle:true, pointStyle:'circle'}}},
        scales:{
          x:{type:'time', time:{unit:'month'}, grid:{display:false}},
          y:{grid:{color:gridColor}, ticks:{callback:v=>(v/1000)+'k'}}
        }
      }
    });
  } else {
    document.getElementById('bankChart').replaceWith(Object.assign(document.createElement('div'), {className:'empty', textContent:'No bank statement lines found'}));
  }

  document.getElementById('bankBoxes').innerHTML = bankEntries.length ? (
    bankEntries.map(([name, b]) => `
      <div class="bank-row">
        <div><div class="bank-name">${name}</div><div class="bank-acct">${b.account_number || ''} · ${b.txn_count} txns</div></div>
        <div class="bank-bal">${MONEY(b.net)}<span class="small">In ${MONEY(b.in_total)} · Out ${MONEY(b.out_total)}</span></div>
      </div>`).join('') +
    `<div class="bank-row" style="border-top:1px solid var(--border); margin-top:6px; padding-top:14px;">
      <div><div class="bank-name" style="color:var(--accent2)">Combined Cash Position</div></div>
      <div class="bank-bal" style="color:var(--accent2)">${MONEY(totalCash)}</div>
    </div>`
  ) : '<div class="empty">No bank journals found</div>';

  const vendorTotal = D.vendor_spend.reduce((s,x)=>s+x.amount,0) || 1;
  document.getElementById('vendorTable').innerHTML = D.vendor_spend.length ? `
    <thead><tr><th>Vendor</th><th class="num">Spend (excl. VAT)</th><th class="num">% of Total</th></tr></thead>
    <tbody>
      ${D.vendor_spend.map(v => `
        <tr>
          <td>${v.name}</td>
          <td class="num">${MONEY(v.amount)}</td>
          <td class="num">${(v.amount / vendorTotal * 100).toFixed(1)}%</td>
        </tr>`).join('')}
    </tbody>` : '<tbody><tr><td class="empty">No posted vendor bills yet</td></tr></tbody>';

  document.getElementById('flagCount').textContent = D.flags.length + ' open';
  document.getElementById('flagList').innerHTML = D.flags.length ? D.flags.map(f => `
    <div class="flag-item">
      <div class="flag-dot"></div>
      <div>
        <div class="flag-doc">${f.doc} <span class="tag">${f.partner}</span></div>
        <div class="flag-meta">${f.date}</div>
        <div class="flag-note">${f.note}</div>
      </div>
    </div>`).join('') : '<div class="empty">No open flags</div>';

  document.getElementById('invoiceTable').innerHTML = D.invoices.length ? `
    <thead><tr><th>Document</th><th>Date</th><th>Customer</th><th>Type</th><th class="num">Amount (excl. VAT)</th></tr></thead>
    <tbody>
      ${D.invoices.map(i => `
        <tr>
          <td><b>${i.name}</b></td>
          <td>${i.date}</td>
          <td>${i.partner}</td>
          <td><span class="tag" style="background:${i.type==='out_refund'?'rgba(251,113,133,.15)':'rgba(52,211,153,.15)'}; color:${i.type==='out_refund'?'#fb7185':'#34d399'}">${i.type === 'out_refund' ? 'Credit Note' : 'Invoice'}</span></td>
          <td class="num ${i.total<0?'neg':'pos'}">${i.total<0?'-':''}${MONEY(Math.abs(i.total))}</td>
        </tr>`).join('')}
    </tbody>` : '<tbody><tr><td class="empty">No posted customer invoices yet</td></tr></tbody>';

}).catch(err => {
  document.getElementById('kpis').innerHTML = '<div class="empty">Failed to load dashboard data: ' + err + '</div>';
});
</script>
</body>
</html>
"""
