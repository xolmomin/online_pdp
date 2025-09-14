from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import ImageField, CASCADE, ForeignKey, CharField
from django.db.models.fields.files import ImageFieldFile
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import UUIDBaseModel, CreatedBaseModel


def image_size_validator(image: ImageFieldFile):
    image_mb = image.size / 1024 / 1024
    if not image_mb <= 5:
        raise ValidationError("Image MUST be less than 5 MB")


# class Image(UUIDBaseModel):      # CKEtidor ichida bor
#     blog = ForeignKey('users.Blog', CASCADE)
#     image = ImageField(upload_to='blogs/%Y/%m/%d', null=True, blank=True,
#                        validators=[image_size_validator, FileExtensionValidator(['jpg', 'jpeg', 'webp'])])
#
#     def delete(self, using=None, keep_parents=False):
#         self.image.delete()
#         return super().delete(using, keep_parents)


class Blog(CreatedBaseModel):
    title = CharField(max_length=255)
    description = CharField(max_length=255)
    cover_image = ImageField(upload_to='cover_images/%Y/%m/%d',
                             validators=[image_size_validator, FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])

    def delete(self, using=None, keep_parents=False):
        self.cover_image.delete()
        return super().delete(using, keep_parents)


class Step(UUIDBaseModel):
    title = CharField(max_length=255)
    description = CKEditor5Field()
    blog = ForeignKey('users.Blog', CASCADE)
