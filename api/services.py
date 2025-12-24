from api.models import Order
from api.exceptions import OrderAlreadyExistsError
from typing import Dict, Any
from decimal import Decimal


class OrderService:

    @staticmethod
    def create_order(order_number: str, total_price: Decimal) -> Order:

        # 1. 檢查訂單編號是否已存在
        if Order.objects.filter(order_number=order_number).exists():
            # 使用自定義 Exception,讓錯誤更明確
            raise OrderAlreadyExistsError(f'Order with number {order_number} already exists')
        
        # 2. 建立訂單
        order = Order.objects.create(
            order_number=order_number,
            total_price=total_price
        )
        
        # 3. 這裡可以加其他業務邏輯:
        # - 發送通知
        # - 記錄日誌
        # - 呼叫外部 API
        # - 計算匯率
        # - 等等...
        
        return order
