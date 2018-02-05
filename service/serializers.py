from rest_framework.serializers import ModelSerializer
from service.models import Image, Video, ImageTag, TextTag


class ImageTagSerializer(ModelSerializer):
    class Meta:
        model = ImageTag
        fields = '__all__'


class TextTagSerializer(ModelSerializer):
    class Meta:
        model = TextTag
        fields = '__all__'


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class VideoSerializer(ModelSerializer):
    image_tags = ImageTagSerializer(required=False, many=True)
    text_tags = TextTagSerializer(required=False, many=True)
    class Meta:
        model = Video
        fields = '__all__'


