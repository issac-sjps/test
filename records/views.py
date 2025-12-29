from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Subsidy
import csv
from django.http import HttpResponse
from django.contrib import messages

def index(request):
    # 1. 處理「新增資料」 (只有登入者才能進來這區塊)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('/admin/login/') # 沒登入的人想 POST，送去登入
            
        student_name = request.POST.get('student_name')
        amount = request.POST.get('amount')
        if student_name and amount:
            Subsidy.objects.create(
                student_name=student_name,
                amount=amount,
                recorder=request.user
            )
            return redirect('index')

    # 2. 處理「搜尋與過濾」
    query = request.GET.get('q')
    
    # --- 關鍵修正：判斷登入狀態 ---
    if request.user.is_authenticated:
        if request.user.is_superuser:
            items = Subsidy.objects.all().order_by('-created_at')
        else:
            items = Subsidy.objects.filter(recorder=request.user).order_by('-created_at')
    else:
        # 沒登入的人，我們讓他看「所有資料」或是「空的」？
        # 建議讓他們看所有資料(唯讀)，否則畫面會是空的
        items = Subsidy.objects.all().order_by('-created_at')

    if query:
        items = items.filter(student_name__icontains=query)

    return render(request, 'index.html', {
        'items': items, 
        'query': query
    })
    
    
@login_required
@permission_required('records.delete_subsidy', raise_exception=True)
def delete_item(request, item_id):
    item = get_object_or_404(Subsidy, id=item_id)
    item.delete()
    return redirect('index')

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subsidy_report.csv"'
    response.write(u'\ufeff'.encode('utf8')) # 解決中文亂碼
    
    writer = csv.writer(response)
    writer.writerow(['學生姓名', '金額', '登記人', '時間'])

    if request.user.is_superuser:
        items = Subsidy.objects.all()
    else:
        items = Subsidy.objects.filter(recorder=request.user)

    for item in items:
        writer.writerow([item.student_name, item.amount, item.recorder.username, item.created_at])

    return response