# M4A 音樂封面自動下載器

這是一個自動為 M4A 音樂檔案下載並嵌入封面的工具。它會自動從 YouTube 搜尋相關的影片縮圖作為音樂封面，並自動處理成適合的格式。

## 特色功能

✨ 自動搜尋 YouTube 獲取封面圖片  
✨ 支援批次處理整個資料夾的 M4A 檔案  
✨ 自動裁剪圖片為正方形  
✨ 多執行緒處理，效率更高  
✨ 自動跳過已有封面的檔案  
✨ 處理結果詳細記錄  

## 推薦工具

在使用本工具之前，建議使用以下工具準備音樂檔案：

### 下載音樂
👉 推薦使用 [Open Video Downloader](https://jely2002.github.io/youtube-dl-gui/)
- 開源、安全、操作簡單
- 支援選擇音質
- 界面友善

### 轉換格式
👉 推薦使用 [EZ CD Audio Converter](https://www.poikosoft.com/ez-cd-audio-converter)
- 可將音檔轉換為 M4A 格式
- 支援批次轉換
- 可保留音樂資訊標籤

## 使用前準備

1. 安裝 Python (建議 3.8 以上版本)
2. 安裝需要的套件：
```bash
pip install yt-dlp mutagen Pillow requests
```

## 使用方法

1. 下載程式檔案到你的電腦

2. 修改程式中的音樂資料夾路徑：
```python
audio_folder = "你的音樂資料夾路徑"
```

3. 執行程式：
```bash
python m4a-cover-finder.py
```

## 建議的完整工作流程

1. 使用 Open Video Downloader 下載音樂
2. 使用 EZ CD Audio Converter 將音檔轉換為 M4A 格式
3. 使用本工具自動下載並嵌入封面

## 注意事項

⚠️ 需要連接網路  
⚠️ 只支援 M4A 格式的音樂檔案  
⚠️ 音樂檔案建議包含完整的資訊（歌名、演出者）以提高搜尋準確度  
⚠️ 處理大量檔案可能需要一些時間  
⚠️ 轉換格式時請保留原始音樂資訊，這樣能提高封面搜尋準確度  

## 授權

MIT License

## 問題回報

如果遇到問題或有建議，歡迎在 GitHub 上開 Issue 回報！

## 更新紀錄

### v1.0.0
- 首次發布
- 支援基本的封面搜尋和嵌入功能
- 支援多執行緒處理
