from decimal import Decimal, ROUND_HALF_UP


def calculate_invoice_amounts(basic_fee: Decimal, unit_price: Decimal, usage: Decimal, tax_rate_percent: Decimal):
    """料金計算: 税抜小計、税額、税込合計を返す。税率はパーセント（例: 10.0）で渡す。"""
    subtotal = (basic_fee + (unit_price * usage)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    tax = (subtotal * (tax_rate_percent / Decimal('100'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total = (subtotal + tax).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return {
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
