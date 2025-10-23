import os
import subprocess
import threading

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Lesson


# TODO asyncio | threading orqali task yaratish

@receiver(post_save, sender=Lesson)
def convert_video_to_hls(sender, instance, created, **kwargs):
    # Faqat yangi yaratilganda ishga tushsin
    if not created or not instance.video:
        return

    input_path = instance.video.path

    # Har bir video uchun unikal papka (uuid asosida)
    base_dir = os.path.join(settings.MEDIA_ROOT, 'hls', f'lesson_{instance.id}')
    os.makedirs(base_dir, exist_ok=True)

    # --- ⃣ Kalit yaratish ---
    key_hex = os.urandom(16).hex()
    key_file_path = os.path.join(base_dir, 'enc.key')
    with open(key_file_path, 'wb') as f:
        f.write(bytes.fromhex(key_hex))

    # 🔥 MUHIM O‘ZGARISH: `key_uri` = to‘liq URL (foydalanuvchi uchun)
    key_uri = f"http://127.0.0.1:8000/get_key/lesson/{instance.id}/"

    # 🔥 MUHIM O‘ZGARISH: `enc.keyinfo` faylga to‘liq *fayl yo‘li* yozish
    key_info_path = os.path.join(base_dir, 'enc.keyinfo')
    with open(key_info_path, 'w') as f:
        f.write(f"{key_uri}\n{key_file_path}\n{key_hex}")

    # --- ⃣ FFmpeg yordamida HLS generatsiya ---
    output_m3u8 = os.path.join(base_dir, 'master.m3u8')
    segment_pattern = os.path.join(base_dir, 'segment_%03d.ts')

    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-c:v', 'libx264', '-c:a', 'aac',
        '-hls_time', '6',
        '-hls_playlist_type', 'vod',
        '-hls_key_info_file', key_info_path,
        '-hls_segment_filename', segment_pattern,
        output_m3u8
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ FFmpeg muvofaqqiyatli HLS yaratdi")
    except subprocess.CalledProcessError as e:
        print("❌ FFmpeg xatolik berdi:")
        print(e.stderr)
        raise

    # --- ⃣ Modelda video_link yangilash ---
    hls_rel_path = os.path.relpath(output_m3u8, settings.MEDIA_ROOT)
    instance.video_link = f"/media/{hls_rel_path}"
    instance.save(update_fields=['video_link'])


# media/courses/videos/hls/2025/05/16
# media/courses/videos/2025/05/16
