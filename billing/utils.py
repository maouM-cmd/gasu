from decimal import Decimal
from django.db import transaction
from django.db.models import Max
from .models import Customer, MeterReading, Invoice, AuditLog
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
        # 同日の複数検針がある場合は最新(idの最大)を採用する
        qs = MeterReading.objects.filter(customer=c)
        if qs.count() < 2:
            continue
        # 各日付ごとに最新のidを取得
        per_day = qs.values('date').annotate(max_id=Max('id')).order_by('date')
        # 実際の最新検針レコードを日付順で取得
        readings = [MeterReading.objects.get(pk=item['max_id']) for item in per_day]
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
            # メーター逆転や入力ミスの可能性: ログを残してスキップ
            try:
                AuditLog.objects.create(
                    actor='system',
                    action_type='skip_negative_usage',
                    target_table='MeterReading',
                    target_id=curr.id,
                    payload=f'curr={curr.value}, prev={prev.value}'
                )
            except Exception:
                pass
            continue
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
            # 記録を残す
            try:
                AuditLog.objects.create(
                    actor='system',
                    action_type='generate_invoice',
                    target_table='Invoice',
                    target_id=inv.id,
                    payload=f'usage={usage}, subtotal={amounts["subtotal"]}, tax={amounts["tax"]}, total={amounts["total"]}'
                )
            except Exception:
                pass
    return created
