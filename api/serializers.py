from rest_framework import serializers
from api.models import Order


class ImportOrderRequestSerializer(serializers.Serializer):
    order_number = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False,
        help_text="訂單編號",
        error_messages={
            'required': 'order_number is required',
            'blank': 'order_number cannot be blank',
            'max_length': 'order_number cannot exceed 100 characters'
        }
    )
    
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        min_value=0,
        help_text="總價",
        error_messages={
            'required': 'total_price is required',
            'invalid': 'total_price must be a valid number',
            'min_value': 'total_price must be positive'
        }
    )
    
    # 移除 validate_order_number() 驗證
    # 理由: 
    # 1. Service 層已經有驗證,避免重複查詢 DB
    # 2. DB 有 unique 約束作為最後防線
    # 3. Serializer 只負責「格式驗證」,不負責「業務邏輯驗證」


class OrderImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'total_price', 'created_time', 'updated_time', 'deleted_time']
        read_only_fields = ['id', 'created_time', 'updated_time', 'deleted_time']


class ImportOrderResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = OrderImportSerializer()
