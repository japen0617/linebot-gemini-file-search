# LINE Group 使用指南

本文件說明 LINE Bot 在 Group 和 Room 中的特殊行為和使用規則。

## 🎯 功能概述

### 1. Mention 機制（@提及機器人）

在 LINE Group 或 Room 中，機器人**只會**在以下情況回覆：

- ✅ **1對1聊天**：所有訊息都會回覆
- ✅ **Group/Room + Mention**：訊息中提及（@）機器人時才回覆
- ❌ **Group/Room 無 Mention**：不會回覆

### 2. 回覆目標正確性

- ✅ **Group 上傳檔案**：回覆訊息會發送到 Group
- ✅ **1對1 上傳檔案**：回覆訊息會發送到個人聊天
- ✅ **圖片分析**：回覆會發送到正確的對話（Group 或個人）

## 📝 技術實作

### 核心函數

#### 1. `is_bot_mentioned(event: MessageEvent) -> bool`

檢查機器人是否被提及，決定是否要回覆訊息。

**邏輯**：
```python
def is_bot_mentioned(event: MessageEvent) -> bool:
    """
    Check if the bot is mentioned in a group/room message.
    Returns True for 1-on-1 chat, or if bot is mentioned in group/room.
    """
    # In 1-on-1 chat, always respond
    if event.source.type == "user":
        return True

    # In group/room, check if bot is mentioned
    if hasattr(event.message, 'mention') and event.message.mention:
        mentionees = event.message.mention.mentionees
        for mentionee in mentionees:
            # Check if this mention is for the bot
            if (hasattr(mentionee, 'isSelf') and mentionee.isSelf) or \
               (hasattr(mentionee, 'type') and mentionee.type == "user" and
                hasattr(mentionee, 'isSelf') and mentionee.isSelf):
                return True

    return False
```

**檢查重點**：
- `mention.mentionees[].type` = "user"
- `mention.mentionees[].isSelf` = True
- 這表示提及的是機器人本身

#### 2. `get_reply_target(event: MessageEvent) -> str`

獲取正確的回覆目標 ID。

**邏輯**：
```python
def get_reply_target(event: MessageEvent) -> str:
    """
    Get the correct reply target ID based on the message source.
    Returns group_id for group chat, user_id for 1-on-1 chat.
    """
    if event.source.type == "group":
        return event.source.group_id
    elif event.source.type == "room":
        return event.source.room_id
    else:
        return event.source.user_id
```

**用途**：
- 在 `push_message` 時使用，確保訊息發送到正確的對話
- Group 上傳檔案 → 回覆到 Group
- 1對1 上傳檔案 → 回覆到個人

### 應用場景

#### 場景 1: 文字訊息處理

```python
async def handle_text_message(event: MessageEvent, message):
    # ⭐ 關鍵檢查：Group 中沒被 mention 就不回覆
    if not is_bot_mentioned(event):
        print(f"Bot not mentioned in group/room, skipping response")
        return

    # 繼續處理訊息...
    store_name = get_store_name(event)
    query = message.text
    # ...
```

**效果**：
- Group 中有人說「今天天氣真好」→ 機器人不回覆 ✅
- Group 中有人說「@bot 今天天氣如何？」→ 機器人回覆 ✅

#### 場景 2: 檔案上傳處理

```python
async def handle_document_message(event: MessageEvent, message: FileMessage):
    store_name = get_store_name(event)
    # ⭐ 關鍵修改：使用正確的回覆目標
    reply_target = get_reply_target(event)

    # ... 上傳檔案處理 ...

    # ✅ 發送到正確的對話（Group 或個人）
    success_msg = TextSendMessage(text="✅ 檔案已成功上傳！...")
    await line_bot_api.push_message(reply_target, success_msg)
```

**效果**：
- Group 中上傳檔案 → 成功訊息回到 Group ✅
- 1對1 上傳檔案 → 成功訊息回到個人聊天 ✅

#### 場景 3: 圖片分析處理

```python
async def handle_image_message(event: MessageEvent, message: ImageMessage):
    # ⭐ 使用正確的回覆目標
    reply_target = get_reply_target(event)

    # ... 圖片分析處理 ...

    # ✅ 發送到正確的對話
    result_msg = TextSendMessage(text=f"📸 圖片分析結果：\n\n{analysis_result}")
    await line_bot_api.push_message(reply_target, result_msg)
```

## 🧪 測試驗證

執行測試腳本驗證邏輯：

```bash
python3 test_group_mention.py
```

**測試案例**：
- ✅ Test 1: 1對1 聊天（應該回覆）
- ✅ Test 2: Group 無 mention（不應回覆）
- ✅ Test 3: Group 有 mention（應該回覆，且回到 Group）
- ✅ Test 4: Group 提及其他人（不應回覆）
- ✅ Test 5: Room 有 mention（應該回覆，且回到 Room）

## 📊 使用範例

### 範例 1: Group 查詢文件

**情境**：在 Group 中查詢已上傳的文件

```
用戶 A: 大家好！
機器人: （不回覆）

用戶 B: @bot 這份報告的主要結論是什麼？
機器人: 根據文件內容，主要結論有三點：
        1. 專案預算控制在目標範圍內
        2. 完成率達到 95%
        ...
        📖 引用1  📖 引用2
```

### 範例 2: Group 上傳檔案

**情境**：在 Group 中上傳文件檔案

```
用戶 A: [上傳 meeting_notes.pdf]
機器人: 正在處理您的檔案，請稍候...
機器人: ✅ 檔案已成功上傳！
        檔案名稱：meeting_notes.pdf

        現在您可以詢問我關於這個檔案的任何問題。
        📝 生成檔案摘要  📌 重點整理  📋 列出檔案
```

**✅ 成功訊息會出現在 Group 中，所有成員都看得到**

### 範例 3: Group 列出檔案

**情境**：在 Group 中列出已上傳的檔案

```
用戶 B: @bot 列出檔案
機器人: 我看到這個群組已經上傳了 3 個檔案唷！

        首先是「會議記錄.pdf」，這是在 1月8日下午2點半上傳的。
        接著是「技術文件.docx」，是在下午3點20分傳的。
        最後一個是「報告.txt」，這個是在下午4點10分上傳的。

        需要我幫你查詢哪個檔案的內容呢？😊
```

## 🔑 關鍵差異對比

| 功能 | 修改前 ❌ | 修改後 ✅ |
|------|----------|----------|
| **Group 文字訊息** | 每句話都回覆 | 只在被 mention 時回覆 |
| **Group 檔案上傳** | 成功訊息發到私訊 | 成功訊息發到 Group |
| **Group 圖片分析** | 結果發到私訊 | 結果發到 Group |
| **1對1 聊天** | 正常回覆 | 正常回覆（無影響）|

## ⚠️ 注意事項

### 1. Mention 格式

在 LINE Group 中提及機器人的方式：
- 使用 `@` 符號選擇機器人
- 或直接在訊息中輸入機器人名稱並選擇

### 2. 檔案上傳不需要 Mention

- **檔案上傳**、**圖片上傳** 等媒體訊息**不需要** mention
- 機器人會自動處理所有上傳的檔案和圖片
- 但**查詢文件內容**時需要 mention

### 3. Quick Reply 在 Group 中的使用

- Quick Reply 按鈕會顯示給所有 Group 成員
- 點擊 Quick Reply 會自動帶入問題
- **但仍需要 mention 機器人**才會回覆

**建議做法**：
```
點擊 Quick Reply「📝 生成檔案摘要」後：
→ 自動帶入：「請幫我生成「檔案.pdf」這個檔案的摘要」
→ 但還是要手動加上 @bot

正確用法：
@bot 請幫我生成「檔案.pdf」這個檔案的摘要
```

### 4. Store 隔離機制

- **1對1 聊天**：每個使用者有獨立的 File Search Store（`user_U123456`）
- **Group 聊天**：所有 Group 成員共享同一個 Store（`group_G123456`）
- **Room 聊天**：所有 Room 成員共享同一個 Store（`room_R123456`）

**隱私考量**：
- Group 中上傳的文件，所有 Group 成員都可以查詢
- 如果需要私密查詢，請在 1對1 聊天中上傳文件

## 🚀 更新日誌

### 2025-11-11
- ✅ 新增 `is_bot_mentioned()` 函數檢查 mention
- ✅ 新增 `get_reply_target()` 函數獲取正確回覆目標
- ✅ 修復 `handle_text_message()` 在 Group 中的回覆邏輯
- ✅ 修復 `handle_document_message()` 檔案上傳回覆目標
- ✅ 修復 `handle_image_message()` 圖片分析回覆目標
- ✅ 新增測試腳本 `test_group_mention.py` 驗證邏輯

## 📚 相關資源

- [LINE Messaging API - Mention Object](https://developers.line.biz/en/reference/messaging-api/#mention-object)
- [LINE Bot SDK for Python](https://github.com/line/line-bot-sdk-python)
- [專案 GitHub Repository](https://github.com/kkdai/linebot-file-search-adk)
