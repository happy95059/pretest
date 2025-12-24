from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from api.models import Order
from api.authentication import APIKeyAuthentication
from api.serializers import ImportOrderRequestSerializer, ImportOrderResponseSerializer
from api.services import OrderService
from api.exceptions import OrderAlreadyExistsError
import logging

logger = logging.getLogger(__name__)

# Create your views here.


@api_view(['POST'])
@authentication_classes([APIKeyAuthentication])
def import_order(request):
    """
    匯入訂單 API
    
    架構:
    View (Controller) → Service (業務邏輯) → Model (資料)
    """
    # 1. Request 驗證 (Serializer 只負責驗證格式)
    serializer = ImportOrderRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    # 2. 呼叫 Service 處理業務邏輯
    try:
        order = OrderService.create_order(
            order_number=serializer.validated_data['order_number'],
            total_price=serializer.validated_data['total_price']
        )
    except OrderAlreadyExistsError as e:
        # 業務邏輯錯誤: 訂單已存在 - 400
        logger.warning(f"Order creation failed: {str(e)}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # 其他未預期的錯誤 (例如: DB 連線失敗、外部 API 錯誤) - 500
        logger.error(f"Failed to create order: {str(e)}", exc_info=True)
        
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # 3. Response 序列化
    response_serializer = ImportOrderResponseSerializer({
        'success': True,
        'message': 'Order created successfully',
        'data': order
    })
    
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)