from django.contrib import admin
from .models import Subsidy

@admin.register(Subsidy)
class SubsidyAdmin(admin.ModelAdmin):
    # 設定後台列表要顯示哪些欄位
    list_display = ('student_name', 'amount', 'recorder', 'created_at')
    # 設定哪些欄位可以搜尋
    search_fields = ('student_name',)