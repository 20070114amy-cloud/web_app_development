import sqlite3
import os

# 動態取得根目錄，對應到 instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """
    取得 SQLite 資料庫連線
    為了確保系統穩定，遇到問題時會拋出例外讓上層處理。
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  
        return conn
    except sqlite3.Error as e:
        print(f"[DB Error] 連線失敗: {e}")
        raise

class TaskModel:
    @staticmethod
    def create(title):
        """
        新增任務
        參數: title (str) - 任務標題
        回傳: task_id (int) - 新增成功的紀錄 ID，若失敗則回傳 None
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tasks (title, status) VALUES (?, ?)',
                (title, 'active')
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[DB Error] 新增任務發生錯誤: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all(status_filter=None):
        """
        取得任務列表
        參數: status_filter (str, 可選) - 設定為 'active' 或 'completed'
        回傳: list of dict - 所有符合條件的任務字典，失敗時回傳空陣列 []
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if status_filter:
                cursor.execute('SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', (status_filter,))
            else:
                cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
                
            tasks = cursor.fetchall()
            return [dict(task) for task in tasks]
        except sqlite3.Error as e:
            print(f"[DB Error] 取得任務列表發生錯誤: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(task_id):
        """
        依照 ID 取得單筆任務詳細資訊
        參數: task_id (int) - 指定的任務 ID
        回傳: dict - 單一任務字典，若查無資料或發生錯誤則回傳 None
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            return dict(task) if task else None
        except sqlite3.Error as e:
            print(f"[DB Error] 取得單一任務發生錯誤: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update_status(task_id, new_status):
        """
        修改指定任務的狀態
        參數: task_id (int) - 任務 ID, new_status (str) - 新的狀態字串
        回傳: bool - 成功回傳 True，失敗回傳 False
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE tasks SET status = ? WHERE id = ?',
                (new_status, task_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DB Error] 更新任務狀態發生錯誤: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(task_id):
        """
        刪除指定任務
        參數: task_id (int) - 要刪除的任務 ID
        回傳: bool - 成功回傳 True，失敗回傳 False
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DB Error] 刪除任務發生錯誤: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

def init_db():
    """初始化並建立 Table, 啟動應用時由 app.py 呼叫一次"""
    schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
    if os.path.exists(schema_path):
        conn = None
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            conn = get_db_connection()
            conn.executescript(schema_sql)
            conn.commit()
        except sqlite3.Error as e:
            print(f"[DB Error] 初始化 SQLite 資料表時發生錯誤: {e}")
            if conn:
                conn.rollback()
        except Exception as e:
            print(f"[System Error] 嘗試讀取 schema.sql 發生意外錯誤: {e}")
        finally:
            if conn:
                conn.close()
