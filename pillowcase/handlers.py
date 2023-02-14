import os

from PIL import Image
from django.conf import settings
from pillowcase.models import Images


class ImageHandler:
    def __init__(self, image: Image):
        self.Image = image

    def save(self, image_name: 'waterfall', image_extension: '.jpg') -> 'save(media/waterfall_320_240.jpg)':
        saved_image_name = f'{image_name}_{self.Image.width}_{self.Image.height}{image_extension}'
        self.Image.save(f'{settings.MEDIA_ROOT}/{saved_image_name}')
        return saved_image_name  # waterfall_320_240.jpg

    @staticmethod
    def get_name_and_extension(image_path: 'waterfall.jpg') -> ('waterfall', '.jpg'):
        image_name, image_extension = os.path.splitext(image_path)
        return image_name, image_extension  # waterfall.jpg

    @staticmethod
    def get_name_with_dimensions(imageObject: Images) -> 'waterfall_100_200.jpg':
        name, extension = ImageHandler.get_name_and_extension(imageObject.name)  # "waterfall", ".jpg"
        new_name = f'{name}_{imageObject.width}_{imageObject.height}'  # "waterfall_320_240"
        return new_name + extension  # "waterfall_320_240" + ".jpg"
