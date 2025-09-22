from io import BytesIO

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db.models import ImageField, CASCADE, ForeignKey, CharField
from django.db.models.fields.files import ImageFieldFile
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import UUIDBaseModel, CreatedBaseModel


def image_size_validator(image: ImageFieldFile):
    image_mb = image.size / 1024 / 1024
    if not image_mb <= 5:
        raise ValidationError("Image MUST be less than 5 MB")


class Blog(CreatedBaseModel):
    title = CharField(max_length=255)
    description = CKEditor5Field()
    cover_image = ImageField(upload_to='cover_images/%Y/%m/%d',
                             validators=[image_size_validator, FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])

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


class Step(UUIDBaseModel):  # TODO ?
    title = CharField(max_length=255)
    description = CKEditor5Field()
    blog = ForeignKey('users.Blog', CASCADE)
