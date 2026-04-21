# 路由與頁面設計 (Routes Design)

## 1. 路由總覽表格

本系統操作集中單純，因此所有頁面渲染都將圍繞在首頁 (`/`)，其餘功能性路由皆為處理動作並在完成後立即「重導向」(Redirect) 迴轉至首頁。

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (任務清單) | GET | `/` | `templates/index.html` | 顯示所有任務，並支援 `?filter=status` 過濾條件 |
| 新增任務 | POST | `/tasks/create` | — | 接收新增表單內容，寫入資庫後重導向至 `/` |
| 切換完成狀態 | POST | `/tasks/<int:id>/toggle` | — | 將指定的任務於 active / completed 狀態互相切換，切換後重導向至 `/` |
| 刪除任務 | POST | `/tasks/<int:id>/delete` | — | 刪除指定任務，刪除後重導向至 `/` |

## 2. 每個路由的詳細說明

### `GET /` (任務清單)
- **輸入**：可選的 URL 參數 `?filter=` (可為 `active` 或是 `completed`)
- **處理邏輯**：
  - 接收到要求後，檢查是否有 `filter` 查詢字串。
  - 若有，呼叫 `TaskModel.get_all(status_filter=...)` 取得對應資料。
  - 若無，直接呼叫 `TaskModel.get_all()` 獲取全部清單。
- **輸出**：渲染 `templates/index.html`，並將撈出的任務列表變數傳遞過去。
- **錯誤處理**：無。清單為空時，由前端 Jinja2 控制顯示「無待辦任務」字樣即可。

### `POST /tasks/create` (新增任務)
- **輸入**：HTML form 所送出的表單欄位 `title`
- **處理邏輯**：
  - 由 `request.form.get('title')` 取得標題。
  - 驗證標題不為純空白；若合法則呼叫 `TaskModel.create(title)` 寫入 DB。
- **輸出**：回傳 HTTP 302，重導向至首頁 (`/`)。
- **錯誤處理**：若 title 為空，使用 Flask 的 `flash()` 功能紀錄錯誤訊息後，依然重導至首頁並把錯誤顯示在頂端。

### `POST /tasks/<int:id>/toggle` (切換任務狀態)
- **輸入**：URL 路徑中夾帶的變數 `id`
- **處理邏輯**：
  - 呼叫 `TaskModel.get_by_id(id)` 檢查任務是否存在。
  - 若狀態為 `'active'`，便呼叫 `TaskModel.update_status(id, 'completed')`；若是已完成則改為 `'active'`。
- **輸出**：回傳 HTTP 302，重導向至首頁 (`/`)。
- **錯誤處理**：若該 id 不存在於 DB 則不執行任何動作，直接重導向回首頁。

### `POST /tasks/<int:id>/delete` (刪除任務)
- **輸入**：URL 路徑中夾帶的變數 `id`
- **處理邏輯**：
  - 調用 `TaskModel.delete(id)` 進行刪除。
- **輸出**：回傳 HTTP 302，重導向至首頁 (`/`)。
- **錯誤處理**：若 id 不存在同樣無須報錯，直接忽略即可。

## 3. Jinja2 模板清單

將透過兩個模板建立出簡單好維護的前端：

- **`templates/base.html`**：全站共用基底模板
  - 定義 `<!DOCTYPE html>` 與所有 HTML 骨架
  - 載入 CSS 與字體資源
  - 定義 `{% block content %}{% endblock %}` 供子模板插入內容
- **`templates/index.html`**：主畫面 (任務清單頁)
  - 使用 `{% extends 'base.html' %}` 繼承骨架
  - 實作在上方顯示「表單填寫區塊」
  - 實作使用 `{% for task in tasks %}` 迴圈渲染各筆待辦任務卡片
  - 裡面會為每個任務產出帶有對應 `/tasks/<id>/toggle` 或 `/tasks/<id>/delete` 路徑的按鈕表單

## 4. 路由骨架程式碼
請參考 `app/routes/task_routes.py` 檔案。我們採用建立 Blueprint 的方式管理這些路由，方便之後跟 `app.py` 銜接掛載。
