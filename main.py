import argparse
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError
from urllib.error import URLError
import socket
import sys

# URL = 'https://www.youtube.com/watch?v=_v4CpSsHpZQ'
# options = {
#     'format': 'bestaudio/best',
# }

# with yt_dlp.YoutubeDL(options) as ydl:
#     ydl.download([URL])

# ARGS PARSER
parser = argparse.ArgumentParser()

parser.add_argument("url", type=str, help="url-адрес YouTube-видео.")
parser.add_argument("-a", "--audio", action="store_true", help="Скачать только аудио вариант видео (без картинки).")

args = parser.parse_args()
# ===========

# YT-DLP SETTINGS
options = {
    'outtmpl': '%(title)s.%(ext)s',
    'quiet': True,
}

if args.audio:
    options['format'] = 'bestaudio/best'
else:
    options['format'] = 'best'
# ===============

# TRY
try:
    with yt_dlp.YoutubeDL(options) as ydl:
        print(f"Начинаю загрузку {args.url}")
        ydl.download([args.url])
        print("Готово! <3")

except URLError:
    print("Ошибка сети: проверь подключение к интернету или VPN.")
except DownloadError:
    print("Не удалось скачать видео. Возможно, оно удалено, приватное или не существует.")
except ExtractorError:
    print("Ошибка при извлечении информации о видео. Проверь ссылку или доступность YouTube.")
except Exception as e:
    print(f"Неизвестная ошибка: {e}")
# ===