from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from nippou_app.models import nippou_data
from nippou_app.models import Task, User
from django import forms
from django.db.models import Q

# Create your views here.
# URLディスパッチャからこのメソッド名を指定して呼ばれる
# nippou_app\urls.py内でviews.メソッド名の形で呼ばれる
# ここでDBからもらった情報をテンプレに流し込む


class editform(ModelForm):
    class Meta:
        model = nippou_data
        #fields = ('title', 'text', 'date')
        fields = ('title', 'date')

class taskform(ModelForm):
    class Meta:
        model = Task
        fields = ('task_name', 'time_yotei', 'time_jitsu', 'task_y', 'task_w', 'task_t')

@login_required(login_url='/accounts/login')
def edit(request, id=None):

    # edit
    if id:
        data = get_object_or_404(nippou_data, pk=id)
        # user check
        if data.user != request.user:
            return redirect('nippou_app:show')
    # new
    else:
        data = nippou_data()

    task_data = Task()

    # edit
    if request.method == 'POST':
        form = editform(request.POST, instance=data)

        # 完了がおされたら
        if form.is_valid():
            nippou = form.save(commit=False)
            nippou.user = request.user
            nippou.save()
            return redirect('nippou_app:show')
        pass
    # new
    else:
        form = editform(instance=data)

    return render_to_response('nippou_app/nippou_edit.html',
                              {'form': form, 'id': id},
                              context_instance=RequestContext(request))

@login_required(login_url='/accounts/login')
def delete(request, id=None):

    nippou = get_object_or_404(nippou_data, pk=id)
    nippou.delete()
    #ここで確認を入れたい
    return redirect('nippou_app:show')

@login_required(login_url='/accounts/login')
def show(request):

    uname = request.user.username
    nippous = nippou_data.objects.all().order_by('date')[:] # show the last N posts

    return render_to_response('nippou_app/nippou_show.html',
                              {'nippous': nippous, 'uname': uname}, context_instance=RequestContext(request))

def profile(request):
    #nippous = nippou_data.objects.all()
    #return render_to_response('nippou_app/nippou_show.html',
    #                          {'nippous': nippous}, context_instance=RequestContext(request))
    return HttpResponse('プロフィール')

"""
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            print("ユーザがアクティブじゃありません")
            # Return a 'disabled account' error message
    else:
        print("ログインエラー（ユーザ名orパスが間違っています）")
        # Return an 'invalid login' error message.
"""


"""
def login(request):
    return HttpResponse('ログインページ')
"""

@login_required(login_url='/accounts/login')
def detail(request, id):
    try:
        nippou = nippou_data.objects.get(pk=id)
    except nippou_data.DoesNotExist:
        raise Http404

    task_all = Task.objects.all()
    tasks = []
    for task in task_all:
        if task.nippou.id == nippou.id:
            tasks.append(task)
        else:
            pass

    # user check
    hide_edit = 0
    if nippou.user != request.user:
        print("you can not edit!")
        hide_edit = 1

    return render_to_response('nippou_app/nippou_detail.html',
                              {'nippou': nippou, 'tasks':tasks, 'hide_edit':hide_edit}, context_instance=RequestContext(request))

class NippouSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, label='キーワード')

@login_required(login_url='/accounts/login')
def search(request):
   form, nippou_ = None, []
   if request.method == 'GET':
       form = NippouSearchForm()

   elif request.method == 'POST':
      form = NippouSearchForm(request.POST)
      nippous = nippou_data.objects.all()
      if form.is_valid():
          nippou_ = nippous.filter(Q(title__contains=form.clean()['keyword']))

   return render_to_response('nippou_app/nippou_search.html', {'form':form, 'nippous':nippou_}, RequestContext(request))

@login_required(login_url='/accounts/login')
def taskadd(request, id=None):

    if id:
        nippou = get_object_or_404(nippou_data, pk=id)
        # user check
        if nippou.user != request.user:
            return redirect('nippou_app:show')
    # new
    else:
        nippou = nippou_data()#ここにあってよい?

    task_data = Task()

    # edit
    if request.method == 'POST':
        form = taskform(request.POST, instance=task_data)

        # 完了がおされたら
        if form.is_valid():
            task_data.nippou = nippou
            task = form.save(commit=False)
            task.save()
            return redirect('nippou_app:show')
        pass
    # new
    else:
        form = taskform(instance=task_data)

    return render_to_response('nippou_app/nippou_taskadd.html', {'task_form':form}, RequestContext(request))
