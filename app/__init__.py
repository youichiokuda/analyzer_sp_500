from flask import Flask
import os

def create_app():
    # Flaskアプリケーションインスタンスを作成
    app = Flask(__name__)

    # 設定（必要に応じて）
    app.config['SECRET_KEY'] =os.environ.get('SECRET_KEY')

    # ルートをインポート（循環インポートを避けるために関数内で行う）
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 他の設定や拡張機能の初期化（必要に応じて）

    return app
