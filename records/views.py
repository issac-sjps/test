from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from .models import Subsidy
import csv
from django.http import HttpResponse
from django.contrib import messages

@login_required
def index(request):
    # 如果使用者按下「送出」按鈕
    if request.method == "POST":
        # 這裡縮進 8 個空格
        student_name = request.POST.get('student_name')
        amount = request.POST.get('amount')
        
        if student_name and amount:
            Subsidy.objects.create(
                student_name=student_name,
                amount=amount,
                recorder=request.user
            )
            # 儲存後立即跳轉，這行必須縮進 12 個空格（在 if 裡面）
            return redirect('index')

    query = request.GET.get('q')
    if request.user.is_superuser:
        items = Subsidy.objects.all().order_by('-created_at') # 建議加個排序，新的在前
    else:
        items = Subsidy.objects.filter(recorder=request.user).order_by('-created_at')
    # 取得所有資料顯示在表格
    items = Subsidy.objects.all()
    
    # 權限過濾邏輯
    if request.user.is_superuser:
        # 如果是管理員，取得所有資料
        items = Subsidy.objects.all()
    else:
        # 如果是一般老師，只取得「recorder 是自己」的資料
        items = Subsidy.objects.filter(recorder=request.user)
    
    return render(request, 'index.html', {'items': items})
    
@login_required
@permission_required('records.delete_subsidy', raise_exception=True) # 雙重保險：沒權限的人禁止執行
def delete_item(request, item_id):
    item = get_object_or_404(Subsidy, id=item_id)
    item.delete()
    return redirect('index')
    
def index(request):
    # 獲取搜尋關鍵字
    query = request.GET.get('q') 
    
    if request.user.is_superuser:
        items = Subsidy.objects.all()
    else:
        items = Subsidy.objects.filter(recorder=request.user)

    # 如果有輸入關鍵字，就過濾姓名
    if query:
        items = items.filter(student_name__icontains=query)

    return render(request, 'index.html', {'items': items, 'query': query})
    
@login_required
def export_csv(request):
    # 建立回應物件，告訴瀏覽器這是一個 CSV 檔
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subsidy_report.csv"'
    
    # 處理中文亂碼問題 (BOM)
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response)
    writer.writerow(['學生姓名', '金額', '登記人', '時間']) # 標題列

    # 只匯出該使用者看得到的資料
    items = Subsidy.objects.all() if request.user.is_superuser else Subsidy.objects.filter(recorder=request.user)

    for item in items:
        writer.writerow([item.student_name, item.amount, item.recorder.username, item.created_at])

    return response