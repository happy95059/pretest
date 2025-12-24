from django.contrib import admin
from api.models import Order

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """訂單管理後台"""
    
    # 列表頁顯示的欄位
    list_display = ('id', 'order_number', 'total_price', 'created_time', 'updated_time', 'deleted_time')
    
    # 可搜尋的欄位
    search_fields = ('order_number',)
    
    # 右側篩選器
    list_filter = ('created_time', 'deleted_time')
    
    # 唯讀欄位 (自動生成的時間戳不應手動修改)
    readonly_fields = ('created_time', 'updated_time', 'deleted_time')
    
    # 排序 (預設按建立時間降序)
    ordering = ('-created_time',)
