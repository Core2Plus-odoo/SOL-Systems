# ZATCA Phase 2 (Integration / Fatoora) — Setup Runbook

**Entity:** SOL Systems Limited Company (Riyadh, KSA) — VAT 312776217500003
**Goal:** Become ZATCA Phase-2 (Integration) compliant: signed UBL 2.1 XML
e-invoices with clearance (B2B) / reporting (B2C) to the Fatoora platform.

> Principle: **use Odoo's official ZATCA modules** (`l10n_sa`, `l10n_sa_edi`).
> Do NOT hand-build the cryptographic stamp / XML — the custom
> `sol_financial_dashboard` module only provides the bilingual PDF and keeps
> working alongside the official e-invoicing.

---

## 0. Portal links
- ZATCA: https://zatca.gov.sa/en
- Fatoora onboarding portal: https://fatoora.zatca.gov.sa

## 1. Prerequisites (do before touching Odoo)
1. Confirm your **integration wave / go-live date** — ZATCA notifies each
   taxpayer directly (minimum 6 months notice). You cannot onboard to
   production before your assigned date; you CAN test in the sandbox anytime.
2. Ensure the **VAT registration details** in Odoo exactly match ZATCA:
   legal name (EN + AR), VAT number (15 digits), CR number, address
   (building no., street, district, city, postal code, additional no.).
3. Decide invoice types you issue:
   - **Standard (B2B)** to KPMG / SOL Gulf → require **Clearance**.
   - **Simplified (B2C)** (if any) → require **Reporting** within 24h.

## 2. Enable the official modules in Odoo
1. **Apps** → update app list → install **"Saudi Arabia - E-invoicing"**
   (`l10n_sa_edi`); it pulls in `l10n_sa` and `account_edi`.
2. This adds the ZATCA EDI format, the onboarding wizard, and the Phase-2 QR.

> On Odoo.sh: installing a standard app is safe and separate from the custom
> module. It does not affect the bilingual PDF report.

## 3. Company / branch configuration
Settings → Companies → SOL Systems, and Accounting → Configuration:
- **Company legal name (AR + EN)**, VAT, CR number
- **Address** fully populated (building number, street, district, city,
  postal code, additional number) — ZATCA validates these
- Set the company's **industry / business category** if prompted
- On the **Sales Journal** used for customer invoices, enable the ZATCA EDI
  format (Accounting → Configuration → Journals → Advanced/EDI tab).

## 4. Onboarding (per journal / device)
Each sales journal acts as an EDI "device" and needs its own CSID.
1. In the journal's ZATCA section, click **Onboard** — Odoo generates a CSR.
2. In the **Fatoora portal**, generate an **OTP** (Onboard New Solution/Device)
   and paste it into Odoo.
3. Odoo submits the CSR → receives the **Compliance CSID (CCSID)**.
4. Odoo runs the **compliance checks** (sends sample standard + simplified
   invoices/credit/debit notes to the compliance API).
5. On success, Odoo requests the **Production CSID (PCSID)** — you are now live.

Start in the **sandbox/simulation** environment first, then switch the journal
to **production** once checks pass and your go-live date has arrived.

## 5. Day-to-day flow after onboarding
- Post a customer invoice → Odoo builds the signed UBL 2.1 XML (UUID, hash,
  PIH chain, cryptographic stamp) and the Phase-2 QR automatically.
- **B2B (standard):** invoice is sent for **Clearance**; once ZATCA returns
  the cleared XML + stamp, share it with the customer. The PDF (your bilingual
  layout) is attached alongside the XML.
- **B2C (simplified):** invoice is issued immediately and **Reported** to
  ZATCA within 24 hours.
- Monitor the EDI status on each invoice (To Send / Sent / Cleared / Rejected)
  and fix any rejections (usually address/VAT/format mismatches).

## 6. How the custom bilingual PDF fits in
- `sol_financial_dashboard`'s "Bilingual Tax Invoice" remains the human-
  readable PDF. Phase-2 compliance is carried by the XML + ZATCA QR from
  `l10n_sa_edi`.
- Optional: switch the invoice's QR image to the **`l10n_sa_edi` Phase-2 QR**
  (crypto stamp) instead of the current Phase-1 QR, so the printed PDF also
  shows the compliant QR. This is a small change to
  `sol_zatca_qr_datauri()` once the official module is installed — do it only
  after onboarding, and behind a fallback so pre-onboarding invoices still
  render the Phase-1 QR.

## 7. Checklist
- [ ] Integration date confirmed from ZATCA
- [ ] Company legal name (AR/EN), VAT, CR, full address correct in Odoo
- [ ] `l10n_sa_edi` installed; EDI enabled on the sales journal
- [ ] Sandbox compliance checks passed
- [ ] Production CSID obtained on/after go-live date
- [ ] First B2B invoice cleared; first B2C (if any) reported
- [ ] (Optional) Bilingual PDF QR switched to the Phase-2 crypto QR
