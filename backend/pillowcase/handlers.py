import os

from PIL import Image
from django.conf import settings
from pillowcase.models import Images


class ImageHandler:
    def __init__(self, image: Image):
        self.Image = image

    def save(self, image_name: str, image_extension: str) -> str:
        saved_image_name = f'{image_name}_{self.Image.width}_{self.Image.height}{image_extension}'
        self.Image.save(f'{settings.MEDIA_ROOT}/{saved_image_name}')
        return saved_image_name

    @staticmethod
    def get_name_and_extension(image_path) -> (str, str):
        image_name, image_extension = os.path.splitext(image_path)
        return image_name, image_extension

    @staticmethod
    def get_name_with_dimensions(imageObject: Images):
        name, extension = ImageHandler.get_name_and_extension(imageObject.name)
        new_name = f'{name}_{imageObject.width}_{imageObject.height}'
        return new_name + extension
