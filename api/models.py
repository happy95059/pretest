from django.db import models


# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True, help_text="訂單編號")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="總價")
    created_time = models.DateTimeField(auto_now_add=True, help_text="建立時間")
    updated_time = models.DateTimeField(auto_now=True, help_text="最後更新時間")
    deleted_time = models.DateTimeField(null=True, blank=True, help_text="刪除時間 (軟刪除)")
    
    class Meta:
        ordering = ['-created_time']  # 預設按建立時間降序排列
        db_table = 'api_order'
        indexes = [
            models.Index(fields=['deleted_time']),   # 軟刪除查詢優化
            models.Index(fields=['-created_time']),  # 時間排序優化
        ]
    
    def __str__(self):
        return f"Order {self.order_number} - ${self.total_price}"

