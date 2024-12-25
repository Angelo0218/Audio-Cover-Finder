# 音樂封面自動下載器 (Audio-Cover-Finder)

這是一款支援多格式音樂檔案的封面自動下載工具。它會自動從 YouTube 搜尋相關的影片縮圖作為音樂封面，並將其嵌入音樂檔案。

## 特色功能

✨ 自動搜尋 YouTube 獲取封面圖片  
✨ 支援批次處理整個資料夾的音樂檔案  
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

2. 把音樂m4a放入./music資料夾
```

3. 執行程式：
```bash
python m4a-cover-finder.py
```

## 建議的完整工作流程


使用 Open Video Downloader 下載音樂。
使用 EZ CD Audio Converter 將音檔轉換為所需格式（如 M4A）。
使用本工具自動下載並嵌入封面。

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

### v1.0.1

🎵 新增格式支援：現在支援 M4A、MP3、FLAC、OPUS、OGG、WAV 和 AAC。

📸 圖片處理強化：自動裁剪為正方形，適合作為專輯封面。

🔄 自動更新功能：自動更新搜尋邏輯和錯誤修復。

⚡ 多執行緒處理：進一步提升批次處理效率。
