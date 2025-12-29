import os
import django

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings') # 如果你的資料夾不叫 myproject 請改掉
django.setup()

from django.contrib.auth.models import User

# 設定你想要的帳號與密碼
username = 'admin'
email = 'admin@example.com'
password = 'yourpassword123' # ⬅️ 這裡可以改成你自己想設的密碼

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'超級管理員 {username} 建立成功！')
else:
    print(f'超級管理員 {username} 已經存在，跳過建立步驟。')