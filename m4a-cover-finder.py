import os
import requests
from mutagen.mp4 import MP4, MP4Cover
from yt_dlp import YoutubeDL
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import uuid

# 搜尋 YouTube 並下載封面圖片 URL
def search_youtube_cover(query):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': False,
        'writethumbnail': True,
        'outtmpl': f"cover_{uuid.uuid4().hex}.%(ext)s",
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' in result and result['entries']:
                video = result['entries'][0]
                if 'thumbnail' in video:
                    return video['thumbnail']
        except Exception as e:
            print(f"YouTube search failed: {e}")
    return None

# 下載並轉換圖片為 JPEG 格式
def download_and_convert_image(image_url, save_path):
    temp_path = save_path + f"_{uuid.uuid4().hex}.tmp"
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(temp_path, 'wb') as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            with Image.open(temp_path) as img:
                img = img.convert("RGB")  # 確保圖片為 RGB 格式
                img.save(save_path, format='JPEG')
            os.remove(temp_path)
            return True
    except Exception as e:
        print(f"Error downloading or converting image: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    return False

# 將圖片裁剪為正方形
def crop_to_square(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            img_cropped = img.crop((left, top, right, bottom))
            img_cropped.save(image_path, format='JPEG')
    except Exception as e:
        print(f"Error cropping image: {e}")

# 嵌入專輯圖片到音樂檔案
def embed_cover_image(audio_file, cover_path):
    try:
        audio = MP4(audio_file)
        if cover_path and os.path.exists(cover_path):
            with open(cover_path, 'rb') as f:
                cover_data = f.read()
                audio["covr"] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]
        audio.save()
    except Exception as e:
        print(f"Error embedding cover image: {e}")

# 檢測檔案是否已有封面
def has_cover_image(audio_file):
    try:
        audio = MP4(audio_file)
        return "covr" in audio
    except Exception as e:
        print(f"Error checking cover for {audio_file}: {e}")
        return False

# 使用 metadata 搜尋封面並嵌入
def process_audio_file(audio_file, directory, missing_cover_files):
    if has_cover_image(audio_file):
        print(f"File already has cover: {audio_file}")
        return

    try:
        audio = MP4(audio_file)
        title = audio.tags.get("\xa9nam", ["Unknown Title"])[0]
        artist = audio.tags.get("\xa9ART", ["Unknown Artist"])[0]
        album = audio.tags.get("\xa9alb", [""])[0]

        query = f"{title} {artist}" if not album else f"{title} {artist} {album}"
        print(f"Searching for cover: {query}")

        # 搜尋封面圖片
        image_url = search_youtube_cover(query)
        if image_url:
            print(f"Found image: {image_url}")
            cover_path = f'cover_{uuid.uuid4().hex}.jpg'
            if download_and_convert_image(image_url, cover_path):
                crop_to_square(cover_path)
                embed_cover_image(audio_file, cover_path)
                os.remove(cover_path)
                print(f"Cover embedded for {audio_file}")
            else:
                print("Failed to download or process cover image.")
        else:
            print(f"No image found for {audio_file}.")
            missing_cover_files.append(audio_file)
    except Exception as e:
        print(f"Error processing file {audio_file}: {e}")
        missing_cover_files.append(audio_file)

# 處理資料夾中的所有音樂檔案
def process_directory(directory):
    missing_cover_files = []

    def worker(file):
        if file.endswith('.m4a'):
            process_audio_file(os.path.join(directory, file), directory, missing_cover_files)

    files = os.listdir(directory)
    with ThreadPoolExecutor() as executor:
        executor.map(worker, files)

    print("\n=== Summary ===")
    print(f"Total files without cover: {len(missing_cover_files)}")
    if missing_cover_files:
        print("Files without cover:")
        for file in missing_cover_files:
            print(f" - {file}")

# 主程式
audio_folder = r"C:\Users\Angelo\桌面\music img"
process_directory(audio_folder)
