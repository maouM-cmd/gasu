from decimal import Decimal
from django.db import transaction
from .models import Customer, MeterReading, Invoice
from .tariff import calculate_invoice_amounts


def generate_invoices_for_all():
    """全顧客の最新検針を見て、前回検針があれば請求を生成する。
    ルール:
    - 各顧客について最新の検針(current)と直近前(previous)を取得
    - previousが存在し、まだ current.date をキーにした請求が無ければ請求を作成
    - 請求の `amount` は税込合計を保存する
    戻り値: 作成したInvoiceオブジェクトのリスト
    """
    created = []
    customers = Customer.objects.all()
    for c in customers:
        readings = list(MeterReading.objects.filter(customer=c).order_by('date'))
        if len(readings) < 2:
            continue
        prev = readings[-2]
        curr = readings[-1]
        # すでに当該検針日で請求があるか確認
        exists = Invoice.objects.filter(customer=c, date=curr.date).exists()
        if exists:
            continue
        usage = (Decimal(curr.value) - Decimal(prev.value))
        if usage < 0:
            usage = Decimal('0')
        amounts = calculate_invoice_amounts(
            Decimal(c.plan_basic_fee), Decimal(c.plan_unit_price), usage, Decimal(c.tax_rate)
        )
        with transaction.atomic():
            inv = Invoice.objects.create(
                customer=c,
                date=curr.date,
                amount=amounts['total'],
                paid=False,
            )
            created.append(inv)
    return created
