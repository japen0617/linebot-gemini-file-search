# Vercel 部署指南 🚀

本文件說明如何將 LINE Bot + Gemini AI 專案部署到 Vercel 平台。

## 📋 目錄

- [環境變數設定](#環境變數設定)
- [部署步驟](#部署步驟)
- [Vercel 平台限制](#vercel-平台限制)
- [故障排除](#故障排除)

## 環境變數設定

### 必要的環境變數

在 Vercel 中部署此專案需要設定以下環境變數：

| 變數名稱 | 說明 | 必填 |
|---------|------|------|
| `ChannelSecret` | LINE Bot Channel Secret | ✅ |
| `ChannelAccessToken` | LINE Bot Channel Access Token | ✅ |
| `GOOGLE_API_KEY` | Google Gemini API Key | ✅ |

### 取得環境變數值

**LINE Bot 設定：**
1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇或建立一個 Messaging API channel
3. 在 Basic settings 頁面取得 `Channel Secret`
4. 在 Messaging API 頁面取得 `Channel Access Token`

**Google Gemini API Key：**
1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 建立或取得 API Key

### ⚠️ 環境變數注意事項

- **不要將敏感資訊提交到版本控制**：確保 `.env` 檔案已加入 `.gitignore`
- **在 Vercel Dashboard 中設定環境變數**：不要在程式碼中硬編碼 API Keys
- **區分環境**：可以為 Production、Preview、Development 設定不同的變數
- **名稱大小寫**：環境變數名稱區分大小寫，請確保完全一致

## 部署步驟

### 步驟 1：準備 GitHub 儲存庫

確保您的專案已推送到 GitHub 儲存庫，並包含以下檔案：
- `vercel.json` - Vercel 配置檔
- `api/index.py` - Serverless Function 入口點
- `main.py` - FastAPI 主應用
- `requirements.txt` - Python 依賴

### 步驟 2：連接 Vercel

1. 前往 [Vercel](https://vercel.com/) 並登入（可使用 GitHub 帳號）
2. 點擊 "Add New..." → "Project"
3. 選擇 "Import Git Repository"
4. 授權 Vercel 存取您的 GitHub 儲存庫
5. 選擇要部署的儲存庫

### 步驟 3：設定環境變數

在 Vercel 專案設定頁面：
1. 展開 "Environment Variables" 區段
2. 新增以下環境變數：
   - `ChannelSecret` = 您的 LINE Channel Secret
   - `ChannelAccessToken` = 您的 LINE Channel Access Token
   - `GOOGLE_API_KEY` = 您的 Google Gemini API Key
3. 選擇要套用的環境（建議全選：Production、Preview、Development）

### 步驟 4：部署專案

1. 點擊 "Deploy" 按鈕
2. 等待部署完成（通常需要 1-3 分鐘）
3. 部署完成後，您會獲得一個專案 URL（例如：`https://your-project.vercel.app`）

### 步驟 5：更新 LINE Bot Webhook URL

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇您的 Messaging API channel
3. 在 "Messaging API" 頁面找到 "Webhook settings"
4. 將 Webhook URL 設定為：`https://your-project.vercel.app/`
5. 確認 "Use webhook" 已開啟
6. 點擊 "Verify" 按鈕測試連線

### 步驟 6：驗證部署

1. 開啟 LINE 應用程式
2. 加入您的 LINE Bot 好友
3. 傳送一則測試訊息
4. 確認 Bot 有正確回應

## Vercel 平台限制

### ⏱️ 執行時間限制

| 方案 | 最大執行時間 |
|-----|-------------|
| Hobby（免費） | 10 秒 |
| Pro | 60 秒 |
| Enterprise | 900 秒 |

**影響說明：**
- 大型檔案上傳可能會超時（特別是 Hobby 方案）
- 複雜的 AI 查詢可能需要較長時間
- 建議使用 Pro 方案以獲得更好的體驗

### 📁 檔案系統限制

- Vercel Serverless Functions 的檔案系統為**唯讀**
- 只有 `/tmp` 目錄可以寫入
- `/tmp` 目錄容量限制為 512MB
- 函數執行結束後 `/tmp` 內容會被清除

**對本專案的影響：**
- 檔案上傳功能可能受限
- 目前程式使用 `uploads/` 目錄暫存檔案，在 Vercel 環境中可能需要調整
- 建議使用雲端儲存（如 Google Cloud Storage）處理大型檔案

### 🥶 Cold Start

- 如果函數長時間未使用，首次呼叫會有延遲（Cold Start）
- Cold Start 時間通常為 1-3 秒
- 可透過定期呼叫來保持函數「熱」狀態

### 📦 部署大小限制

- 未壓縮：250MB
- 壓縮後：50MB
- 確保 `requirements.txt` 不包含不必要的大型套件

## 故障排除

### 常見問題

**Q: 部署失敗，顯示 "Build failed"**
A: 檢查以下項目：
- `requirements.txt` 中的套件版本是否相容
- 是否有語法錯誤
- 查看 Vercel 的 Build Logs 獲取詳細錯誤訊息

**Q: Webhook 驗證失敗**
A: 確認：
- 環境變數設定正確
- Webhook URL 格式正確（結尾需要 `/`）
- 等待幾秒後重試（可能是 Cold Start 造成的延遲）

**Q: Bot 沒有回應**
A: 檢查：
- Vercel 的 Function Logs 是否有錯誤訊息
- LINE Bot 的 Webhook 是否已開啟
- 環境變數是否設定正確

**Q: 檔案上傳失敗**
A: 由於 Vercel 的檔案系統限制：
- 確認檔案大小在限制範圍內
- 檢查是否有超時問題（Hobby 方案只有 10 秒）
- 考慮升級到 Pro 方案

### 查看日誌

1. 前往 Vercel Dashboard
2. 選擇您的專案
3. 點擊 "Deployments" 查看部署歷史
4. 點擊 "Functions" 查看 Serverless Function 日誌
5. 使用 "Logs" 頁面即時監控

### 重新部署

如果需要重新部署：
1. 推送新的 commit 到 GitHub（自動觸發部署）
2. 或在 Vercel Dashboard 點擊 "Redeploy"

## 與其他部署方式比較

| 特性 | Vercel | Docker | Heroku |
|-----|--------|--------|--------|
| 設定複雜度 | 低 | 中 | 低 |
| 免費方案 | ✅ | 需自行架設 | ✅（有限制）|
| 執行時間限制 | 10-900秒 | 無限制 | 30秒 |
| 檔案系統 | 唯讀（僅 /tmp 可寫） | 可讀寫 | 臨時檔案系統 |
| 自動擴展 | ✅ | 需自行設定 | ✅ |
| 自訂域名 | ✅ | 需自行設定 | ✅ |

## 相關資源

- [Vercel 官方文件](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
- [FastAPI on Vercel](https://vercel.com/templates/python/fastapi)
- [LINE Developers Console](https://developers.line.biz/console/)
- [Google AI Studio](https://aistudio.google.com/)
