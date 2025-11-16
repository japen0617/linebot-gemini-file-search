# 專案完整概述 📚

> 這份文件提供 LINE Bot 智能文件助手的完整技術概述，包括架構、功能、實作細節與執行方式。

---

## 📋 目錄

1. [專案目的](#專案目的)
2. [核心功能](#核心功能)
3. [技術架構](#技術架構)
4. [資料夾結構](#資料夾結構)
5. [程式進入點](#程式進入點)
6. [主要函數運作方式](#主要函數運作方式)
7. [關鍵設定檔](#關鍵設定檔)
8. [執行專案](#執行專案)
9. [部署方式](#部署方式)

---

## 專案目的

**LINE Bot 智能文件助手** 是一個結合 **LINE Messaging API** 與 **Google Gemini AI** 的智能問答機器人。

### 🎯 核心價值

- **文件智能問答**：上傳 PDF、Word、文字檔等文件後，使用自然語言提問，AI 會基於文件內容回答
- **圖片智能分析**：傳送圖片給 Bot，立即獲得 AI 視覺分析結果（場景、物品、文字辨識等）
- **多人協作支援**：支援 1對1 聊天與群組聊天，文件共享與隱私隔離機制完善
- **即時回應**：FastAPI 異步架構，高效處理並發請求

### 💡 使用情境

1. **文件研究**：上傳研究論文或技術文件，快速取得摘要與重點
2. **會議記錄查詢**：上傳會議記錄，詢問特定決議或討論內容
3. **圖片內容辨識**：拍攝產品標籤、文件照片，快速取得文字內容
4. **團隊協作**：在 LINE 群組中共享文件，成員可共同查詢內容

---

## 核心功能

### 1. 📄 文件上傳與管理

- **支援格式**：PDF、DOCX、TXT 及其他 Google Gemini File API 支援的格式
- **自動上傳**：檔案自動上傳至 Google Gemini File Search Store
- **檔案管理**：支援列出已上傳檔案、查看上傳時間
- **檔案刪除**：透過互動式 Flex Message Carousel 刪除不需要的檔案

### 2. 🖼️ 圖片即時分析

- **支援格式**：JPG、JPEG、PNG、GIF、WebP
- **即時分析**：使用 Gemini Vision 能力即時分析圖片內容
- **詳細描述**：AI 會描述圖片中的場景、物品、文字等資訊
- **無需儲存**：圖片分析後立即清除，不占用儲存空間

### 3. 🤖 AI 智能問答

- **基於文件回答**：使用 Google Gemini File Search 技術，根據上傳的文件內容回答問題
- **引用來源**：回答時提供引用來源（Citations），可查看原始文件片段
- **自然語言**：支援繁體中文、英文等多語言自然對話
- **Quick Reply**：上傳檔案後提供快捷按鈕（生成摘要、重點整理等）

### 4. 👥 多人協作支援

#### 1對1 聊天
- ✅ 每個使用者有獨立的文件庫
- ✅ 所有訊息都會回覆
- ✅ 完全隱私保護

#### 群組聊天
- ✅ 群組成員共享文件庫
- ✅ 文字訊息需 @mention 機器人才回覆（避免干擾群組對話）
- ✅ 上傳檔案/圖片無需 mention，自動處理
- ✅ 回覆訊息顯示在群組中，所有成員可見

### 5. 🎨 互動式使用者介面

- **Quick Reply 快捷按鈕**：上傳成功後提供常用操作按鈕
- **Flex Message Carousel**：美觀的檔案列表卡片，支援分頁與刪除
- **引用查看**：點擊引用按鈕可查看 AI 回答的原始來源片段

---

## 技術架構

### 🛠️ 技術堆疊

```
┌─────────────────────────────────────────────┐
│           LINE Messaging API                │
│        (Webhook 接收使用者訊息)              │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│          FastAPI (Python 3.10)              │
│       (異步處理 & Webhook Handler)           │
└─────────────┬───────────────────────────────┘
              │
         ┌────┴────┐
         ▼         ▼
┌──────────────┐ ┌──────────────────────────┐
│ LINE Bot API │ │  Google Gemini API       │
│ - 推送訊息    │ │  - File Search (文件)    │
│ - Quick Reply│ │  - Vision (圖片)         │
│ - Flex Msg   │ │  - Generate Content      │
└──────────────┘ └──────────────────────────┘
```

### 📦 核心依賴套件

| 套件 | 版本 | 用途 |
|------|------|------|
| `line-bot-sdk` | 3.14.0 | LINE Messaging API SDK |
| `fastapi` | ≥0.116.2 | 高效能 Web 框架 |
| `uvicorn` | ≥0.34.0 | ASGI 伺服器 |
| `google-genai` | ≥1.45.0 | Google Gemini AI SDK |
| `aiohttp` | (間接依賴) | 異步 HTTP 客戶端 |
| `aiofiles` | 24.1.0 | 異步檔案操作 |
| `requests` | ≥2.32.4 | REST API 請求 |
| `Pillow` | 11.0.0 | 圖片處理 |

### 🔄 資料流程

#### 文件上傳流程
```
使用者上傳檔案 → LINE 伺服器
                     ↓
              Webhook 通知 FastAPI
                     ↓
         下載檔案到本地 (uploads/)
                     ↓
    上傳至 Google Gemini File Search Store
                     ↓
         刪除本地暫存檔案
                     ↓
      回覆使用者「上傳成功」+ Quick Reply
```

#### 文件查詢流程
```
使用者提問 → Webhook 通知 FastAPI
                  ↓
     檢查是否為群組 & 是否 mention bot
                  ↓
   呼叫 Google Gemini File Search API
                  ↓
      AI 基於文件內容生成回答
                  ↓
    提取引用來源 (Citations)
                  ↓
    回覆使用者 + 引用快捷按鈕
```

#### 圖片分析流程
```
使用者傳送圖片 → LINE 伺服器
                     ↓
              Webhook 通知 FastAPI
                     ↓
         下載圖片到本地 (uploads/)
                     ↓
      使用 Gemini Vision API 分析
                     ↓
         刪除本地暫存圖片
                     ↓
         回覆分析結果
```

---

## 資料夾結構

```
linebot-gemini-file-search/
│
├── main.py                      # 主程式進入點 (FastAPI app)
│
├── requirements.txt             # Python 依賴套件清單
├── runtime.txt                  # Python 版本指定 (3.10.17)
│
├── Dockerfile                   # Docker 容器化設定
├── Procfile                     # Heroku/雲端部署設定
│
├── README.md                    # 專案說明文件
├── PROJECT_OVERVIEW.md          # 本文件 (完整技術概述)
├── GROUP_USAGE_GUIDE.md         # 群組使用指南
├── CHANGES_GROUP_SUPPORT.md     # 群組支援變更記錄
│
├── test_group_mention.py        # 單元測試 (mention 檢測邏輯)
│
├── uploads/                     # 暫存上傳檔案的目錄 (自動建立)
│
└── .gitignore                   # Git 忽略檔案清單
```

### 📄 檔案說明

#### 核心程式
- **`main.py`** (1014 行)
  - FastAPI 應用程式主體
  - Webhook handler
  - 所有業務邏輯與 AI 整合

#### 設定檔
- **`requirements.txt`**：Python 依賴套件
- **`runtime.txt`**：指定 Python 版本
- **`Dockerfile`**：Docker 容器化設定
- **`Procfile`**：雲端平台部署設定

#### 文件
- **`README.md`**：面向使用者的說明文件
- **`PROJECT_OVERVIEW.md`**：面向開發者的技術文件
- **`GROUP_USAGE_GUIDE.md`**：群組使用的詳細指南
- **`CHANGES_GROUP_SUPPORT.md`**：群組功能變更記錄

#### 測試
- **`test_group_mention.py`**：測試 mention 檢測邏輯

---

## 程式進入點

### 主程式：`main.py`

```python
# 初始化 FastAPI 應用
app = FastAPI()

# 主要 Webhook 端點
@app.post("/")
async def handle_callback(request: Request):
    """
    處理來自 LINE 的 Webhook 請求
    
    流程：
    1. 驗證簽章 (signature)
    2. 解析事件 (MessageEvent, PostbackEvent)
    3. 根據訊息類型分派處理
       - 文字訊息 → handle_text_message()
       - 檔案訊息 → handle_document_message()
       - 圖片訊息 → handle_image_message()
       - Postback → handle_postback()
    """
    ...
```

### 啟動方式

使用 **Uvicorn** ASGI 伺服器啟動 FastAPI 應用：

```bash
uvicorn main:app --host=0.0.0.0 --port=8000
```

- `main:app` - 載入 `main.py` 的 `app` 物件
- `--host=0.0.0.0` - 監聽所有網路介面
- `--port=8000` - 監聽 8000 埠

### 環境變數

程式啟動時會檢查以下環境變數：

| 變數名稱 | 必要性 | 說明 |
|---------|-------|------|
| `ChannelSecret` | ✅ 必要 | LINE Bot Channel Secret |
| `ChannelAccessToken` | ✅ 必要 | LINE Bot Channel Access Token |
| `GOOGLE_API_KEY` | ✅ 必要 | Google Gemini API Key |

若缺少任何必要變數，程式會終止並顯示錯誤訊息。

---

## 主要函數運作方式

由於文件篇幅較長，這裡僅說明核心函數的運作邏輯。詳細程式碼請參考 `main.py`。

### 🔧 輔助函數

#### 1. `get_store_name(event) -> str`
**用途**：根據對話類型取得 File Search Store 名稱

- 1對1 聊天：`"user_{user_id}"`
- 群組聊天：`"group_{group_id}"`
- Room 聊天：`"room_{room_id}"`

這樣可以實現：
- 1對1：每人獨立文件庫
- 群組：成員共享文件庫

#### 2. `get_reply_target(event) -> str`
**用途**：取得正確的訊息推送目標 ID

用於 `push_message()`，確保訊息發送到正確位置：
- 群組上傳檔案 → 回覆到群組
- 1對1 上傳檔案 → 回覆到個人

#### 3. `is_bot_mentioned(event, bot_user_id) -> bool`
**用途**：檢查 Bot 是否被 @mention（群組聊天關鍵）

邏輯：
1. 1對1 聊天 → 永遠回傳 True
2. 群組/Room → 檢查 `mention.mentionees`，比對 `mentionee.user_id == bot_user_id`

用途：避免在群組中每句話都回覆

---

### 📥 檔案處理函數

#### 1. `download_line_content(message_id, file_name) -> Path`
**用途**：從 LINE 伺服器下載檔案或圖片

步驟：
1. 使用 `line_bot_api.get_message_content(message_id)`
2. 儲存到 `uploads/{message_id}{副檔名}`
3. 回傳檔案路徑

#### 2. `upload_to_file_search_store(file_path, store_name, display_name) -> bool`
**用途**：上傳檔案到 Google Gemini File Search Store

步驟：
1. 確保 Store 存在 (`ensure_file_search_store_exists`)
2. 使用 `client.file_search_stores.upload_to_file_search_store()`
3. 等待上傳操作完成 (`operation.done`)

#### 3. `list_documents_in_store(store_name) -> list`
**用途**：列出 Store 中的所有文件

使用 REST API（比 SDK 更穩定）取得文件清單，回傳包含檔案名稱、上傳時間等資訊的陣列。

#### 4. `delete_document(document_name) -> bool`
**用途**：刪除文件

**注意**：File Search Store 的文件刪除需要 `force=True` 參數。

---

### 🤖 AI 處理函數

#### 1. `query_file_search(query, store_name) -> tuple[str, list]`
**用途**：使用 File Search 查詢文件並生成回答

步驟：
1. 取得實際 Store 名稱
2. 建立 FileSearch tool
3. 呼叫 `generate_content()` 生成回答
4. 提取 grounding_metadata (引用來源)
5. 回傳 (AI回答, 引用清單)

#### 2. `analyze_image_with_gemini(image_path) -> str`
**用途**：使用 Gemini Vision 分析圖片

步驟：
1. 讀取圖片 bytes
2. 根據副檔名判斷 MIME type
3. 建立 image Part
4. 呼叫 `generate_content()` 分析
5. 回傳分析結果文字

---

### 💬 訊息處理函數

#### 1. `handle_text_message(event, message, bot_user_id)`
**用途**：處理文字訊息（查詢文件或列出檔案）

流程：
1. 檢查是否需要回覆 (`is_bot_mentioned`)
2. 判斷意圖：列出檔案 或 查詢文件
3. 回覆訊息 + Quick Reply (引用按鈕)

#### 2. `handle_document_message(event, message)`
**用途**：處理檔案上傳

流程：
1. 下載檔案
2. 上傳至 File Search Store
3. 刪除本地暫存檔
4. 回覆成功訊息 + Quick Reply

Quick Reply 按鈕：
- 📝 生成檔案摘要
- 📌 重點整理
- 📋 列出檔案

#### 3. `handle_image_message(event, message)`
**用途**：處理圖片上傳

流程：
1. 下載圖片
2. 使用 Gemini Vision 分析
3. 刪除暫存圖片
4. 回覆分析結果

**特點**：即時分析，不儲存到 File Search Store

#### 4. `handle_postback(event)`
**用途**：處理 Postback 事件（按鈕點擊）

支援的 action：
- `delete_file`：刪除檔案
- `query`：Quick Reply 查詢
- `list_files`：列出檔案（含分頁）
- `view_citation`：查看引用來源

---

### 🎨 UI 相關函數

#### `send_files_carousel(event, documents, page, store_name)`
**用途**：以 Flex Message Carousel 顯示檔案列表

特色：
- 每頁最多 11 個檔案
- 第 12 個位置顯示分頁控制
- 每個檔案卡片顯示：檔案圖示、檔案名稱、上傳時間、刪除按鈕

---

## 關鍵設定檔

### 1. `requirements.txt`
**用途**：Python 依賴套件清單

```txt
line-bot-sdk==3.14.0
fastapi>=0.116.2
uvicorn[standard]>=0.34.0,<1.0.0
google-genai>=1.45.0,<2.0.0
pydantic>=2.10.3,<3.0.0
tiktoken==0.8.0
Pillow==11.0.0
aiofiles==24.1.0
requests>=2.32.4,<3.0.0
```

**安裝方式**：
```bash
pip install -r requirements.txt
```

### 2. `runtime.txt`
**用途**：指定 Python 版本（用於雲端部署）

```txt
python-3.10.17
```

### 3. `Dockerfile`
**用途**：Docker 容器化設定

```dockerfile
FROM python:3.10.17

# 複製專案
COPY . /app
WORKDIR /app

# 安裝依賴
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# 啟動服務
EXPOSE 8080
CMD uvicorn main:app --host=0.0.0.0 --port=$PORT
```

### 4. `Procfile`
**用途**：Heroku/雲端平台部署設定

```
web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
```

### 5. `.gitignore`
**用途**：Git 版本控制忽略清單

忽略項目包括：Python cache、虛擬環境、IDE 設定、暫存檔案目錄 (`uploads/`)、環境變數檔 (`.env`) 等。

---

## 執行專案

### 📋 前置準備

#### 1. 安裝 Python 3.10+
```bash
python --version  # 確認版本
```

#### 2. 克隆專案
```bash
git clone https://github.com/japen0617/linebot-gemini-file-search.git
cd linebot-gemini-file-search
```

#### 3. 安裝依賴
```bash
pip install -r requirements.txt
```

#### 4. 取得 API Keys

**LINE Bot：**
1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 建立 Messaging API Channel
3. 取得 Channel Secret 和 Channel Access Token

**Google Gemini：**
1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 建立 API Key

#### 5. 設定環境變數

```bash
export ChannelSecret="你的_LINE_CHANNEL_SECRET"
export ChannelAccessToken="你的_LINE_CHANNEL_ACCESS_TOKEN"
export GOOGLE_API_KEY="你的_GOOGLE_API_KEY"
```

---

### 🚀 本地開發

#### 1. 啟動服務
```bash
uvicorn main:app --reload --host=0.0.0.0 --port=8000
```

- `--reload` - 自動重載（檔案變更時）
- `--host=0.0.0.0` - 監聽所有網路介面
- `--port=8000` - 使用 8000 埠

#### 2. 使用 ngrok 建立公開網址

LINE Bot 需要 HTTPS 的公開 Webhook URL。本地開發時使用 ngrok：

```bash
# 安裝 ngrok
brew install ngrok  # macOS

# 建立隧道
ngrok http 8000
```

ngrok 會顯示公開網址：`https://abc123.ngrok.io`

#### 3. 設定 LINE Webhook URL

前往 LINE Developers Console：
1. 選擇你的 Channel
2. Messaging API 設定
3. Webhook URL 設定為：`https://abc123.ngrok.io/`
4. 啟用 Webhook
5. 關閉「自動回覆訊息」

---

### 🐳 Docker 部署

#### 1. 建立映像
```bash
docker build -t linebot-file-search .
```

#### 2. 啟動容器
```bash
docker run -d \
  --name linebot \
  -p 8000:8000 \
  -e ChannelSecret=你的SECRET \
  -e ChannelAccessToken=你的TOKEN \
  -e GOOGLE_API_KEY=你的API_KEY \
  linebot-file-search
```

---

## 部署方式

### ☁️ Google Cloud Run

#### 部署步驟

**1. 安裝 gcloud CLI**
```bash
# macOS
brew install --cask google-cloud-sdk
```

**2. 登入並設定專案**
```bash
gcloud auth login
gcloud config set project 你的專案ID
```

**3. 建立並推送映像**
```bash
gcloud builds submit --tag gcr.io/你的專案ID/linebot-file-search
```

**4. 部署到 Cloud Run**
```bash
gcloud run deploy linebot-file-search \
  --image gcr.io/你的專案ID/linebot-file-search \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars ChannelSecret=你的SECRET,ChannelAccessToken=你的TOKEN,GOOGLE_API_KEY=你的API_KEY
```

**5. 取得服務網址**
```bash
gcloud run services describe linebot-file-search \
  --platform managed \
  --region asia-east1 \
  --format 'value(status.url)'
```

將取得的網址設定到 LINE Developers Console 的 Webhook URL。

---

### 🔒 使用 Secret Manager（推薦）

不要將敏感資訊寫在程式碼或環境變數，使用 Secret Manager：

**1. 建立 secrets**
```bash
echo -n "你的SECRET" | gcloud secrets create line-channel-secret --data-file=-
echo -n "你的TOKEN" | gcloud secrets create line-channel-token --data-file=-
echo -n "你的API_KEY" | gcloud secrets create google-api-key --data-file=-
```

**2. 部署時使用 secrets**
```bash
gcloud run deploy linebot-file-search \
  --image gcr.io/你的專案ID/linebot-file-search \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --update-secrets=ChannelSecret=line-channel-secret:latest,ChannelAccessToken=line-channel-token:latest,GOOGLE_API_KEY=google-api-key:latest
```

---

## 📊 監控與除錯

### Cloud Run Logs
```bash
# 查看最近 50 筆 logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=linebot-file-search" --limit 50

# 即時串流 logs
gcloud alpha logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=linebot-file-search"
```

### 常見問題

**1. Bot 不回覆**
- 檢查 Webhook URL 是否正確
- 確認環境變數是否設定
- 確認 LINE Webhook 是否啟用

**2. 群組中無法回覆**
- 確認是否有 @mention Bot
- 檢查 Bot User ID 是否正確取得

**3. 檔案上傳失敗**
- 檢查 GOOGLE_API_KEY 是否有效
- 確認 File Search API 是否啟用

---

## 🎓 學習資源

### 官方文件
- [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Google Gemini File Search](https://ai.google.dev/gemini-api/docs/file-search)
- [FastAPI](https://fastapi.tiangolo.com/)

### 專案文件
- [README.md](./README.md) - 使用者指南
- [GROUP_USAGE_GUIDE.md](./GROUP_USAGE_GUIDE.md) - 群組使用指南
- [CHANGES_GROUP_SUPPORT.md](./CHANGES_GROUP_SUPPORT.md) - 變更記錄

---

## 🙋 常見問題

### Q: 為什麼群組中 Bot 不回覆？
A: 在群組聊天中，Bot 只會在被 @mention 時回覆文字訊息。這是為了避免干擾群組正常對話。上傳檔案/圖片不需要 mention。

### Q: 檔案會保存多久？
A: 文件檔案會持續保存在 Google Gemini File Search Store 中。圖片分析後會立即清除。

### Q: 支援哪些檔案格式？
A: 文件：PDF、DOCX、TXT 等（取決於 Google Gemini File API）。圖片：JPG、JPEG、PNG、GIF、WebP。

### Q: 如何刪除上傳的檔案？
A: 輸入「列出檔案」，在 Carousel 卡片中點擊「🗑️ 刪除檔案」按鈕。

### Q: 群組中的檔案會被其他成員看到嗎？
A: 會。群組成員共享同一個文件庫。如需私密查詢，請在 1對1 聊天中上傳。

---

**文件版本**：v1.0.0  
**最後更新**：2025-11-16  
**作者**：japen0617

---

⭐ 如果這個專案對你有幫助，請給個 Star！
