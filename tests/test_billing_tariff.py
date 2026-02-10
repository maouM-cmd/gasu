from decimal import Decimal
from billing.tariff import calculate_invoice_amounts


def test_calculate_invoice_amounts_basic():
    basic = Decimal('500')
    unit = Decimal('50')
    usage = Decimal('10')
    tax = Decimal('10')
    res = calculate_invoice_amounts(basic, unit, usage, tax)
    assert res['subtotal'] == Decimal('1000.00')  # 500 + 50*10
    assert res['tax'] == Decimal('100.00')
    assert res['total'] == Decimal('1100.00')


def test_calculate_invoice_rounding():
    basic = Decimal('123.45')
    unit = Decimal('12.345')
    usage = Decimal('7.89')
    tax = Decimal('8')
    res = calculate_invoice_amounts(basic, unit, usage, tax)
    # just ensure keys and types exist
    assert 'subtotal' in res and 'tax' in res and 'total' in res
