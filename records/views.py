from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Subsidy
import csv
from django.http import HttpResponse
from django.contrib import messages

@login_required
def index(request):
    # 處理「新增資料」邏輯
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        amount = request.POST.get('amount')
        
        if student_name and amount:
            Subsidy.objects.create(
                student_name=student_name,
                amount=amount,
                recorder=request.user
            )
            return redirect('index') # 儲存完畢立刻跳轉

    # 處理「顯示與搜尋」邏輯
    query = request.GET.get('q')
    
    # 權限過濾：管理員看全部，老師看自己
    if request.user.is_superuser:
        items = Subsidy.objects.all().order_by('-created_at')
    else:
        items = Subsidy.objects.filter(recorder=request.user).order_by('-created_at')

    # 如果有搜尋關鍵字，再進一步過濾姓名
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