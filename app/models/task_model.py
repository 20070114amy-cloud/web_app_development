import sqlite3
import os

# 動態取得根目錄，對應到 instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """取得 SQLite 資料庫連線"""
    # 確保儲存資料庫的 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # 設定回傳型別為 Dict，讓取用欄位時比較直觀
    conn.row_factory = sqlite3.Row  
    return conn

class TaskModel:
    @staticmethod
    def create(title):
        """新增任務"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, status) VALUES (?, ?)',
            (title, 'active')
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id

    @staticmethod
    def get_all(status_filter=None):
        """取得任務 (可選擇過濾特定 status)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status_filter:
            cursor.execute('SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', (status_filter,))
        else:
            cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            
        tasks = cursor.fetchall()
        conn.close()
        return [dict(task) for task in tasks]

    @staticmethod
    def get_by_id(task_id):
        """依照 ID 取得單筆任務詳細資訊"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        conn.close()
        return dict(task) if task else None

    @staticmethod
    def update_status(task_id, new_status):
        """修改指定任務的狀態"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET status = ? WHERE id = ?',
            (new_status, task_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        """刪除指定任務"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

def init_db():
    """初始化並建立 Table, 通常只在應用啟動或開發初期時呼叫"""
    schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        conn = get_db_connection()
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()
