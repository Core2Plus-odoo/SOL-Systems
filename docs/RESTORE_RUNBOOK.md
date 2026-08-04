# SOL Systems — Data Restore / Re-import Runbook

Use this after an Odoo.sh restore that is missing recent (June) data, or when
rebuilding a fresh instance from this repo.

The code (module) redeploys automatically from GitHub `main`. This runbook is
only about **data**.

---

## Situation A — You restored a pre-June backup (your current case)

The restored database already contains everything **up to and including INV-6**
(2026-06-02) plus the April–May bills, payroll, and bank statements. Do **NOT**
re-import those files — they already exist and re-importing would create
duplicates.

You only need to add the **June gap**:

### A1. Add the recovered June invoices (INV-7, INV-8)
1. In Odoo: **Accounting → Customers → Invoices** → list view.
2. Top-left **⚙ / Favorites → Import records** (or the **Import** button).
3. Upload `odoo_imports/09_recovered_june_invoices.csv`.
4. Map columns (they match Odoo field names / external IDs already). The
   `tax_ids/id` value `__import__.tax_sale_15` must resolve to your existing
   **15% Sales VAT** tax — if the external ID differs, map the tax column to
   the 15% sales tax by name instead.
5. **Test**, then **Import**.
6. Open INV-7 and INV-8, verify amounts, then **Confirm** (post) each.

> INV-7: SOL Gulf, 250,000.00 + 15% VAT = **287,500.00** (e-Inv 220626123631350)
> INV-8: SOL Gulf, 30,705.44 + 15% VAT = **35,311.26**, dated 2026-06-28
>
> INV-8's original e-Inv number wasn't captured; the module regenerates one on
> post. If you have the original PDF, copy its e-Inv number into the `ref`
> field.

### A2. Other June transactions NOT in this repo
The repo does **not** contain June vendor bills or June bank statement lines
(bank statements stop at May). If June bills / bank movements are also missing,
re-enter them from source documents (bank portal export, vendor invoices).
There is no automated source for these in the repo.

### A3. Mark INV-8 as paid (it was Paid before)
Register the payment on INV-8 to match its previous "Paid" state
(**Register Payment**, Immediate Payment, 2026-06-28).

---

## Situation B — Fresh/empty instance (full rebuild)

Import in this exact order (dependencies first). Use
**Settings → Technical → Import** or each model's list-view **Import** button.
Match on the `id` / external-ID columns so relations link up.

### B1. Master data (`master_data/`)
1. `00_taxes.csv` — taxes (creates `tax_sale_15`, etc.)
2. `07_product_categories.csv` — product categories
3. `06_payment_terms.csv` — payment terms
4. `04_products_services.csv` — sold services
5. `05_products_expenses.csv` — expense products
6. `01_res_partner_customers.csv` — customers
7. `02_res_partner_vendors.csv` — vendors
8. `03_res_partner_employees.csv` — employees
9. `05_journal_sales_setup.txt` — follow the notes to configure the sales
   journal / chart-of-accounts codes (400200, 400300, etc.) used by the
   imports.

### B2. Opening balances
Post the opening trial balance from `docs/trial_balance_31dec2025.md` as a
manual journal entry dated 2025-12-31 (or via an "Opening Balances" journal).

### B3. Transactions (`odoo_imports/`)
1. `01_customer_invoices.csv` — INV-1…INV-6 + CN-1
2. `09_recovered_june_invoices.csv` — INV-7, INV-8
3. `02_astrolabs_bills.csv`
4. `03_flexistart_bills.csv`
5. `04_gosi_bills.csv`
6. `06_misc_vendor_bills.csv`
7. `05_payroll_journal_entries.csv`
8. `07_snb_bank_statement.csv`
9. `08_riyadh_bank_statement.csv`

### B4. Post & reconcile
- Confirm (post) all invoices/bills.
- Reconcile the two bank statements against the posted invoices/bills.
- Verify the trial balance matches `docs/trial_balance_31dec2025.md` for the
  opening position.

---

## Verify (both situations)
- **Accounting → Reporting → Trial Balance / P&L** — sanity-check totals.
- Print a **Bilingual Tax Invoice** on INV-7 to confirm the report still works.
- Fill the **Arabic Name** on customers/products if you want the Arabic lines
  (these are not stored in the CSVs and must be re-entered).
