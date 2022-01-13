import os

import requests
from PIL import Image
from django.conf import settings
from pillowcase.handlers import ImageHandler
from pillowcase.models import Images
from rest_framework import serializers


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)

    class Meta:
        model = Images
        fields = ['url', 'file', 'id', 'name', 'picture', 'width', 'height', 'parent_picture']
        read_only_fields = ['id', 'name', 'picture', 'width', 'height', 'parent_picture']

    def create(self, validated_data):
        if validated_data.get('url'):
            image_raw_content = requests.get(url=validated_data.get('url'), stream=True).raw
        elif validated_data.get('file'):
            image_raw_content = validated_data.get('file')
        else:
            raise serializers.ValidationError("You must specify <url> or <file> parameter")

        image = Image.open(image_raw_content)

        image_path_data = os.path.basename(validated_data.get('url') or validated_data.get('file').name)
        image_name, image_extension = ImageHandler.get_name_and_extension(image_path_data)
        saved_image_name = ImageHandler(image).save(image_name, image_extension)

        return Images.objects.create(name=image_name + image_extension,
                                     url=validated_data.get('url', None),
                                     picture=self.context['request'].build_absolute_uri(
                                         settings.MEDIA_URL) + saved_image_name,
                                     width=image.width,
                                     height=image.height)


class ImageResizeSerializer(serializers.Serializer):
    width = serializers.IntegerField(required=True)
    height = serializers.IntegerField(required=True)
