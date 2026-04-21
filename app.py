import os
from flask import Flask
from app.routes.task_routes import task_bp
from app.models.task_model import init_db

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key_for_dev')

# 註冊 Blueprint 路由
app.register_blueprint(task_bp)

if __name__ == '__main__':
    # 確保資料夾結構與資料庫在啟動時有被正確初始化
    init_db()
    
    # 啟動應用程式
    app.run(debug=True)
