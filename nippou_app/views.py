from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from nippou_app.models import nippou_data

# Create your views here.
# URLディスパッチャからこのメソッド名を指定して呼ばれる
# nippou_app\urls.py内でviews.メソッド名の形で呼ばれる
# ここでDBからもらった情報をテンプレに流し込む


class editform(ModelForm):
    class Meta:
        model = nippou_data
        fields = ('title', 'text', 'date')

def edit(request, id=None):

    # edit
    if id:
        data = get_object_or_404(nippou_data, pk=id)
    # new
    else:
        data = nippou_data()

    #form = None
    if request.method == 'POST':
        form = editform(request.POST, instance=data)
        if form.is_valid():
            nippou = form.save(commit=False)
            nippou.save()
            return redirect('nippou_app:show')
        pass
    else:
        form = editform(instance=data)

    return render_to_response('nippou_app/nippou_edit.html',
                              {'form': form, 'id': id},
                              context_instance=RequestContext(request))

    #return HttpResponse('編集')


def delete(request, id=None):

    nippou = get_object_or_404(nippou_data, pk=id)
    nippou.delete()
    #ここで確認を入れる
    return redirect('nippou_app:show')

    #return HttpResponse('削除')

#@login_required
def show(request):
    nippous = nippou_data.objects.all().order_by('date')[:] # show the last N posts
    return render_to_response('nippou_app/nippou_show.html',
                              {'nippous': nippous}, context_instance=RequestContext(request))
    #return HttpResponse('読む')

def show2(request):
    user = authenticate(username='john', password='secret')
    if user is not None:
        if user.is_active:
            print("You provided a correct username and password!")
        else:
            print("Your account has been disabled!")
    else:
        print("Your username and password were incorrect.")
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            pass # Return a 'disabled account' error message
    else:
        pass
        # Return an 'invalid login' error message.

def profile(request):
    #nippous = nippou_data.objects.all()
    #return render_to_response('nippou_app/nippou_show.html',
    #                          {'nippous': nippous}, context_instance=RequestContext(request))
    return HttpResponse('プロフィール')


"""
def login(request):
    return HttpResponse('ログインページ')
"""

def detail(request, id):
    try:
        nippou = nippou_data.objects.get(pk=id)
    except nippou_data.DoesNotExist:
        raise Http404
    return render_to_response('nippou_app/nippou_detail.html',
                              {'nippou': nippou}, context_instance=RequestContext(request))
    #return HttpResponse('詳細')