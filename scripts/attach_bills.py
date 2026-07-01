#!/usr/bin/env python3
"""
Attach bill/invoice PDFs to matching Odoo records via XML-RPC.

Usage:
    python3 attach_bills.py \
        --url https://your-odoo-instance.odoo.com \
        --db your-database-name \
        --user your@email.com \
        --password "your-api-key-or-password" \
        --data-dir /path/to/extracted/Data

The script will:
  1. Search Odoo for vendor bills (account.move, move_type=in_invoice)
     and customer invoices (move_type=out_invoice) by partner name.
  2. Attach each PDF/image to the best-matching record as an ir.attachment.
  3. Print a summary of matched and unmatched files.

Folder → vendor mapping (edit VENDOR_MAP below if partner names differ in Odoo):
  "Astro Labs - Invoices"             -> "Astro Labs"
  "FlexiStart - Invoices"             -> "FlexiStart"
  "Gosi Invoices"                     -> "GOSI" / "General Organization for Social Insurance"
  "Etimad"                            -> "Etimad"
  "Laptop Invoice"                    -> (unmatched — no clear vendor; attaches to first draft bill)
  "Muneeb Exit Reentry Bill"          -> (expense — attaches as standalone attachment)
  "Muneeb Iqamah, Work Permit payments" -> (expense)
  "Payroll (payment data)"            -> (payroll — attaches as standalone)
  "QIWA Subscription Fee"             -> "QIWA" / "Qiwa"
  "Salamah Insurance Bill"            -> "Tameeni" / "Salamah"
  "Sameer Hasan Iqama Bill"           -> (expense)
  "Saudi Competitiveness & Business Center" -> "Saudi Competitiveness"
  "SNB BID Bond"                      -> "SNB" / "Saudi National Bank"
  "Tally Prime - Saudi Gisco Company" -> "Gisco" / "Saudi Gisco"
  "Travel Expenses Reimbursed to Muneeb Khan" -> (expense)
  "SOL SYSTEMS LTD - Customer Invoices" -> customer invoices (out_invoice)
  SNB Bank Statements                 -> bank journal entries
  Riyadh Bank Statements              -> bank journal entries
"""

import argparse
import base64
import mimetypes
import os
import sys
import xmlrpc.client
from pathlib import Path

# ---------------------------------------------------------------------------
# Edit this map to match exact partner names in YOUR Odoo database.
# Key = folder name under "Historical Bookkeeping Data/"
# Value = list of Odoo partner name fragments to search (case-insensitive)
# ---------------------------------------------------------------------------
VENDOR_MAP = {
    "Astro Labs - Invoices":                    ["Astro Labs"],
    "FlexiStart - Invoices":                    ["FlexiStart", "Flexi Start"],
    "Gosi Invoices":                            ["GOSI", "General Organization for Social Insurance"],
    "Etimad":                                   ["Etimad"],
    "QIWA Subscription Fee":                    ["Qiwa", "QIWA"],
    "Salamah Insurance Bill":                   ["Tameeni", "Salamah", "Bupa"],
    "Saudi Competitiveness & Business Center":  ["Saudi Competitiveness", "Business Center"],
    "SNB BID Bond":                             ["Saudi National Bank", "SNB"],
    "Tally Prime - Saudi Gisco Company":        ["Gisco", "Saudi Gisco"],
    "Laptop Invoice":                           [],   # no clear partner — will skip auto-match
    "Muneeb Exit Reentry Bill":                 [],   # expense receipts — no vendor bill
    "Muneeb Iqamah, Work Permit payments":      [],
    "Payroll (payment data)":                   [],
    "Sameer Hasan Iqama Bill":                  [],
    "Travel Expenses Reimbursed to Muneeb Khan": [],
    "2025 Financial Statements & Audit 2025 Docs": [],  # audit docs — skip
}

CUSTOMER_INVOICE_FOLDER = "SOL SYSTEMS LTD - Customer Invoices"
BANK_FOLDERS = ["SNB Bank Statements", "Riyadh Bank Statements"]


def connect(url, db, user, password):
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)
    uid = common.authenticate(db, user, password, {})
    if not uid:
        print("ERROR: Authentication failed. Check URL, database, username, and password/API key.")
        sys.exit(1)
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)
    return uid, models


def search_partner(models, db, uid, password, name_fragments):
    """Return partner IDs matching any of the name fragments."""
    domain = ["|"] * (len(name_fragments) - 1) if len(name_fragments) > 1 else []
    for frag in name_fragments:
        domain += [("name", "ilike", frag)]
    return models.execute_kw(db, uid, password, "res.partner", "search", [domain])


def find_bills(models, db, uid, password, partner_ids, move_type="in_invoice"):
    """Return account.move IDs for given partner(s) and move type, sorted newest first."""
    if not partner_ids:
        return []
    return models.execute_kw(
        db, uid, password, "account.move", "search",
        [[("partner_id", "in", partner_ids), ("move_type", "=", move_type)]],
        {"order": "invoice_date desc, id desc"},
    )


def already_attached(models, db, uid, password, res_model, res_id, filename):
    """Check if an attachment with this filename already exists on the record."""
    count = models.execute_kw(
        db, uid, password, "ir.attachment", "search_count",
        [[("res_model", "=", res_model), ("res_id", "=", res_id), ("name", "=", filename)]],
    )
    return count > 0


def attach_file(models, db, uid, password, filepath, res_model, res_id, dry_run=False):
    filename = Path(filepath).name
    if already_attached(models, db, uid, password, res_model, res_id, filename):
        print(f"  [SKIP] Already attached: {filename}")
        return False
    mime, _ = mimetypes.guess_type(str(filepath))
    mime = mime or "application/octet-stream"
    with open(filepath, "rb") as f:
        data_b64 = base64.b64encode(f.read()).decode("ascii")
    if dry_run:
        print(f"  [DRY-RUN] Would attach: {filename} -> {res_model}({res_id})")
        return True
    models.execute_kw(
        db, uid, password, "ir.attachment", "create",
        [{
            "name": filename,
            "type": "binary",
            "datas": data_b64,
            "mimetype": mime,
            "res_model": res_model,
            "res_id": res_id,
        }],
    )
    print(f"  [OK] Attached: {filename} -> {res_model}({res_id})")
    return True


def process_vendor_folder(models, db, uid, password, folder_path, partner_fragments, dry_run):
    files = [f for f in folder_path.rglob("*") if f.is_file()]
    if not files:
        return

    if not partner_fragments:
        print(f"\n[SKIP] {folder_path.name} — no vendor mapping defined (attach manually)")
        return

    partner_ids = search_partner(models, db, uid, password, partner_fragments)
    if not partner_ids:
        print(f"\n[NO PARTNER] '{folder_path.name}' — no Odoo partner found for {partner_fragments}")
        print(f"  Files to attach manually:")
        for f in files:
            print(f"    {f.name}")
        return

    bill_ids = find_bills(models, db, uid, password, partner_ids, "in_invoice")
    if not bill_ids:
        print(f"\n[NO BILLS] '{folder_path.name}' — partner found but no vendor bills in Odoo")
        print(f"  Partner IDs: {partner_ids}")
        print(f"  Files to attach manually:")
        for f in files:
            print(f"    {f.name}")
        return

    print(f"\n[VENDOR] {folder_path.name} — {len(files)} file(s) -> {len(bill_ids)} bill(s)")

    if len(files) == len(bill_ids):
        # 1-to-1 match by sort order (newest file → newest bill)
        pairs = sorted(files, key=lambda f: f.name)
        for filepath, bill_id in zip(pairs, bill_ids):
            attach_file(models, db, uid, password, filepath, "account.move", bill_id, dry_run)
    else:
        # Attach all files to every matched bill
        print(f"  (count mismatch: {len(files)} files vs {len(bill_ids)} bills — attaching all to all)")
        for filepath in files:
            for bill_id in bill_ids:
                attach_file(models, db, uid, password, filepath, "account.move", bill_id, dry_run)


def process_customer_invoices(models, db, uid, password, folder_path, dry_run):
    files = [f for f in folder_path.rglob("*") if f.is_file()]
    if not files:
        return
    print(f"\n[CUSTOMER INVOICES] {folder_path.name} — {len(files)} file(s)")
    # Get all customer invoices sorted oldest first
    inv_ids = models.execute_kw(
        db, uid, password, "account.move", "search",
        [[("move_type", "=", "out_invoice")]],
        {"order": "invoice_date asc, id asc"},
    )
    if not inv_ids:
        print("  No customer invoices found in Odoo.")
        return
    print(f"  Found {len(inv_ids)} customer invoice(s) in Odoo")
    for filepath in sorted(files, key=lambda f: f.name):
        # Try to find invoice by matching filename hint (Inv #01 -> oldest, etc.)
        # Default: attach to the first available invoice for review
        print(f"  Attaching {filepath.name} to invoice {inv_ids[0]} (edit script to re-map)")
        attach_file(models, db, uid, password, filepath, "account.move", inv_ids[0], dry_run)


def process_bank_statements(models, db, uid, password, folder_path, dry_run):
    files = [f for f in folder_path.rglob("*") if f.is_file()]
    if not files:
        return
    bank_name = folder_path.name
    print(f"\n[BANK STATEMENTS] {bank_name} — {len(files)} file(s)")
    # Find bank journals matching the bank name
    journal_ids = models.execute_kw(
        db, uid, password, "account.journal", "search",
        [[("type", "=", "bank"), ("name", "ilike", bank_name.split()[0])]],
    )
    if not journal_ids:
        # Try generic bank journal
        journal_ids = models.execute_kw(
            db, uid, password, "account.journal", "search",
            [[("type", "=", "bank")]],
        )
    if not journal_ids:
        print(f"  No bank journal found. Attach manually.")
        return
    journal_id = journal_ids[0]
    print(f"  Using journal ID {journal_id}")
    for filepath in files:
        attach_file(models, db, uid, password, filepath, "account.journal", journal_id, dry_run)


def main():
    parser = argparse.ArgumentParser(description="Attach bill PDFs to Odoo records via XML-RPC")
    parser.add_argument("--url", required=True, help="Odoo URL e.g. https://mycompany.odoo.com")
    parser.add_argument("--db", required=True, help="Odoo database name")
    parser.add_argument("--user", required=True, help="Odoo login email")
    parser.add_argument("--password", required=True, help="Odoo password or API key")
    parser.add_argument("--data-dir", required=True, help="Path to extracted Data folder")
    parser.add_argument("--dry-run", action="store_true", help="Preview matches without uploading")
    args = parser.parse_args()

    uid, models = connect(args.url, args.db, args.user, args.password)
    print(f"Connected as uid={uid}")

    data_root = Path(args.data_dir)
    historical = data_root / "Historical Bookkeeping Data"

    # Process vendor bill folders
    for folder_name, partner_fragments in VENDOR_MAP.items():
        folder_path = historical / folder_name
        if folder_path.exists():
            process_vendor_folder(models, args.db, uid, args.password,
                                  folder_path, partner_fragments, args.dry_run)

    # Customer invoices
    customer_folder = historical / CUSTOMER_INVOICE_FOLDER
    if customer_folder.exists():
        process_customer_invoices(models, args.db, uid, args.password,
                                  customer_folder, args.dry_run)

    # Bank statements
    for bank_folder_name in BANK_FOLDERS:
        bank_folder = data_root / bank_folder_name
        if bank_folder.exists():
            process_bank_statements(models, args.db, uid, args.password,
                                    bank_folder, args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
