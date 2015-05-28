from django.test import TestCase
from nippou_app.models import Task, nippou_data, User


"""""""""""""""""""""
以下、モデル検証用単体テスト
"""""""""""""""""""""
def create_user():
    return User.objects.create()

def create_task():
    return Task.objects.create()

def create_nippou():
    return nippou_data.objects.create()

class UserModelTests(TestCase):
    def create_user(self, username='', user_dev=''):
        user = User.objects.create(username=username, user_dev=user_dev)
        user.save()
        return user

    def test_user_is_empty(self):
        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 0)

    def test_user_is_not_empty(self):
        self.create_user('test', 'test_dev')
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_saving_and_retrieving_user(self):
        self.create_user('test', 'test_dev')
        user = User.objects.all()[0]

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.user_dev, 'test_dev')

class NippouModelTests(TestCase):
    def create_nippou(self, username='', title=''):
        user = User(username=username)
        user.save()
        nippou = nippou_data.objects.create(user=user, title=title)
        nippou.save()
        return nippou

    def test_nippou_is_empty(self):
        nippous = nippou_data.objects.all()
        self.assertEqual(nippous.count(), 0)

    def test_nippou_is_not_empty(self):
        username = 'test_user'
        self.create_nippou(username=username, title='test_title')
        nippous = nippou_data.objects.all()
        self.assertEqual(nippous.count(), 1)

    def test_saving_and_retrieving_nippou(self):
        username = 'test_user'
        title = 'test_title'
        self.create_nippou(username=username, title='test_title')
        nippou = nippou_data.objects.all()[0]

        self.assertEqual(nippou.user.username, username)
        self.assertEqual(nippou.title, title)

class TaskModelTest(TestCase):
    def create_task(self, username='', title='', taskname=''):
        user = User(username=username)
        user.save()
        nippou = nippou_data.objects.create(user=user, title=title)
        nippou.save()
        task = Task.objects.create(nippou=nippou, task_name=taskname, time_yotei=1, time_jitsu=1) # have to specify these times
        task.save()
        return task

    def test_task_is_empty(self):
        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 0)

    def test_task_is_not_empty(self):
        self.create_task('test_user', 'test_title', 'test_task')
        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 1)


    def test_saving_and_retrieving_nippou(self):
        username = 'test_user'
        title = 'test_title'
        taskname = 'test_task'
        self.create_task(username=username, title=title, taskname=taskname)
        task = Task.objects.all()[0]

        self.assertEqual(task.nippou.title, title)
        self.assertEqual(task.task_name, taskname)


"""""""""""""""""""""
以下、URL解決検証用単体テスト
"""""""""""""""""""""

from django.core.urlresolvers import resolve
from django.test import TestCase
from nippou_app.views import edit, delete, show, detail, search, mypage, make
from nippou_app.views import taskedit, taskadd, taskdelete

class UrlResolveTests(TestCase):
    def test_url_resolves_to_show_view(self):
        found = resolve('/nippou_app/')
        self.assertEqual(found.func, show)

    def test_url_resolves_to_mypage_view(self):
        found = resolve('/mypage/')
        self.assertEqual(found.func, mypage)

    def test_url_resolves_to_search_view(self):
        found = resolve('/nippou_app/search/')
        self.assertEqual(found.func, search)

    def test_url_resolves_to_delete_view(self):
        found = resolve('/nippou_app/delete/1/')
        self.assertEqual(found.func, delete)

    def test_url_resolves_to_edit_view(self):
        found = resolve('/nippou_app/edit/1/')
        self.assertEqual(found.func, edit)
        found = resolve('/nippou_app/new/')
        self.assertEqual(found.func, edit)

    def test_url_resolves_to_detail_view(self):
        found = resolve('/nippou_app/1/')
        self.assertEqual(found.func, detail)

    def test_url_resolves_to_taskadd_view(self):
        found = resolve('/nippou_app/taskadd/1/')
        self.assertEqual(found.func, taskadd)

    def test_url_resolves_to_taskedit_view(self):
        found = resolve('/nippou_app/taskedit/1/')
        self.assertEqual(found.func, taskedit)

    def test_url_resolves_to_taskdelete_view(self):
        found = resolve('/nippou_app/taskdelete/1/')
        self.assertEqual(found.func, taskdelete)

    def test_url_resolves_to_make_view(self):
        found = resolve('/nippou_app/make/1/')
        self.assertEqual(found.func, make)


"""""""""""""""""""""
以下、ビューのHTML返却検証用単体テスト
"""""""""""""""""""""

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from nippou_app.views import *


class HtmlTests(TestCase):
    def test_show_page_returns_correct_html(self):
        request = HttpRequest()
        task_test = TaskModelTest()
        task = task_test.create_task()

        request.user = task.nippou.user
        response = show(request)
        expected_html = render_to_string('nippou_app/nippou_show.html',
                                         {'nippous': [task.nippou], 'tasks':task, 'uname':request.user.last_name+request.user.first_name})
        self.assertEqual(response.content.decode(), expected_html)

    def test_mypage_page_returns_correct_html(self):
        request = HttpRequest()
        task_test = TaskModelTest()
        task = task_test.create_task()

        request.user = task.nippou.user
        response = mypage(request)
        expected_html = render_to_string('nippou_app/mypage.html',
                                         {'nippous': [task.nippou], 'tasks':[task], 'uname':request.user.last_name+request.user.first_name})
        self.assertEqual(response.content.decode(), expected_html)

    """
    def test_search_page_returns_correct_html(self):
        request = HttpRequest()
        nippou_test = NippouModelTests()
        nippou = nippou_test.create_nippou()
        form = NippouSearchForm()

        request.user = nippou.user
        response = search(request)
        expected_html = render_to_string('nippou_app/nippou_search.html',
                                         {'form': form, 'nippous':[nippou]} )
        self.assertEqual(response.content.decode(), expected_html)
    """


"""""""""""""""""""""
以下、フォームの検証用単体テスト
"""""""""""""""""""""

from django.test import TestCase
from nippou_app.views import NippouEditForm, TaskEditForm, NippouSearchForm
from nippou_app.models import nippou_data, Task

class NippouFormTests(TestCase):
    def test_valid(self):
        params = dict(title='test_title', text='test', date='2015-05-28 17:04:40')
        nippou = nippou_data()
        form = NippouEditForm(params, instance=nippou)
        self.assertTrue(form.is_valid())

    def test_either1(self):
        params = dict()
        nippou = nippou_data()
        form = NippouEditForm(params, instance=nippou)
        self.assertFalse(form.is_valid())


class TaskFormTests(TestCase):
    def test_valid(self):
        params = dict(task_name='task_test', time_yotei=0, time_jitsu=0, task_y='y', task_w='w', task_t='t')
        task = Task()
        form = TaskEditForm(params, instance=task)
        self.assertTrue(form.is_valid())

    def test_either1(self):
        params = dict()
        task = Task()
        form = TaskEditForm(params, instance=task)
        self.assertFalse(form.is_valid())

class NippouSearchForm(TestCase):
    def test_valid(self):
        params = dict(keyword='keyword')
        nippou = nippou_data()
        form = NippouSearchForm(params)
        self.assertTrue(form.is_valid())

    def test_either1(self):
        params = dict()
        nippou = nippou_data()
        form = NippouSearchForm(params)
        self.assertFalse(form.is_valid())