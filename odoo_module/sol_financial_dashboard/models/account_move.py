# -*- coding: utf-8 -*-
import base64
from urllib.parse import quote

from markupsafe import Markup

from odoo import fields, models

_EN_ONES = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
_EN_TEENS = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen',
             'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
_EN_TENS = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
_EN_SCALE = ['', 'Thousand', 'Million', 'Billion']

_AR_ONES = ['', 'واحد', 'اثنان', 'ثلاثة', 'أربعة', 'خمسة', 'ستة', 'سبعة', 'ثمانية', 'تسعة']
_AR_TEENS = ['عشرة', 'أحد عشر', 'اثنا عشر', 'ثلاثة عشر', 'أربعة عشر', 'خمسة عشر',
             'ستة عشر', 'سبعة عشر', 'ثمانية عشر', 'تسعة عشر']
_AR_TENS = ['', '', 'عشرون', 'ثلاثون', 'أربعون', 'خمسون', 'ستون', 'سبعون', 'ثمانون', 'تسعون']
_AR_HUNDREDS = ['', 'مائة', 'مائتان', 'ثلاثمائة', 'أربعمائة', 'خمسمائة',
                'ستمائة', 'سبعمائة', 'ثمانمائة', 'تسعمائة']
_AR_SCALE = ['', 'ألف', 'مليون', 'مليار']
_AR_DIGITS = '٠١٢٣٤٥٦٧٨٩'


def _en_under_1000(n):
    parts = []
    if n >= 100:
        parts.append(_EN_ONES[n // 100] + ' Hundred')
        n %= 100
    if 10 <= n < 20:
        parts.append(_EN_TEENS[n - 10])
    elif n >= 20:
        tens = _EN_TENS[n // 10]
        parts.append(tens + (' ' + _EN_ONES[n % 10] if n % 10 else ''))
    elif n > 0:
        parts.append(_EN_ONES[n])
    return ' '.join(parts)


def number_to_words_en(n):
    if n == 0:
        return 'Zero'
    groups = []
    scale = 0
    while n > 0:
        n, rem = divmod(n, 1000)
        if rem:
            groups.append((rem, scale))
        scale += 1
    groups.reverse()
    words = []
    for val, scale in groups:
        w = _en_under_1000(val)
        if scale:
            w += ' ' + _EN_SCALE[scale]
        words.append(w)
    return ' '.join(words)


def amount_to_words_en(amount, currency_name='Saudi Arabian Riyal', subunit_name='Halala'):
    riyals = int(amount)
    halalas = round((amount - riyals) * 100)
    parts = [currency_name, number_to_words_en(riyals)]
    if halalas:
        parts += ['and', number_to_words_en(halalas), subunit_name]
    parts.append('Only')
    return ' '.join(parts)


def _ar_under_1000(n):
    parts = []
    if n >= 100:
        parts.append(_AR_HUNDREDS[n // 100])
        n %= 100
    if 10 <= n < 20:
        parts.append(_AR_TEENS[n - 10])
    else:
        ones, tens = n % 10, n // 10
        sub = []
        if ones:
            sub.append(_AR_ONES[ones])
        if tens >= 2:
            sub.append(_AR_TENS[tens])
        if sub:
            parts.append(' و'.join(sub))
    return ' و'.join(parts)


def number_to_words_ar(n):
    if n == 0:
        return 'صفر'
    groups = []
    scale = 0
    while n > 0:
        n, rem = divmod(n, 1000)
        if rem:
            groups.append((rem, scale))
        scale += 1
    groups.reverse()
    words = []
    for val, scale in groups:
        w = _ar_under_1000(val)
        if scale:
            if val == 1:
                w = _AR_SCALE[scale]
            elif val == 2:
                w = _AR_SCALE[scale] + 'ان'
            else:
                w = w + ' ' + _AR_SCALE[scale]
        words.append(w)
    return ' و'.join(words)


def amount_to_words_ar(amount, currency_name='ريال سعودي', subunit_name='هللة'):
    riyals = int(amount)
    halalas = round((amount - riyals) * 100)
    parts = [number_to_words_ar(riyals), currency_name]
    if halalas:
        parts += ['و', number_to_words_ar(halalas), subunit_name]
    parts.append('فقط')
    return ' '.join(parts)


def to_arabic_digits(value):
    out = []
    for ch in str(value):
        if ch.isdigit():
            out.append(_AR_DIGITS[int(ch)])
        elif ch == ',':
            out.append('٬')
        elif ch == '.':
            out.append('٫')
        else:
            out.append(ch)
    return ''.join(out)


def to_ncr(text):
    """Convert text to HTML Numeric Character References (encoding-agnostic).

    Returns a markupsafe.Markup object so QWeb's ``t-out`` emits the entities
    unescaped. Every non-ASCII character becomes ``&#DECIMAL;`` -- pure ASCII
    that survives wkhtmltopdf's cp1252 mis-detection of the HTML file and is
    then resolved back to the correct Unicode glyph by the HTML parser. ASCII
    HTML-special characters (& < >) are escaped so names like "AT&T" stay safe.
    """
    if not text:
        return Markup('')
    out = []
    for ch in str(text):
        codepoint = ord(ch)
        if codepoint > 127:
            out.append('&#%d;' % codepoint)
        elif ch == '&':
            out.append('&amp;')
        elif ch == '<':
            out.append('&lt;')
        elif ch == '>':
            out.append('&gt;')
        else:
            out.append(ch)
    return Markup(''.join(out))


def _tlv(tag, value):
    value_bytes = value.encode('utf-8')
    return bytes([tag]) + bytes([len(value_bytes)]) + value_bytes


class AccountMove(models.Model):
    _inherit = 'account.move'

    def sol_einvoice_number(self):
        self.ensure_one()
        dt = self.invoice_date or fields.Date.context_today(self)
        return '%02d%02d%02d%06d%03d' % (
            dt.day, dt.month, dt.year % 100,
            int(self.create_date.strftime('%H%M%S')) if self.create_date else 0,
            self.id % 1000,
        )

    def sol_zatca_qr(self):
        self.ensure_one()
        company = self.company_id
        seller_name = company.name or ''
        vat_number = company.vat or ''
        timestamp = (self.invoice_date or fields.Date.context_today(self)).strftime('%Y-%m-%dT%H:%M:%SZ')
        total = '%.2f' % self.amount_total
        vat_amount = '%.2f' % self.amount_tax
        raw = b''.join([
            _tlv(1, seller_name),
            _tlv(2, vat_number),
            _tlv(3, timestamp),
            _tlv(4, total),
            _tlv(5, vat_amount),
        ])
        return base64.b64encode(raw).decode('ascii')

    def sol_zatca_qr_url(self):
        self.ensure_one()
        qr_value = quote(self.sol_zatca_qr(), safe='')
        return '/report/barcode/?type=QR&value=%s&width=120&height=120' % qr_value

    def sol_vat_percent_label(self, line):
        rate = line.tax_ids[0].amount if line.tax_ids else 0
        return '%.0f %%' % rate

    def sol_amount_in_words_en(self):
        self.ensure_one()
        return amount_to_words_en(abs(self.amount_total))

    def sol_amount_in_words_ar(self):
        self.ensure_one()
        return amount_to_words_ar(abs(self.amount_total))

    def sol_vat_in_words_en(self):
        self.ensure_one()
        return amount_to_words_en(abs(self.amount_tax))

    def sol_vat_in_words_ar(self):
        self.ensure_one()
        return amount_to_words_ar(abs(self.amount_tax))

    def sol_ar_num(self, value):
        return to_arabic_digits('{:,.2f}'.format(value or 0))

    def sol_ar_digits(self, value):
        return to_arabic_digits(value or '')

    # Arabic Labels
    def sol_ar_company_name(self):
        """Return company name in Arabic (from field or default)."""
        company = self.company_id
        if company.partner_id and company.partner_id.arabic_name:
            return company.partner_id.arabic_name
        # Fallback: use English name if no Arabic name
        return company.name or ''

    def sol_ar_company_address(self):
        """Return company address in Arabic (from field or default)."""
        company = self.company_id
        if company.partner_id and company.partner_id.arabic_address:
            return company.partner_id.arabic_address
        return ''

    def sol_ar_partner_name(self):
        """Return partner name in Arabic (from field or default)."""
        partner = self.partner_id
        if partner.arabic_name:
            return partner.arabic_name
        return partner.name or ''

    def sol_ar_label(self, key):
        """Return Arabic label for common invoice terms."""
        labels = {
            'buyer': 'المشتري',
            'invoice_title': 'فاتورة ضريبية',
            'items': 'البنود',
            'no': 'ر.م',
            'description': 'الوصف',
            'vat': 'ضريبة',
            'amount': 'القيمة',
            'summary': 'الملخص',
            'bank_details': 'تفاصيل البنك',
            'signature': 'ختم العميل وتوقيعه',
            'authorized': 'المفوض بالتوقيع',
        }
        return labels.get(key, '')

    def sol_format_amount(self, value):
        """Format amount with thousand separators."""
        return '{:,.2f}'.format(value or 0)

    def sol_ar_label_ncr(self, key):
        """Return Arabic label in HTML NCR format (encoding-agnostic).

        This version uses Numeric Character References to bypass
        wkhtmltopdf's UTF-8 mis-detection bug. Use this when standard
        sol_ar_label() renders as mojibake in the PDF.
        """
        label = self.sol_ar_label(key)
        return to_ncr(label)

    def sol_ar_company_name_ncr(self):
        """Return company Arabic name in NCR format."""
        return to_ncr(self.sol_ar_company_name())

    def sol_ar_company_address_ncr(self):
        """Return company Arabic address in NCR format."""
        return to_ncr(self.sol_ar_company_address())

    def sol_ar_partner_name_ncr(self):
        """Return partner Arabic name in NCR format."""
        return to_ncr(self.sol_ar_partner_name())

    def sol_amount_in_words_ar_ncr(self):
        """Return Arabic amount-in-words in NCR format."""
        return to_ncr(self.sol_amount_in_words_ar())

    def sol_ar_vat_line_ncr(self):
        """Return the company's VAT number line ('ضريبة: <arabic digits>') in NCR."""
        label = self.sol_ar_label('vat')
        digits = to_arabic_digits(self.company_id.vat or '')
        return to_ncr('%s: %s' % (label, digits))

    def sol_ar_country(self, country):
        """Return an Arabic country name (mapped for common cases, else the name)."""
        if not country:
            return ''
        mapping = {
            'SA': 'السعودية',
            'AE': 'الإمارات العربية المتحدة',
            'KW': 'الكويت',
            'BH': 'البحرين',
            'QA': 'قطر',
            'OM': 'عُمان',
            'EG': 'مصر',
            'JO': 'الأردن',
        }
        return mapping.get(country.code or '', country.name or '')

    def sol_ar_partner_country(self):
        """Arabic name of the customer's country."""
        return self.sol_ar_country(self.partner_id.country_id)

    def sol_vat_rate_label(self):
        """Effective VAT rate for the invoice as a label, e.g. '15%'."""
        if self.amount_untaxed:
            return '%g%%' % round(self.amount_tax / self.amount_untaxed * 100.0, 2)
        return '0%'


