### 📄 Vercel 檔案格式支援

由於 Vercel Serverless 環境的限制（無法安裝 LibreOffice），支援的檔案格式與 Docker/Heroku 部署略有不同：

| 格式 | Vercel | Docker/Heroku | 說明 |
|------|--------|---------------|------|
| **.docx** | ✅ 支援 | ✅ 支援 | Word 文件 |
| **.pdf** | ✅ 支援 | ✅ 支援 | PDF 文件 |
| **.txt** | ✅ 支援 | ✅ 支援 | 純文字 |
| **.md** | ✅ 支援 | ✅ 支援 | Markdown |
| **.html/.htm** | ✅ 支援 | ✅ 支援 | HTML 網頁 |
| **.csv** | ✅ 支援 | ✅ 支援 | CSV 表格 |
| **.xml** | ✅ 支援 | ✅ 支援 | XML 文件 |
| **.rtf** | ✅ 支援 | ✅ 支援 | RTF 文件 |
| **.pptx** | ✅ 支援 | ✅ 支援 | PowerPoint 簡報 |
| **.doc** | ⚠️ 需手動轉換 | ✅ 自動轉換 | 舊版 Word（請先轉為 .docx） |
| **.ppt** | ⚠️ 需手動轉換 | ✅ 自動轉換 | 舊版 PowerPoint（請先轉為 .pptx） |

> 💡 **Vercel 使用者提示**：
> - 如果您有 .doc 或 .ppt 檔案，請先使用 Microsoft Office 或 Google Docs 將其另存為 .docx 或 .pptx 格式後再上傳
> - Vercel 環境無法安裝 LibreOffice，因此無法自動轉換舊版格式
> - 其他格式（.docx、.pdf、.pptx 等）在 Vercel 上完全正常運作
