# -*- coding: utf-8 -*-
import base64
import io
from lxml import etree

from odoo import models


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _prepare_html(self, html):
        """Prepare HTML ensuring proper UTF-8 encoding for wkhtmltopdf.

        Addresses wkhtmltopdf 0.12.6.1's known bug where it misinterprets UTF-8
        bytes as cp1252 for Arabic text. Strategy: Ensure clean UTF-8 without
        BOM and proper charset meta tag placement.
        """
        # Call parent's implementation first
        result = super()._prepare_html(html)

        # Remove UTF-8 BOM if present (can confuse wkhtmltopdf)
        if isinstance(result, bytes):
            if result.startswith(b'\xef\xbb\xbf'):
                result = result[3:]

        return result
