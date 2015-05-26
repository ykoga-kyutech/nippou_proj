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
        fields = ('task_name', 'time_yotei')
        #, 'time_jitsu', 'task_y', 'task_w', 'task_t'


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
        #ftask = taskform(request.POST, instance=task_data)

        # 完了がおされたら
        if form.is_valid():
            nippou = form.save(commit=False)
            tmp_task = Task(
            task_name="test_task",
            time_yotei = 0,
            time_jitsu = 0,
            task_y = "y",
            task_w = "w",
            task_t = "t")
            tmp_task.save()

            nippou.task = tmp_task
            nippou.user = request.user
            nippou.save()
            """
            if ftask.is_valid():
                task = ftask.save(commit=False)
                # とりあえずの値
                task.time_jitsu = 0
                task.task_y = "y"
                task.task_w = "w"
                task.task_t = "t"
                task.save()
          """
            return redirect('nippou_app:show')

        # タスク追加がおされたら
        """
        if ftask.is_valid():
            #form =
            task = ftask.save(commit=False)
            # とりあえずの値
            task.time_jitsu = 0
            task.task_y = "y"
            task.task_w = "w"
            task.task_t = "t"
            task.save()
            return render_to_response('nippou_app/nippou_edit.html',
                              {'form': form, 'form_task': ftask, 'id': id},
                              context_instance=RequestContext(request))
            #return redirect('nippou_app:new')
            #return redirect('nippou_app:edit')
        """
        pass
    # new
    else:
        form = editform(instance=data)
        #ftask = taskform(instance=task_data)

    #return render_to_response('nippou_app/nippou_edit.html',
    #                          {'form': form, 'form_task': ftask, 'id': id},
    #                          context_instance=RequestContext(request))
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

    # user check
    hide_edit = 0
    if nippou.user != request.user:
        print("you can not edit!")
        hide_edit = 1

    return render_to_response('nippou_app/nippou_detail.html',
                              {'nippou': nippou, 'hide_edit':hide_edit}, context_instance=RequestContext(request))

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