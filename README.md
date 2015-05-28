nippou_proj
===========

このアプリは、日報作成のためのWebアプリ「タスクde日報」です。

※　nippou_proj/settings.pyは諸事情のため.gitignoreしてます。

特長
1. P/YWT（計画、やったこと、わかったこと、つぎやること）モデルに沿ったタスクの生成機能  
1日の終わりに日報を書くときには既に1日何をしたか、忘れてしまったということ、ありませんか？このアプリは、1日の中の各タスクについて個別に管理できます。各タスクで業務前にPを、業務中にYWを、業務後にTを書き込むことで、効果的に予実差、理解度や不明点などの振り返りを行えるようになっています。

2. 日報自動生成
日報作成のために1日の終わりに膨大な量のタスクを振り返るのは辛くありませんか？もしP/YWTモデルに沿ってタスクを作成しておけば、複数のタスクを自動的に１枚の日報に変換してくれます。あなたが書くことは、その日報に次やることと所感だけです。

3. 自分だけの業務メモツール
業務で必要になった、細々したメモはすぐに忘れてしまうものです。しかし、後日また必要になったりして悔しい思いをしたことありませんか？そんなときはタスクde日報のタスクをメモツールとして活用しましょう。そうすれば、後日いつでも振り返られます。この内容は自分だけが見ることができます。


その他、タスクde日報の機能は以下のとおりです。
* 日報作成に必須の基本的な機能（投稿、編集、削除、検索、一覧／個別表示）
* ユーザ認証機能（ログイン・ログアウト）
* 他ユーザの日報表示


（写真などでアプリイメージを伝える）


実行環境
===========
Python 3.4.2?
Django 1.8.4?
PostgreSQL x.x.x?

Pythonモジュール
psycopg2（PostgresSQLのドライバ）


実行準備
===========
* DB作成


実行方法
===========

```python

python manage.py runserver 8000

```

以下のように出力されれば正常に起動しています。
```bash

Performing system checks...

System check identified no issues (0 silenced).
May 27, 2015 - 20:21:21
Django version 1.8.2, using settings 'nippou_proj.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```


アプリ利用のための事前準備
===========
* 利用者登録のためサイト管理者にユーザ登録を申請し、IDとパスワードを入手してください
* 管理者は、以下のコマンドでユーザを作成してください

```bash

python manage.py createsuperuser

```


アプリ利用方法
========
1. http://172.0.0.1:8000/nippou_app にWebブラウザでアクセスし、ユーザ登録時にもらったID,パスワードでログインしてください
2. ログインに成功すれば、サイトトップページに移ります。ユーザ名が左上に表示されていることを確認してください

* 日報作成
* 