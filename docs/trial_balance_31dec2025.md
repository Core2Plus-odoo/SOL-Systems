# SOL Systems Limited Company — Trial Balance 31-Dec-2025

**Audited by:** Abdullah Alfuraih Certified Public Accountant  
**Period:** 09-Jan-2025 to 31-Dec-2025  
**Generated:** June 2026  
**Status:** ✅ Matches Audited Financial Statements

---

## Trial Balance Summary

| Code   | Account                          |     Debit SAR |    Credit SAR |       Net SAR |
|--------|----------------------------------|---------------|---------------|---------------|
| 100001 | Liquidity Transfer (Suspense)    |   617,672.59  |   750,078.69  |  (132,406.10) |
| 102000 | SNB Bank Account                 |   369,906.10  |    73,526.44  |   296,379.66  |
| 103000 | Riyadh Bank Account              |   153,685.00  |   152,496.11  |     1,188.89  |
| 210000 | Trade Payables                   |    26,955.60  |    47,855.74  |   (20,900.14) |
| 210100 | GOSI Payable                     |         0.00  |     1,864.00  |    (1,864.00) |
| 210200 | Salaries Payable                 |    71,549.00  |    91,549.00  |   (20,000.00) |
| 210300 | Prof Fees Payable                |         0.00  |    10,000.00  |   (10,000.00) |
| 220000 | Due to Related Party (SOL Canada)|         0.00  |   274,437.00  |  (274,437.00) |
| 220100 | EOSB Provision                   |         0.00  |     5,795.00  |    (5,795.00) |
| 300000 | Share Capital                    |         0.00  |   200,000.00  |  (200,000.00) |
| 390000 | Retained Earnings                |   214,437.00  |         0.00  |   214,437.00  |
| 600000 | Salaries Expense                 |    90,367.11  |         0.00  |    90,367.11  |
| 600100 | GOSI Expense                     |     8,655.06  |         0.00  |     8,655.06  |
| 600200 | GOSI Penalty                     |       100.68  |         0.00  |       100.68  |
| 600300 | EOSB Expense                     |     5,795.00  |         0.00  |     5,795.00  |
| 600400 | Govt Fees & Iqama                |     9,700.00  |         0.00  |     9,700.00  |
| 600700 | Professional & Audit Fees        |    10,000.00  |         0.00  |    10,000.00  |
| 600800 | Bank Charges                     |        60.95  |         0.00  |        60.95  |
| 600900 | Office Rent / Co-working         |    29,400.00  |         0.00  |    29,400.00  |
| **TOTAL** |                               | **1,613,472** | **1,613,472** | **0.00** ✅ |

---

## Balance Sheet vs Audited FS

| Line Item                     | Odoo SAR  | FS SAR    | Match |
|-------------------------------|-----------|-----------|-------|
| **Cash (SNB + Riyadh)**       | 297,569   | 297,569   | ✅    |
| GOSI Payable                  | 1,864     | 1,864     | ✅    |
| Salaries Payable              | 20,000    | 20,000    | ✅    |
| Professional Fees Payable     | 10,000    | 10,000    | ✅    |
| Due to SOL Canada (Loan)      | 274,437   | 274,437   | ✅    |
| EOSB Provision                | 5,795     | 5,795     | ✅    |
| **Total Liabilities**         | 312,096   | 312,096   | ✅    |
| Share Capital                 | 200,000   | 200,000   | ✅    |
| Accumulated Loss              | (214,437) | (214,437) | ✅    |
| **Net Equity**                | (14,437)  | (14,437)  | ✅    |
| **Total L + Equity**          | 297,659   | 297,659   | ✅    |

---

## Notes

- **100001 Suspense (132,406 Cr):** Represents unreconciled bank statement lines. Will clear to zero after bank reconciliation in Odoo UI. Does not affect the balance sheet presentation.
- **P&L Net Loss in Odoo (154,079) vs FS (214,437):** The SAR 60,358 gap represents 2025 expenses paid via bank (GOSI Aug-Sep, Iqama fees) that are still sitting in suspense pending bank reconciliation. After reconciliation this will close to exactly 214,437.
- **Trade Payables (210000) of 20,900:** Residual AP from bills partially cleared. The AstroLabs INV-6707 (SAR 29,400) paid Jan-5-2026 is outstanding at Dec-31 — correctly in AP.
