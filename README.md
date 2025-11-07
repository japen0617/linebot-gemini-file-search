# LINE Bot 智能文件助手 📚

> 一個結合 LINE Bot 與 Google Gemini File Search 的智能文件問答機器人

## 🎯 這是什麼？

想像一下：你可以把任何 PDF、Word 文件、圖片傳給 LINE Bot，然後直接問它「這份文件在講什麼？」、「幫我整理重點」、「這張圖片裡有什麼？」，Bot 就會用 AI 幫你分析並回答！

這個專案讓你輕鬆打造一個專屬的文件智能助手，只要：
1. 📤 傳送文件或圖片給 Bot
2. 💬 用自然語言提問
3. 🤖 AI 立即分析並回答

## ✨ 功能特色

### 📁 支援多種檔案格式
- 📄 文件檔案：PDF、Word (DOCX)、純文字 (TXT) 等
- 🖼️ 圖片檔案：JPG、PNG 等（可以分析圖片內容！）
- 🔄 自動上傳並管理檔案

### 🧠 AI 智能問答
- 使用 Google Gemini 2.5 Flash 模型
- 基於你上傳的文件內容回答問題
- 支援繁體中文、英文等多語言

### 👥 多人協作支援
- **1 對 1 聊天**：每個人有自己的文件庫（隔離的）
- **群組聊天**：群組成員共享文件庫（大家都能查詢）
- 自動識別對話類型，無需手動設定

### 🚀 部署簡單
- 支援 Docker 容器化部署
- 可部署到 Google Cloud Run
- 或在本地開發測試

## 📸 使用範例

```
👤 你: [上傳一份會議記錄.pdf]
🤖 Bot: ✅ 檔案已成功上傳！
       檔案名稱：會議記錄.pdf

       現在您可以詢問我關於這個檔案的任何問題。

👤 你: 這次會議的主要決議是什麼？
🤖 Bot: 根據會議記錄，主要決議包括：
       1. 下季度預算增加 15%
       2. 新產品預計 6 月上市
       3. 人力資源部門將擴編 3 名員工
       ...
```

## 🛠️ 技術架構

- **Python 3.9+**
- **FastAPI** - 高效能異步 Web 框架
- **LINE Messaging API** - LINE Bot 介面
- **Google Gemini API** - 文件搜尋與 AI 問答
- **Docker** - 容器化部署

## 📦 快速開始

### 1️⃣ 環境準備

首先，你需要準備這些：

**LINE Bot 設定**
1. 到 [LINE Developers Console](https://developers.line.biz/console/) 建立一個 Messaging API channel
2. 取得你的 `Channel Secret` 和 `Channel Access Token`

**Google Gemini API**
1. 到 [Google AI Studio](https://aistudio.google.com/app/apikey) 建立 API Key
2. 複製你的 `API Key`

### 2️⃣ 下載專案

```bash
git clone <你的 repo URL>
cd linebot-file-search-adk
```

### 3️⃣ 安裝套件

```bash
pip install -r requirements.txt
```

### 4️⃣ 設定環境變數

建立 `.env` 檔案或直接設定環境變數：

```bash
export ChannelSecret="你的 LINE Channel Secret"
export ChannelAccessToken="你的 LINE Channel Access Token"
export GOOGLE_API_KEY="你的 Google Gemini API Key"
```

### 5️⃣ 啟動服務

```bash
uvicorn main:app --reload
```

服務會在 `http://localhost:8000` 啟動

### 6️⃣ 設定 Webhook

如果在本地開發，使用 ngrok 來建立公開的網址：

```bash
ngrok http 8000
```

然後到 LINE Developers Console，把 Webhook URL 設定為：
```
https://你的-ngrok-網址.ngrok.io/
```

## 🎮 使用方式

### 📤 上傳檔案

1. 直接在 LINE 聊天室傳送檔案或圖片
2. Bot 會回覆「正在處理您的檔案，請稍候...」
3. 上傳完成後會顯示「✅ 檔案已成功上傳！」

### 💬 開始提問

上傳檔案後，你可以問任何相關問題：

- 「這份文件的重點是什麼？」
- 「幫我整理成條列式」
- 「第三章在講什麼？」
- 「這張圖片裡有哪些物品？」
- 「根據這份報告，我們應該注意什麼？」

### 📁 檔案管理方式

- **個人聊天**：每個人有獨立的文件庫，只能查詢自己上傳的檔案
- **群組聊天**：所有群組成員共享同一個文件庫，任何人上傳的檔案都能被查詢

## 🐳 Docker 部署

### 建立映像檔

```bash
docker build -t linebot-file-search .
```

### 啟動容器

```bash
docker run -p 8000:8000 \
  -e ChannelSecret=你的SECRET \
  -e ChannelAccessToken=你的TOKEN \
  -e GOOGLE_API_KEY=你的API_KEY \
  linebot-file-search
```

## ☁️ 部署到 Google Cloud Run

### 步驟 1：安裝 Google Cloud SDK

參考[官方文件](https://cloud.google.com/sdk/docs/install)安裝

### 步驟 2：登入並設定專案

```bash
gcloud auth login
gcloud config set project 你的專案ID
```

### 步驟 3：建立並上傳 Docker 映像

```bash
gcloud builds submit --tag gcr.io/你的專案ID/linebot-file-search
```

### 步驟 4：部署到 Cloud Run

```bash
gcloud run deploy linebot-file-search \
  --image gcr.io/你的專案ID/linebot-file-search \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars ChannelSecret=你的SECRET,ChannelAccessToken=你的TOKEN,GOOGLE_API_KEY=你的API_KEY
```

### 步驟 5：取得服務網址

```bash
gcloud run services describe linebot-file-search \
  --platform managed \
  --region asia-east1 \
  --format 'value(status.url)'
```

把這個網址設定到 LINE Bot 的 Webhook URL 就完成了！

## 🔒 安全性建議

**不要把敏感資訊寫進程式碼！** 建議使用 Google Secret Manager：

```bash
# 建立 secrets
echo -n "你的SECRET" | gcloud secrets create line-channel-secret --data-file=-
echo -n "你的TOKEN" | gcloud secrets create line-channel-token --data-file=-
echo -n "你的API_KEY" | gcloud secrets create google-api-key --data-file=-
```

部署時使用 secrets：

```bash
gcloud run deploy linebot-file-search \
  --image gcr.io/你的專案ID/linebot-file-search \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --update-secrets=ChannelSecret=line-channel-secret:latest,ChannelAccessToken=line-channel-token:latest,GOOGLE_API_KEY=google-api-key:latest
```

## 📊 監控與除錯

部署後可以透過 Google Cloud Console 監控：

### 查看 Logs

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=linebot-file-search" --limit 50
```

### 檢查服務狀態

直接到 [Cloud Run Console](https://console.cloud.google.com/run) 查看服務狀態、錯誤率、回應時間等指標

## 💡 使用小技巧

1. **上傳多份文件**：可以連續上傳多份文件，Bot 會記住所有文件並在查詢時搜尋
2. **重新開始**：想清空文件庫？目前檔案會持續儲存在 Gemini 後端，建議用不同的對話
3. **支援的檔案類型**：取決於 Google Gemini File API 的支援，大部分常見格式都可以

## 🤔 常見問題

**Q: 為什麼我問問題時 Bot 說「您還沒有上傳任何檔案」？**
A: 請先上傳至少一個檔案或圖片，Bot 才能根據內容回答問題。

**Q: 群組聊天中，其他人上傳的檔案我也能查詢嗎？**
A: 可以！群組中所有成員共享同一個文件庫。

**Q: 檔案會保存多久？**
A: 檔案會持續保存在 Google Gemini 的後端，除非手動刪除或 store 過期。

**Q: 支援哪些語言？**
A: Google Gemini 支援多種語言，包括繁體中文、簡體中文、英文、日文等。

**Q: 可以處理多大的檔案？**
A: 取決於 Google Gemini File API 的限制，一般文件都沒問題。

## 🔧 進階設定

### 修改 AI 模型

在 `main.py` 第 71 行可以修改使用的模型：

```python
MODEL_NAME = "gemini-2.5-flash"  # 可改成其他 Gemini 模型
```

### 調整回應溫度

在 `main.py` 第 177 行可以調整 AI 的創意程度：

```python
temperature=0.7,  # 0.0 = 保守精確, 1.0 = 創意發散
```

## 📝 授權條款

MIT License - 歡迎自由使用、修改、分享！

## 🙌 貢獻

歡迎提交 Issue 或 Pull Request！

## 📚 相關連結

- [Google Gemini File Search 官方文件](https://ai.google.dev/gemini-api/docs/file-search?hl=zh-tw)
- [LINE Messaging API 文件](https://developers.line.biz/en/docs/messaging-api/)
- [FastAPI 文件](https://fastapi.tiangolo.com/)

---

⭐ 如果這個專案對你有幫助，請給個 Star 支持一下！
