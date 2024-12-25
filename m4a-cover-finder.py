import os
import requests
import mutagen  # Ensure mutagen is imported
from mutagen import File
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import ID3, APIC
from mutagen.flac import Picture
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
        'ignoreerrors': True,  # 確保自動更新和錯誤忽略
        'force_generic_extractor': False,  # Update to ensure ytsearch works as intended
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
                img = crop_to_square(img)  # 裁剪為正方形
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
def crop_to_square(image):
    try:
        width, height = image.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        return image.crop((left, top, right, bottom))
    except Exception as e:
        print(f"Error cropping image: {e}")
        return image

# 嵌入專輯圖片到音樂檔案
def embed_cover_image(audio_file, cover_path):
    try:
        audio = File(audio_file, easy=False)
        with open(cover_path, 'rb') as img_file:
            cover_data = img_file.read()

        if isinstance(audio, MP4):
            audio["covr"] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]
        elif audio and audio.tags and isinstance(audio.tags, ID3):
            audio.tags.add(
                APIC(
                    encoding=3,  # UTF-8
                    mime='image/jpeg',
                    type=3,  # Cover front
                    desc='Cover',
                    data=cover_data
                )
            )
        elif audio and isinstance(audio, mutagen.flac.FLAC):
            picture = Picture()
            picture.data = cover_data
            picture.type = 3  # Cover front
            picture.mime = 'image/jpeg'
            audio.add_picture(picture)

        audio.save()
    except Exception as e:
        print(f"Error embedding cover image: {e}")

# 檢測檔案是否已有封面
def has_cover_image(audio_file):
    try:
        audio = File(audio_file, easy=False)
        if isinstance(audio, MP4):
            return "covr" in audio
        elif audio and audio.tags and isinstance(audio.tags, ID3):
            return any(tag.FrameID == "APIC" for tag in audio.tags.values())
        elif isinstance(audio, mutagen.flac.FLAC):
            return any(picture.type == 3 for picture in audio.pictures)
    except Exception as e:
        print(f"Error checking cover for {audio_file}: {e}")
    return False

# 使用 metadata 搜尋封面並嵌入
def process_audio_file(audio_file, missing_cover_files):
    if has_cover_image(audio_file):
        print(f"File already has cover: {audio_file}")
        return

    try:
        audio = File(audio_file, easy=True)
        title = audio.get("title", ["Unknown Title"])[0]
        artist = audio.get("artist", ["Unknown Artist"])[0]
        album = audio.get("album", [""])[0]

        query = f"{title} {artist}" if not album else f"{title} {artist} {album}"
        print(f"Searching for cover: {query}")

        # 搜尋封面圖片
        image_url = search_youtube_cover(query)
        if image_url:
            print(f"Found image: {image_url}")
            cover_path = f'cover_{uuid.uuid4().hex}.jpg'
            if download_and_convert_image(image_url, cover_path):
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

# 處理資料夾中的所有音樂檔案，並遞迴進入子資料夾
def process_directory(directory):
    missing_cover_files = []

    def worker(file):
        if file.endswith(('.m4a', '.mp3', '.flac', '.opus', '.ogg', '.wav', '.aac')):
            process_audio_file(file, missing_cover_files)

    # 使用 os.walk 遞迴遍歷資料夾及其子資料夾
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    with ThreadPoolExecutor() as executor:
        executor.map(worker, files)

    print("\n=== Summary ===")
    print(f"Total files without cover: {len(missing_cover_files)}")
    if missing_cover_files:
        print("Files without cover:")
        for file in missing_cover_files:
            print(f" - {file}")

# 主程式
audio_folder = "./music"
process_directory(audio_folder)
