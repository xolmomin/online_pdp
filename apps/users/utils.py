import os
import subprocess

from django.conf import settings


def convert_video_to_hls(video_path, video_name, lesson_id):
    # Faqat yangi yaratilganda ishga tushsin
    if not video_path or not os.path.exists(video_path):
        return

    print(video_name)

    url = video_name.removeprefix('courses/').split('.')[0]
    print(url)

    # Har bir video uchun unikal papka (uuid asosida)
    base_dir = os.path.join(settings.MEDIA_ROOT, 'courses/hls', f"{url}/{lesson_id}")
    os.makedirs(base_dir, exist_ok=True)

    # --- Kalit yaratish ---
    key_hex = os.urandom(16).hex()
    key_file_path = os.path.join(base_dir, 'enc.key')
    with open(key_file_path, 'wb') as f:
        f.write(bytes.fromhex(key_hex))

    # 🔥 MUHIM O‘ZGARISH: `key_uri` = to‘liq URL (foydalanuvchi uchun)
    key_uri = f"http://127.0.0.1:8000/get_key/lesson/{lesson_id}/"

    # 🔥 MUHIM O‘ZGARISH: `enc.keyinfo` faylga to‘liq *fayl yo‘li* yozish
    key_info_path = os.path.join(base_dir, 'enc.keyinfo')
    with open(key_info_path, 'w') as f:
        f.write(f"{key_uri}\n{key_file_path}\n{key_hex}")

    # --- FFmpeg yordamida HLS generatsiya ---
    output_m3u8 = os.path.join(base_dir, 'master.m3u8')
    segment_pattern = os.path.join(base_dir, 'segment_%03d.ts')

    cmd = [
        'ffmpeg', '-y', '-i', video_path,
        '-c:v', 'libx264', '-c:a', 'aac',
        '-hls_time', '6',
        '-hls_playlist_type', 'vod',
        '-hls_key_info_file', key_info_path,
        '-hls_segment_filename', segment_pattern,
        output_m3u8
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise
