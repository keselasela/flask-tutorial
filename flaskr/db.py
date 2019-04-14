import sqlite3

import click
#g-request毎に固有データを持つ・リクエスト中に関数によって参照されるであろうデータを保持

from flask import current_app, g
from flask.cli import with_appcontext

#get_dbが同じリクエストで二階呼ばれたときはコネクションが再利用？？
def get_db():
    if 'db' not in g:
    	#sqlite3.connect()は[database configuration key]によって指定されたファイルに接続を確立する
        g.db = sqlite3.connect(
        	#current_app-requestをさばくアプリケーションを指す
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #sqlite3.Rowはコネクションに行を返すように命令する
        g.db.row_factory = sqlite3.Row
        click.echo('get_db()')
        
    return g.db

#g.dbが設定されたかどうかを調べて、コネクションが作らたかを調べるおーコネクションあったら削除
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
#----------------------------------------------------------------------------------------------

def init_db():
    db = get_db()
	#open_resource()-フラスコパッケージから相対的位置にあるファイルを開く関数
	#ファイルから読み取ったコマンドを実行するため
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#init-dbというコマンドラインコマンドを定義、init_db関数を呼び出し、成功アラートを表示
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    
#----------------------------------------------------------------------------------------------
#アプリを初期化　クリーニング関数とコマンドを設定
def init_app(app):
	#app.teardown.appcontext()-レスポンスを返した後のクリーニングで関数を呼び出す
    app.teardown_appcontext(close_db)
    #flskコマンドと一緒に呼ばれるコマンドを追加
    app.cli.add_command(init_db_command)    



    
    
    
    
    
