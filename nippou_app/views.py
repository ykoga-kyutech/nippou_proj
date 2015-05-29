from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from nippou_app.models import nippou_data
from nippou_app.models import Task, User
from django import forms
from django.db.models import Q

# Create your views here.
class NippouEditForm(ModelForm):
    class Meta:
        model = nippou_data
        fields = ('title', 'date', 'text', 'open')
        widgets = {
          'title': forms.TextInput(attrs={'size': '100'}),
          'text': forms.Textarea(attrs={'rows':20, 'cols':100}),
        }

class TaskEditForm(ModelForm):

    class Meta:
        model = Task
        fields = ('task_name', 'time_yotei', 'time_jitsu', 'task_y', 'task_w', 'task_t')
        widgets = {
          'task_name': forms.TextInput(attrs={'size': '100'}),
          'task_y': forms.Textarea(attrs={'rows':10, 'cols':100}),
          'task_w': forms.Textarea(attrs={'rows':10, 'cols':100}),
          'task_t': forms.Textarea(attrs={'rows':10, 'cols':100}),
        }


class NippouSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, label='キーワード')

@login_required(login_url='/accounts/login')
def edit(request, id=None):
    """
    日報を新規作成、または指定された日報を編集する
    """
    # edit
    if id:
        data = get_object_or_404(nippou_data, pk=id)
        # user check
        if data.user != request.user:
            print("不正なアクセスです！")
            return redirect('nippou_app:show')
    # new
    else:
        data = nippou_data()

    task_data = Task()

    # edit
    if request.method == 'POST':
        form = NippouEditForm(request.POST, instance=data)

        # 完了がおされたら
        if form.is_valid():
            nippou = form.save(commit=False)
            nippou.user = request.user
            nippou.open = form.cleaned_data['open']
            nippou.save()
            return redirect('nippou_app:mypage')
        pass
    # new
    else:
        form = NippouEditForm(instance=data)

    return render_to_response('nippou_app/nippou_edit.html',
                              {'form': form, 'id': id},
                              context_instance=RequestContext(request))

@login_required(login_url='/accounts/login')
def delete(request, id=None):
    """
    指定された日報を削除する
    """
    nippou = get_object_or_404(nippou_data, pk=id)

    # user check
    if nippou.user == request.user:
        #ここで確認を入れたい
        nippou.delete()
    else:
        print("不正なアクセスです！")
        return redirect('nippou_app:show')

    return redirect('nippou_app:mypage')

@login_required(login_url='/accounts/login')
def show(request):

    """
    日報一覧を表示する
    """

    #公開にチェックがはいっているもののみ最新のものから順に表示
    nippous_tmp = nippou_data.objects.all().order_by('-date')[:]
    nippous = list(filter(lambda x: x.open==True, nippous_tmp))

    return render_to_response('nippou_app/nippou_show.html',
                              {'nippous': nippous, 'uname': request.user.last_name+request.user.first_name},
                              context_instance=RequestContext(request))

@login_required(login_url='/accounts/login')
def mypage(request):

    """
    マイページを表示する
    """

    #uname = request.user.username
    nippous_tmp = nippou_data.objects.all().order_by('-date')[:]

    nippous = []
    for nippou in nippous_tmp:
        # user check
        if nippou.user == request.user:
            nippous.append(nippou)
    nippou = nippous[0]

    task_all = Task.objects.all()

    tasks = []
    for task in task_all:
        if task.nippou.id == nippou.id:
            tasks.append(task)

    return render_to_response('nippou_app/mypage.html',
                              {'nippous': nippous, 'tasks': tasks, 'uname': request.user.last_name+request.user.first_name},
                              context_instance=RequestContext(request))

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

    """
    選択された日報の詳細を表示する
    """

    nippou = get_object_or_404(nippou_data, pk=id)

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
        # 他人の日報は編集削除できないようにする
        hide_edit = 1

    return render_to_response('nippou_app/nippou_detail.html',
                              {'nippou': nippou, 'tasks':tasks, 'hide_edit':hide_edit}, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login')
def search(request):

   """
   一覧から日報を検索する
　 """

   form, nippou_ = None, []
   if request.method == 'GET':
       form = NippouSearchForm()

   elif request.method == 'POST':
      form = NippouSearchForm(request.POST)
      nippous = nippou_data.objects.all()
      if form.is_valid():
          nippou_ = list(nippous.filter(Q(title__contains=form.clean()['keyword']))) #title
          nippou_.extend(nippous.filter(Q(text__contains=form.clean()['keyword']))) #text
          #nippou_.extend(nippous.filter(Q(user__contains=form.clean()['keyword']))) #user # error

   return render_to_response('nippou_app/nippou_search.html', {'form':form, 'nippous':nippou_}, RequestContext(request))

@login_required(login_url='/accounts/login')
def taskadd(request, id=None):

    """
   指定された日報にタスクを追加する
　 """

    if id:
        nippou = get_object_or_404(nippou_data, pk=id)
        # user check
        if nippou.user != request.user:
            print("不正なアクセスです！")
            return redirect('nippou_app:show')
    # new
    else:
        nippou = nippou_data()#ここにあってよい?

    task = Task()

    # edit
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)

        # 完了がおされたら
        if form.is_valid():
            task.nippou = nippou
            task = form.save(commit=False)
            task.save()
            return redirect('nippou_app:mypage')
        pass
    # new
    else:
        form = TaskEditForm(instance=task)

    return render_to_response('nippou_app/nippou_taskadd.html', {'task_form':form}, RequestContext(request))

@login_required(login_url='/accounts/login')
def taskedit(request, id=None):

    """
   タスクを新規作成、または指定されたタスクを編集する
　 """

    # edit
    if id:
        task = get_object_or_404(Task, pk=id)
        # user check
        if task.nippou.user != request.user:
            print("不正なアクセスです！")
            return redirect('nippou_app:show')
    # new
    else:
        task = Task()

    # edit
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)

        # 完了がおされたら
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('nippou_app:mypage')
        pass
    # new
    else:
        form = TaskEditForm(instance=task)
    return render_to_response('nippou_app/nippou_taskedit.html',
                              {'form': form, 'id': id},
                              context_instance=RequestContext(request))

@login_required(login_url='/accounts/login')
def taskdelete(request, id=None):

    """
   指定されたタスクを削除する
　 """
    if id:
        task = get_object_or_404(Task, pk=id)
        # user check
        if task.nippou.user == request.user:
            #ここで確認を入れたい
            task.delete()
        else:
            print("不正なアクセスです！")
            return redirect('nippou_app:show')

    return redirect('nippou_app:mypage')

@login_required(login_url='/accounts/login')
def make(request, id=None):

    """
    日報をタスクから自動生成する
　  """

    if id:
        nippou = get_object_or_404(nippou_data, pk=id)
        # user check
        if nippou.user != request.user:
            print("不正なアクセスです！")
            return redirect('nippou_app:show')
    # new
    else:
        nippou = nippou_data()#ここにあってよい?

    task_all = Task.objects.all()
    tasks = []
    for task in task_all:
        if task.nippou.id == nippou.id:
            tasks.append(task)
        else:
            pass

    nippou_text = nippou.text

    nippou_text += "\n#### 以下、自動作成結果 ####\n"

    nippou_text += "\n・計画\n"
    for task in tasks:
        nippou_text += task.task_name+"\n"

    nippou_text += "\n・やったこと\n"
    for task in tasks:
        nippou_text += task.task_y+"\n"

    nippou_text += "\n・わかったこと\n"
    for task in tasks:
        nippou_text += task.task_w+"\n"

    nippou_text += "\n・次やること\n"
    for task in tasks:
        nippou_text += task.task_t+"\n"

    nippou_text += "\n・所感\n"

    # edit
    if request.method == 'POST':
        form = NippouEditForm(request.POST, instance=nippou)

        # 完了がおされたら
        if form.is_valid():
            nippou = form.save(commit=False)
            nippou.save()
            return redirect('nippou_app:mypage')
        pass
    # new
    else:
        nippou.text = nippou_text
        form = NippouEditForm(instance=nippou)
        print("get")

    return render_to_response('nippou_app/nippou_edit.html',
                              {'form': form, 'id': id},
                              context_instance=RequestContext(request))
