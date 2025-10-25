import os
import subprocess
import threading
from io import BytesIO

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.db.models import TextChoices, ForeignKey, CASCADE, URLField, FileField, SET_NULL, \
    CheckConstraint, Q, ImageField
from django.db.models.fields import CharField, IntegerField, BooleanField, SmallIntegerField
from django.db.models.fields.files import ImageFieldFile
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import CreatedBaseModel, OrderBaseModel, UUIDBaseModel


class Category(CreatedBaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


def image_size_validator(image: ImageFieldFile):
    image_mb = image.size / 1024 / 1024
    if not image_mb <= 5:
        raise ValidationError("Image MUST be less than 5 MB")


class Course(CreatedBaseModel):
    class Level(TextChoices):
        BEGINNER = 'beginner', _('Beginner')
        ELEMENTARY = 'elementary', _('Elementary')
        INTERMEDIATE = 'intermediate', _('Intermediate')
        ADVANCED = 'advanced', _('Advanced')

    name = CharField(max_length=255)
    level = CharField(max_length=20, choices=Level.choices)
    full_description = CKEditor5Field()
    short_description = CKEditor5Field(blank=True)
    has_certificate = BooleanField(default=True, db_default=True)
    has_support = BooleanField(default=False, db_default=False)
    practice_count = IntegerField(default=0, db_default=0, editable=False)
    valid_days = IntegerField()
    price = IntegerField()
    rating = SmallIntegerField(default=50, editable=False)
    video_count = IntegerField(default=0, db_default=0, editable=False)
    total_video_duration = IntegerField(default=0, db_default=0, editable=False)
    cover_image = ImageField(upload_to='courses/cover_image/%Y/%m/%d',
                             validators=[image_size_validator, FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    category = ForeignKey('users.Category', SET_NULL, null=True, blank=True)
    teachers = ForeignKey('users.User', CASCADE, blank=True)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = '-created_at',
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0) & Q(rating__lte=50),
                name='rating_check_constraints'
            ),
        ]

    def save(self, *args, **kwargs):
        if self.cover_image:
            img = Image.open(self.cover_image)
            img = img.convert("RGB")
            buffer = BytesIO()
            img.save(buffer, format="WEBP", quality=85)
            buffer.seek(0)

            filename = f"{self.cover_image.name.split('.')[0]}.webp"
            self.cover_image = ContentFile(buffer.read(), name=filename)

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.cover_image.delete()
        return super().delete(using, keep_parents)

    def __str__(self):
        return self.name


class About(UUIDBaseModel):
    text = CKEditor5Field(blank=True)
    course = ForeignKey('users.Course', CASCADE, related_name='abouts')

    def __str__(self):
        return self.text


class Requirement(UUIDBaseModel):
    text = CKEditor5Field(blank=True)
    course = ForeignKey('users.Course', CASCADE, related_name='requirements')

    def __str__(self):
        return self.text


class Section(CreatedBaseModel, OrderBaseModel):
    class Status(TextChoices):
        PUBLISHED = 'published', _('Published')
        UNPUBLISHED = 'unpublished', _('Unpublished')

    name = CharField(max_length=255)
    status = CharField(max_length=20, choices=Status.choices, default=Status.UNPUBLISHED)
    course = ForeignKey('users.Course', CASCADE, related_name='sections')
    video_count = IntegerField(default=0, db_default=0, editable=False)
    total_video_duration = IntegerField(default=0, db_default=0, editable=False)

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.name


class Lesson(CreatedBaseModel, OrderBaseModel):  # TODO Parts
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'
        UNPUBLISHED = 'unpublished', 'Unpublished'

    class AccessType(TextChoices):
        PRIVATE = 'private', 'Private'
        PUBLIC = 'public', 'Public'

    name = CharField(max_length=255)
    status = CharField(max_length=20, choices=Status.choices, default=Status.UNPUBLISHED)
    access_type = CharField(max_length=20, choices=AccessType.choices, default=AccessType.PRIVATE)
    video_duration = IntegerField(db_default=0, editable=False)
    section = ForeignKey('users.Section', CASCADE, related_name='lessons')
    video = FileField(upload_to='courses/videos/%Y/%m/%d',
                      help_text="video's format must be 'mp4', 'mov', 'webm'",
                      validators=[FileExtensionValidator(['mp4', 'mov', 'webm'])]
                      )

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')


    # def convert_video_to_hls(self):
    #     # Faqat yangi yaratilganda ishga tushsin
    #     if not self.created_at or not self.video:
    #         return
    #
    #     input_path = self.video.path
    #     print(self.video.name)
    #     # videos / 2025 / 10 / 23 / example_video_kplirQO.mp4
    #
    #     url = self.video.name.removeprefix('courses/').split('.')[0]
    #     print(url)
    #
    #     # Har bir video uchun unikal papka (uuid asosida)
    #     base_dir = os.path.join(settings.MEDIA_ROOT, 'courses/hls', f"{url}")
    #     os.makedirs(base_dir, exist_ok=True)
    #
    #     # --- Kalit yaratish ---
    #     key_hex = os.urandom(16).hex()
    #     key_file_path = os.path.join(base_dir, 'enc.key')
    #     with open(key_file_path, 'wb') as f:
    #         f.write(bytes.fromhex(key_hex))
    #
    #     # 🔥 MUHIM O‘ZGARISH: `key_uri` = to‘liq URL (foydalanuvchi uchun)
    #     key_uri = f"http://127.0.0.1:8000/get_key/lesson/{self.id}/"
    #
    #     # 🔥 MUHIM O‘ZGARISH: `enc.keyinfo` faylga to‘liq *fayl yo‘li* yozish
    #     key_info_path = os.path.join(base_dir, 'enc.keyinfo')
    #     with open(key_info_path, 'w') as f:
    #         f.write(f"{key_uri}\n{key_file_path}\n{key_hex}")
    #
    #     # --- FFmpeg yordamida HLS generatsiya ---
    #     output_m3u8 = os.path.join(base_dir, 'master.m3u8')
    #     segment_pattern = os.path.join(base_dir, 'segment_%03d.ts')
    #
    #     cmd = [
    #         'ffmpeg', '-y', '-i', input_path,
    #         '-c:v', 'libx264', '-c:a', 'aac',
    #         '-hls_time', '6',
    #         '-hls_playlist_type', 'vod',
    #         '-hls_key_info_file', key_info_path,
    #         '-hls_segment_filename', segment_pattern,
    #         output_m3u8
    #     ]
    #
    #     try:
    #         subprocess.run(cmd, check=True, capture_output=True, text=True)
    #         print("✅ FFmpeg muvofaqqiyatli HLS yaratdi")
    #     except subprocess.CalledProcessError as e:
    #         print("❌ FFmpeg xatolik berdi:")
    #         print(e.stderr)
    #         raise


    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        # threading.Thread(target=self.convert_video_to_hls())


    def __str__(self):
        return self.name
