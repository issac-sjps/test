from django.contrib import admin
from django.urls import path, include  # ⬅️ 確保這行有 path 和 include
from records import views              # ⬅️ 確保這行有引入你寫的視圖

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'), 
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('export/', views.export_csv, name='export_csv'),
]