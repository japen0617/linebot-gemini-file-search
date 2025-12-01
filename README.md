### 📁 Vercel 環境檔案格式支援

由於 Vercel Serverless 環境的限制（無法安裝 LibreOffice），檔案格式支援與 Docker/Cloud Run 部署有所不同：

#### ✅ 完整支援的格式

| 格式 | 副檔名 | 說明 |
|------|--------|------|
| PDF | `.pdf` | ✅ 完整支援 |
| Word (新版) | `.docx` | ✅ 完整支援 |
| PowerPoint (新版) | `.pptx` | ✅ 完整支援 |
| 純文字 | `.txt` | ✅ 完整支援 |
| Markdown | `.md` | ✅ 完整支援 |
| HTML | `.html`, `.htm` | ✅ 完整支援 |
| CSV | `.csv` | ✅ 完整支援 |
| XML | `.xml` | ✅ 完整支援 |
| RTF | `.rtf` | ✅ 完整支援 |

#### ⚠️ 需要手動轉換的格式

| 格式 | 副檔名 | Vercel 環境 | 解決方案 |
|------|--------|-------------|----------|
| Word (舊版) | `.doc` | ❌ 無法自動轉換 | 請先用 Microsoft Word 另存為 `.docx` |
| PowerPoint (舊版) | `.ppt` | ❌ 無法自動轉換 | 請先用 PowerPoint 另存為 `.pptx` |

#### 💡 為什麼有這個限制？

- **Docker / Cloud Run 部署**：可以安裝 LibreOffice，支援 `.doc` → `.docx` 和 `.ppt` → `.pptx` 自動轉換
- **Vercel Serverless 部署**：無法安裝系統套件（如 LibreOffice），因此舊版格式需要手動轉換

> 📝 **建議**：如果經常需要處理 `.doc` 或 `.ppt` 檔案，建議使用 Docker 部署到 Google Cloud Run 或其他支援 Docker 的平台。

---

## 🤔 常見問題

### Vercel 部署

**Q: 為什麼在 Vercel 上無法上傳 .doc 或 .ppt 檔案？**
A: Vercel Serverless 環境無法安裝 LibreOffice，因此無法自動轉換舊版 Office 格式。請先使用 Microsoft Office 將檔案另存為新版格式（.docx 或 .pptx）後再上傳。

**Q: Vercel 和 Docker 部署有什麼差異？**
A: 
- **Vercel**：部署簡單、自動擴展、免費額度，但不支援 .doc/.ppt 自動轉換
- **Docker (Cloud Run)**：完整功能支援，包括 .doc/.ppt 自動轉換，但需要設定較多

**Q: 如何選擇部署方式？**
A: 
- 如果主要使用 PDF、DOCX、PPTX 等新版格式 → 選擇 **Vercel**（簡單快速）
- 如果需要支援 .doc/.ppt 舊版格式 → 選擇 **Docker + Cloud Run**（完整功能）
