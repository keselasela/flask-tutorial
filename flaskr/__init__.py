import os

from flask import Flask

# create_appについて https://kuzunoha-ne.hateblo.jp/entry/2019/03/29/200000
#関数の中にオブジェクト作成を入れることによって跡で複数インスタンスを作れる
def create_app(test_config=None):
    #instance_relative_config=True アプリの設定はinstance_folderに関連しているということ　
    app = Flask(__name__, instance_relative_config=True)
    
    #今後使うであろうデフォルトの設定をしている
    app.config.from_mapping(
    	#データを守るためのキー
        SECRET_KEY='dev',
        #データベースが保存されている場所のパス　データベースについては違うセクションで学ぶ
        #app.instance_pathとはinstance foloderのパス
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #instance_folderにあるconfig.pyによってデフォルト設定を上書きする（例えばデプロイの際にSECRET_KYを設定）
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
    	#確実にinstance folderを作る
        os.makedirs(app.instance_path)
    except OSError:
        pass
	#---------------------------------------------------------------------------
    
    from . import db
    #アプリを初期化　クリーニング関数とコマンドを設定
    db.init_app(app)
    #-----------------------------------------------------------------------------
    from . import auth
    app.register_blueprint(auth.bp)
    from . import blog
    app.register_blueprint(blog.bp)

    #--------------------------------------------------------------------------------
    #"index"と"/"を関連つけている。つまり、url_for('index')はURL'/'を作り出す
    #app.add_url_rule('/', endpoint='index')

    return app
    
    
    
