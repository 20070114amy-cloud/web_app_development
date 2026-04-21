from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task_model import TaskModel

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
    # 從 URL Query String 中取得過濾狀態參數
    status_filter = request.args.get('filter')
    
    # 向 Model 要資料 (如果是 None 就會抓取全部)
    tasks = TaskModel.get_all(status_filter=status_filter)
    
    # 渲染 index.html，並將任務清單與當前的過濾字串傳給前端使用
    return render_template('index.html', tasks=tasks, current_filter=status_filter)


@task_bp.route('/tasks/create', methods=['POST'])
def create_task():
    """
    [新增任務]
    目的：接收表單資料並將新任務處存進資料庫
    輸入：表單內的 `title` 欄位
    輸出：處理完成後重導向 (Redirect) 至首頁
    邏輯：如果有填寫標題則呼叫 TaskModel 建立新資料；若空白則提示錯誤
    """
    title = request.form.get('title')
    
    # 驗證輸入內容是否為空值
    if not title or not title.strip():
        flash("任務標題不能為空！", "danger")
        return redirect(url_for('task_bp.index'))
        
    # 呼叫 Model 寫入資料庫
    result = TaskModel.create(title.strip())
    
    if result is None:
        flash("伺服器發生異常，新增任務失敗。", "danger")
    else:
        flash("任務新增成功！", "success")
        
    return redirect(url_for('task_bp.index'))


@task_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    [切換任務狀態]
    目的：將任務的 active (未完成) 重設為 completed (已完成) — 反之亦然
    輸入：從 URL 獲取任務的 ID
    輸出：重導向 (Redirect) 至首頁
    邏輯：查詢該任務目標原先狀態並進行狀態翻轉更新
    """
    # 先查詢有沒有這筆資料並得知當前狀態
    task = TaskModel.get_by_id(task_id)
    if not task:
        flash("找不到指定的任務。", "danger")
        return redirect(url_for('task_bp.index'))
        
    # 決定修改後的對應狀態
    new_status = 'completed' if task['status'] == 'active' else 'active'
    success = TaskModel.update_status(task_id, new_status)
    
    if not success:
        flash("更新任務狀態時發生錯誤。", "danger")
        
    # 修改後重導回首頁
    return redirect(url_for('task_bp.index'))


@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    [刪除任務]
    目的：移除特定任務資料
    輸入：從 URL 獲取要刪除的任務 ID
    輸出：重導向 (Redirect) 至首頁
    邏輯：呼叫 TaskModel 的 delete 方法將其從 SQLite 中移除
    """
    success = TaskModel.delete(task_id)
    
    if success:
        flash("任務已成功刪除。", "success")
    else:
        flash("刪除任務時發生錯誤。", "danger")
        
    return redirect(url_for('task_bp.index'))
