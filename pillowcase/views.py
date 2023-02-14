import os

from PIL import Image
from django.conf import settings
from django.shortcuts import get_object_or_404
from pillowcase.handlers import ImageHandler
from pillowcase.models import Images
from pillowcase.serializers import ImageSerializer, ImageResizeSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer

    @action(detail=True, methods=['post'], serializer_class=ImageResizeSerializer)
    def resize(self, request, *args, **kwargs):
        # imageObject <- (models.Images)
        imageObject = self.get_object()  # imageObject.name = "waterfall.jpg"

        old_image_name, old_image_extension = ImageHandler.get_name_and_extension(
            imageObject.name
        )  # old_image_name, old_image_extension = ("waterfall",".jpg")

        old_image_path = ImageHandler.get_name_with_dimensions(imageObject)  # old_image_path = "waterfall_320_240.jpg"

        serializer = ImageResizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = Image.open(f'{settings.MEDIA_ROOT}/{old_image_path}')  # loads "waterfall_320_240.jpg"
        # performs resizing of "waterfall_320_240.jpg"
        resized_image = image.resize((int(serializer.data['width']), int(serializer.data['height'])))
        # saved_image_name = "waterfall_80_60.jpg"
        saved_image_name = ImageHandler(resized_image).save(old_image_name, old_image_extension)

        newImage = Images.objects.create(
            name=old_image_name + old_image_extension,
            url=imageObject.url,
            picture=self.request.build_absolute_uri(
                settings.MEDIA_URL) + saved_image_name,
            width=resized_image.width,
            height=resized_image.height,
            parent_picture=imageObject)

        serializer = ImageSerializer(newImage, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, pk=None, *args, **kwargs):
        image = self.get_object()

        # image_path = "waterfall_320_240.jpg"
        image_path = ImageHandler.get_name_with_dimensions(image)
        # delete file from MEDIA folder
        os.remove(f'{settings.MEDIA_ROOT}/{image_path}')
        # delete from database
        image.delete()
        return Response(status=204)
