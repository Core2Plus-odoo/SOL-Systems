# -*- coding: utf-8 -*-
from odoo import models


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _build_wkhtmltopdf_args(self, *args, **kwargs):
        """Force wkhtmltopdf to read its HTML input as UTF-8.

        wkhtmltopdf 0.12.6.1's Qt WebKit engine auto-detects the input
        charset from a byte-prefix window and, for our lean reports, guesses
        Windows-1252 (cp1252) instead of UTF-8. That mis-detection turns every
        Arabic character into mojibake (e.g. 'شركة' -> 'Ø´Ø±ÙƒØ©') even though
        the file is valid UTF-8 with a <meta charset="utf-8"> tag.

        Passing an explicit ``--encoding utf-8`` on the command line pins the
        input encoding so the auto-detector can't override it, which is the
        only layer that reliably fixes this: Odoo re-serializes the report
        HTML through lxml before invoking wkhtmltopdf, so HTML-level tricks
        (numeric character references, BOM tweaks) are undone before the
        engine ever sees them.

        The ``*args, **kwargs`` passthrough keeps this override immune to core
        signature changes across Odoo versions -- it only appends a flag to
        whatever argument list the parent builds. ``--encoding utf-8`` is
        correct for every Odoo report (Odoo always emits UTF-8), so applying
        it globally is safe.
        """
        command_args = super()._build_wkhtmltopdf_args(*args, **kwargs)
        if '--encoding' not in command_args:
            command_args = list(command_args) + ['--encoding', 'utf-8']
        return command_args
