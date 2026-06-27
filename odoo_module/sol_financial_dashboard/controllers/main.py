# -*- coding: utf-8 -*-
import json
from collections import defaultdict

from odoo import http
from odoo.http import request

from .templates import DASHBOARD_HTML


class SolDashboardController(http.Controller):

    @http.route('/sol_dashboard', type='http', auth='user')
    def dashboard_page(self, **kw):
        return request.make_response(DASHBOARD_HTML, headers=[('Content-Type', 'text/html')])

    @http.route('/sol_dashboard/data', type='http', auth='user', methods=['GET'], csrf=False)
    def dashboard_data(self, **kw):
        data = self._compute_data()
        return request.make_response(
            json.dumps(data, default=str),
            headers=[('Content-Type', 'application/json')],
        )

    def _compute_data(self):
        env = request.env
        Move = env['account.move']
        MoveLine = env['account.move.line']
        BankLine = env['account.bank.statement.line']
        company = env.company

        revenue_by_month = defaultdict(float)
        invoices_data = []
        sale_moves = Move.search([
            ('move_type', 'in', ('out_invoice', 'out_refund')),
            ('state', '=', 'posted'),
            ('company_id', '=', company.id),
        ], order='invoice_date')
        for m in sale_moves:
            if not m.invoice_date:
                continue
            month = m.invoice_date.strftime('%Y-%m')
            revenue_by_month[month] += m.amount_untaxed_signed
            invoices_data.append({
                'name': m.name,
                'date': str(m.invoice_date),
                'partner': m.partner_id.display_name or '',
                'total': round(m.amount_untaxed_signed, 2),
                'type': m.move_type,
            })

        expense_by_month = defaultdict(float)
        expense_by_account = defaultdict(float)
        vendor_spend = defaultdict(float)
        purchase_moves = Move.search([
            ('move_type', 'in', ('in_invoice', 'in_refund')),
            ('state', '=', 'posted'),
            ('company_id', '=', company.id),
        ])
        for m in purchase_moves:
            if not m.invoice_date:
                continue
            month = m.invoice_date.strftime('%Y-%m')
            expense_by_month[month] += m.amount_untaxed_signed
            vendor_spend[m.partner_id.display_name or ''] += m.amount_untaxed_signed
            for line in m.invoice_line_ids.filtered(lambda l: l.display_type == 'product'):
                acct = line.account_id.display_name or line.account_id.code or 'Unmapped'
                expense_by_account[acct] += line.balance

        # Manual journal entries booked straight to expense accounts (e.g. payroll runs)
        misc_lines = MoveLine.search([
            ('move_id.state', '=', 'posted'),
            ('move_id.move_type', '=', 'entry'),
            ('account_id.internal_group', '=', 'expense'),
            ('company_id', '=', company.id),
        ])
        for line in misc_lines:
            if not line.date:
                continue
            month = line.date.strftime('%Y-%m')
            expense_by_month[month] += line.balance
            acct = line.account_id.display_name or line.account_id.code or 'Unmapped'
            expense_by_account[acct] += line.balance

        banks = {}
        bank_journals = env['account.journal'].search([
            ('type', '=', 'bank'), ('company_id', '=', company.id),
        ])
        for journal in bank_journals:
            lines = BankLine.search([('journal_id', '=', journal.id)], order='date, id')
            running = 0.0
            timeline = []
            in_total = out_total = 0.0
            for l in lines:
                amt = l.amount
                running += amt
                if amt > 0:
                    in_total += amt
                else:
                    out_total += -amt
                timeline.append({
                    'date': str(l.date),
                    'amount': round(amt, 2),
                    'balance': round(running, 2),
                    'ref': l.payment_ref or l.narration or '',
                })
            banks[journal.name] = {
                'account_number': journal.bank_account_id.acc_number if journal.bank_account_id else '',
                'in_total': round(in_total, 2),
                'out_total': round(out_total, 2),
                'net': round(running, 2),
                'timeline': timeline,
                'txn_count': len(lines),
            }

        flags = []
        flagged_moves = Move.search([
            ('company_id', '=', company.id),
            '|', '|',
            ('ref', 'ilike', 'WARNING'),
            ('ref', 'ilike', 'REVIEW'),
            ('state', '=', 'draft'),
        ], limit=100)
        for m in flagged_moves:
            if m.state == 'draft':
                note = 'Draft — not yet posted'
            else:
                note = m.ref or ''
            flags.append({
                'doc': m.name or m.ref or '(unsaved)',
                'partner': m.partner_id.display_name or '',
                'date': str(m.invoice_date or m.date or ''),
                'note': note,
            })

        total_revenue = sum(revenue_by_month.values())
        total_expense = sum(expense_by_month.values())

        return {
            'company': company.name,
            'currency': company.currency_id.symbol or company.currency_id.name,
            'revenue_by_month': dict(sorted(revenue_by_month.items())),
            'expense_by_month': dict(sorted(expense_by_month.items())),
            'expense_by_account': dict(sorted(
                ((k, round(v, 2)) for k, v in expense_by_account.items()),
                key=lambda x: -x[1],
            )),
            'invoices': sorted(invoices_data, key=lambda x: x['date']),
            'invoices_count': len(invoices_data),
            'bills_count': len(purchase_moves),
            'total_revenue_excl': round(total_revenue, 2),
            'total_expense_excl': round(total_expense, 2),
            'banks': banks,
            'vendor_spend': sorted(
                ({'name': k, 'amount': round(v, 2)} for k, v in vendor_spend.items()),
                key=lambda x: -x['amount'],
            ),
            'flags': flags,
        }
