# ZATCA — Pre-August-2026 invoices erroneously CLEARED in production

**Issue:** With the ZATCA (l10n_sa_edi) integration go-live = **1 August 2026**,
the following documents dated **before 1 Aug 2026** were nonetheless submitted
to and **accepted (cleared/reported) by ZATCA in production**. They are real,
previously-reported sales, so this is a **duplicate-clearance / process** error,
not a tax-understatement. Reversal decision belongs to the ZATCA advisor.

**Cutoff going forward:** only invoices dated **1 Aug 2026 and onwards** may be
sent to ZATCA.

## Documents

| # | Doc | Date | Customer | Type | Net SAR | VAT 15% | Total SAR |
|---|-----|------|----------|------|--------:|--------:|----------:|
| 1 | INV-1 | 2026-04-14 | KPMG Professional Services | invoice | 207,843.75 | 31,176.56 | 239,020.31 |
| 2 | INV-2 | 2026-04-14 | SOL Gulf Communications | invoice | 68,233.72 | 10,235.06 | 78,468.78 |
| 3 | CN-1 | 2026-05-10 | KPMG Professional Services | credit note | -207,843.75 | -31,176.56 | -239,020.31 |
| 4 | INV-3 | 2026-05-13 | KPMG Professional Services | invoice | 207,843.75 | 31,176.56 | 239,020.31 |
| 5 | INV-4 | 2026-05-18 | SOL Gulf Communications | invoice | 24,133.72 | 3,620.06 | 27,753.78 |
| 6 | INV-5 | 2026-05-31 | KPMG Professional Services | invoice | 69,281.25 | 10,392.19 | 79,673.44 |
| 7 | INV-6 | 2026-06-02 | KPMG Professional Services | invoice | 69,281.25 | 10,392.19 | 79,673.44 |
| 8 | INV-7 | 2026-06-22 | SOL Gulf Communications | invoice | 250,000.00 | 37,500.00 | 287,500.00 |
| 9 | INV-8 | 2026-06-28 | SOL Gulf Communications | invoice | 30,705.44 | 4,605.82 | 35,311.26 |
| | **TOTAL** | | | | **719,479.13** | **107,921.88** | **827,401.01** |

> Amounts are from the accounting records in this repo. **Fill the ZATCA-side
> fields from Odoo before sending to the advisor:** ICV (invoice counter),
> Clearance/Reporting UUID, cleared timestamp, and the QR/hash — one row each.

## Recommended handling (for the ZATCA advisor to confirm)
- These are **genuine, already-VAT-reported** invoices → **do not reverse with
  credit notes** without explicit advisor direction (would cancel real revenue).
- Likely path: **document the error + voluntary disclosure to ZATCA** about the
  early/duplicate clearance of pre-integration-date invoices.
- Note the **counter (ICV)/hash-chain** values consumed, so the going-forward
  numbering stays consistent.

## Prevention (in progress)
- Journal ZATCA e-invoicing disabled during cleanup.
- A cutoff guard to block any invoice dated < 2026-08-01 from ZATCA submission
  (pending confirmation of the EDI format technical name / staging test).
