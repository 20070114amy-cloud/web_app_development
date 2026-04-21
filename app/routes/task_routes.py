from flask import Blueprint, render_template, request, redirect, url_for, flash

# 稍後實作時我們會引入 TaskModel，例如：
# from app.models.task_model import TaskModel

# 宣告 Blueprint 模組，之後會在 main app 裡面註冊它
task_bp = Blueprint('task_bp', __name__)


@task_bp.route('/', methods=['GET'])
def index():
    """
    [任務清單] 首頁
    目的：顯示所有任務或經狀態過濾後的任務清單。
    輸入：可接收 URL 參數 `?filter=active` 或 `?filter=completed`
    輸出：回傳渲染過後的 templates/index.html 畫面
    邏輯：呼叫 TaskModel 拿取對應任務，並傳入 Jinja2 模板
    """
    pass


@task_bp.route('/tasks/create', methods=['POST'])
def create_task():
    """
    [新增任務]
    目的：接收表單資料並將新任務處存進資料庫
    輸入：表單內的 `title` 欄位
    輸出：處理完成後重導向 (Redirect) 至首頁
    邏輯：如果有填寫標題則呼叫 TaskModel 建立新資料；若空白則提示錯誤
    """
    pass


@task_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    [切換任務狀態]
    目的：將任務的 active (未完成) 重設為 completed (已完成) — 反之亦然
    輸入：從 URL 獲取任務的 ID
    輸出：重導向 (Redirect) 至首頁
    邏輯：查詢該任務目標原先狀態並進行狀態翻轉更新
    """
    pass


@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    [刪除任務]
    目的：移除特定任務資料
    輸入：從 URL 獲取要刪除的任務 ID
    輸出：重導向 (Redirect) 至首頁
    邏輯：呼叫 TaskModel 的 delete 方法將其從 SQLite 中移除
    """
    pass
