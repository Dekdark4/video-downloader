import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError
from urllib.error import URLError
import threading

def download_video(url, audio_only=False):
    options = {
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
    }
    if audio_only:
        options['format'] = 'bestaudio/best'
    else:
        options['format'] = 'best'

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
            return "Готово! <3"
    except URLError:
        return "Ошибка сети: проверь интернет или VPN."
    except DownloadError:
        return "Не удалось скачать видео. Возможно, оно удалено или приватное."
    except ExtractorError:
        return "Ошибка при извлечении информации. Проверь ссылку."
    except Exception as e:
        return f"Неизвестная ошибка: {e}"
    
def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Ошибка", "Введи ссылку на видео!")
        return
    
    download_btn.config(state="disabled")
    status_label.config(text="Идёт загрузка, подожди немного.")

    def task():
        result = download_video(url, audio_var.get())
        root.after(0, lambda: update_ui(result))

    threading.Thread(
        target=task,
        daemon=True,
    ).start()

def update_ui(result):
    status_label.config(text=result)
    download_btn.config(state="normal")

def enable_ctrl_v(event):
    """Разрешает вставку по Ctrl+V."""
    event.widget.event_generate('<<Paste>>')
    
    
root = tk.Tk()
root.title("YouTube downloader")
root.geometry("500x200")
root.resizable(False, False)

tk.Label(root, text="Ссылка на YouTube-видео:").pack(pady=(15, 0))
url_entry = tk.Entry(root, width=300)
url_entry.pack(pady=10)
url_entry.bind('<Control-v>', enable_ctrl_v)

audio_var = tk.BooleanVar()
tk.Checkbutton(root, text="Только аудио", variable=audio_var).pack()

download_btn = ttk.Button(root, text="Скачать", command=start_download)
download_btn.pack(pady=20)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

root.mainloop()