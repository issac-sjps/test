from django.db import models
from django.contrib.auth.models import User # 引入 Django 內建的使用者系統

class Subsidy(models.Model):
    # 定義欄位
    student_name = models.CharField(max_length=100, verbose_name="學生姓名")
    reason = models.TextField(verbose_name="申請事由")
    amount = models.IntegerField(verbose_name="金額")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登記時間")
    
    # 記錄是誰登記的（關聯到使用者）
    recorder = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="登記人")

    def __str__(self):
        return f"{self.student_name} - {self.amount}"