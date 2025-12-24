from decimal import Decimal
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import Order
from api.services import OrderService
from api.exceptions import OrderAlreadyExistsError


class OrderModelTestCase(TestCase):
    """測試 Order Model"""
    
    def test_create_order_success(self):
        """測試成功建立訂單"""
        order = Order.objects.create(
            order_number="TEST001",
            total_price=Decimal("100.50")
        )
        self.assertEqual(order.order_number, "TEST001")
        self.assertEqual(order.total_price, Decimal("100.50"))
        self.assertIsNotNone(order.created_time)
        self.assertIsNotNone(order.updated_time)
        self.assertIsNone(order.deleted_time)
    
    def test_order_number_unique_constraint(self):
        """測試 order_number 唯一性約束"""
        Order.objects.create(order_number="TEST002", total_price=100)
        
        with self.assertRaises(Exception):  # IntegrityError
            Order.objects.create(order_number="TEST002", total_price=200)


class OrderServiceTestCase(TestCase):
    """測試 OrderService"""
    
    def test_create_order_success(self):
        """測試成功建立訂單"""
        order = OrderService.create_order("SVC001", Decimal("250.75"))
        
        self.assertEqual(order.order_number, "SVC001")
        self.assertEqual(order.total_price, Decimal("250.75"))
        self.assertIsNotNone(order.id)
    
    def test_create_order_duplicate_raises_exception(self):
        """測試重複訂單號拋出異常"""
        OrderService.create_order("SVC002", Decimal("100"))
        
        with self.assertRaises(OrderAlreadyExistsError) as cm:
            OrderService.create_order("SVC002", Decimal("200"))
        
        self.assertIn("SVC002", str(cm.exception))


@override_settings(API_TOKEN="test_token_12345")
class ImportOrderAPITestCase(APITestCase):
    """測試 import_order API"""
    
    def setUp(self):
        """每個測試前執行"""
        self.url = "/api/import-order/"
        self.valid_token = "test_token_12345"
        self.invalid_token = "wrong_token"
    
    def test_import_order_success(self):
        """測試成功匯入訂單"""
        data = {
            "order_number": "API001",
            "total_price": "500.00"
        }
        response = self.client.post(
            self.url, 
            data, 
            HTTP_X_API_KEY=self.valid_token,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['order_number'], "API001")
        
        # 確認資料庫有此筆資料
        self.assertTrue(Order.objects.filter(order_number="API001").exists())
    
    def test_import_order_duplicate_returns_400(self):
        """測試重複訂單號回傳 400"""
        data = {"order_number": "API002", "total_price": "100.00"}
        
        # 第一次成功
        response1 = self.client.post(
            self.url, 
            data, 
            HTTP_X_API_KEY=self.valid_token,
            format='json'
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # 第二次失敗
        response2 = self.client.post(
            self.url, 
            data, 
            HTTP_X_API_KEY=self.valid_token,
            format='json'
        )
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response2.data)
    
    def test_import_order_invalid_token_returns_401(self):
        """測試錯誤 Token 回傳 401"""
        data = {"order_number": "API003", "total_price": "100.00"}
        response = self.client.post(
            self.url, 
            data, 
            HTTP_X_API_KEY=self.invalid_token,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_import_order_missing_required_fields_returns_400(self):
        """測試缺少必填欄位回傳 400"""
        data = {"total_price": "100.00"}  # 缺少 order_number
        response = self.client.post(
            self.url, 
            data, 
            HTTP_X_API_KEY=self.valid_token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_import_order_invalid_total_price_returns_400(self):
        """測試無效金額回傳 400"""
        data = {"order_number": "API004", "total_price": "-100.00"}  # 負數
        response = self.client.post(
            self.url, 
            data, 
            HTTP_X_API_KEY=self.valid_token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
