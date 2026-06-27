# -*- coding: utf-8 -*-
{
    'name': 'SOL Financial Dashboard',
    'version': '17.0.1.1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Live financial dashboard for SOL Systems (revenue, expenses, bank balances, vendor spend, data-quality flags)',
    'description': """
SOL Financial Dashboard
========================
Adds a single-page financial dashboard under Accounting that reads
live data straight from Odoo's accounting models:

* Revenue vs. expenses by month
* Expense breakdown by GL account
* Bank balance trend per bank journal (running balance)
* Top vendors by spend
* Customer invoices / credit notes
* Data-quality flags (draft documents, refs tagged WARNING/REVIEW)

No external data files or services are required — everything is
computed on the fly from account.move / account.move.line /
account.bank.statement.line.
""",
    'author': 'Core2Plus',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'views/dashboard_menu.xml',
    ],
    'installable': True,
    'application': False,
}
