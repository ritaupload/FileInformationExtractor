import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
try :
    from moviepy.editor import VideoFileClip
except :
    os.system("pip install moviepy")
    quit()

def is_video_file(file_path):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mpeg', '.mpg', '.webm']
    _, extension = os.path.splitext(file_path)
    return extension.lower() in video_extensions

def seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), int(seconds)

def get_video_duration(file_path):
    try:
        video_clip = VideoFileClip(file_path)
        duration_seconds = video_clip.duration
        return duration_seconds
    except Exception as e:
        print(f"영상 파일 '{file_path}'의 재생 시간을 얻는 중 오류 발생: {e}")

def convert_bytes_to_human_readable(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0

def list_files_and_folders(folder_path):
    global total_size, total_file, total_duration, total_video
    real_path = folder_path
    video = []
    etc = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            size_human_readable = convert_bytes_to_human_readable(size)
            total_size += size
            relative_path = file_path.replace(f"{real_path}\\", "")
            data = f"{relative_path}, 크기 : {size_human_readable}"
            if is_video_file(file_path):
                duration = get_video_duration(file_path)
                duration_hms = seconds_to_hms(duration)
                total_duration += duration
                total_video += 1
                data += f", 시간 : {duration_hms[0]:02d}:{duration_hms[1]:02d}:{duration_hms[2]:02d}"
                video.append(data)
            else:
                etc.append(data)

            total_file += 1
    return video, etc


def update_textbox():
    global total_size, total_file, total_duration, total_video
    folder_path = folder_var.get().replace("\"", "")

    video, etc = list_files_and_folders(folder_path)
    total_size = convert_bytes_to_human_readable(total_size)
    duration_hms = seconds_to_hms(total_duration)

    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)

    result_text.insert(tk.END, f"  - 영상 파일 {total_video}개\n")
    for v in video:
        result_text.insert(tk.END, v + "\n")
    result_text.insert(tk.END, f"\n  - 기타 파일 {total_file - total_video}개\n")
    for e in etc:
        result_text.insert(tk.END, e + "\n")
    result_text.insert(tk.END, f"\n총 {total_file}개의 파일\n\n  - 용량 : {total_size}\n\n  - 시간 : {duration_hms[0]:02d}:{duration_hms[1]:02d}:{duration_hms[2]:02d}\n")
    
    result_text.config(state=tk.DISABLED)
    total_file = 0
    total_video = 0
    total_size = 0
    total_duration = 0

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)
        update_textbox()


total_file = 0
total_video = 0
total_size = 0
total_duration = 0

root = tk.Tk()
root.title("간단 정보 추출기")

folder_var = tk.StringVar()

tk.Label(root, text="폴더 경로:").pack(pady=5)
tk.Entry(root, textvariable=folder_var, width=40).pack(pady=5)
tk.Button(root, text="찾아보기", command=browse_folder).pack(pady=5)
tk.Button(root, text="정보출력", command=update_textbox).pack(pady=10)

result_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack(pady=10)

root.mainloop()