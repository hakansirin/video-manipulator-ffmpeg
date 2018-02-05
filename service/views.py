from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from service.models import Image, Video, ImageTag, TextTag
from service.serializers import ImageSerializer, VideoSerializer, ImageTagSerializer, TextTagSerializer
from rest_framework import permissions
from rest_framework.permissions import  AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

import os


class ImageTagViewSet(viewsets.ModelViewSet):
    queryset = ImageTag.objects.all()
    serializer_class = ImageTagSerializer
    permission_classes = (permissions.AllowAny,)


class TextTagViewSet(viewsets.ModelViewSet):
    queryset = TextTag.objects.all()
    serializer_class = TextTagSerializer
    permission_classes = (permissions.AllowAny,)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.AllowAny,)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (permissions.AllowAny,)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def generate_video(request, video_id):
    video = Video.objects.get(id=video_id)
    video_path = video.video.path
    text_tags = video.text_tags.all()
    image_tags = video.image_tags.all().order_by('id')
    command = 'ffmpeg -i ' + str(video_path)
    complex_filter = ""

    count = 0
    for tag in image_tags:
        command += ' -i ' + str(tag.image.image.path)
        if count == 0:
            complex_filter += "[0][1]overlay=x="+ str(tag.x) +":y= "+str(tag.y)+ ":enable='between(t,"+str(tag.start_time)+","+str(tag.end_time)+")'[v1];\n"
        else:
            complex_filter += "[v"+str(count)+"]["+str(count+1)+"]overlay=x="+ str(tag.x) +":y= "+str(tag.y)+\
                              ":enable='between(t,"+str(tag.start_time)+","+str(tag.end_time)+")'[v"+ str(count+1) +"];\n"
        count += 1

    if len(text_tags) and len(image_tags):
        complex_filter += "[v"+ str(count) +"]"

    for tag in text_tags:
        complex_filter += "drawtext=fontsize=" + str(
            tag.size) + ":fontcolor=White:fontfile='arial.ttf:text='" + tag.text + \
                          ":enable='between(t," + str(tag.start_time) + "," + str(tag.end_time) + ")'" + ":x=" + str(
            tag.x) + ":y=" + str(tag.y) + ","

    if len(text_tags):
        complex_filter = complex_filter[:-1]

    index = str(video.video).find('/')
    video_name = str(video.video)[index+1:]

    command += ' -filter_complex '+ '"' + complex_filter + '"' + ' media/videos/outputs/' + video_name
    print(command)
    os.system('rm media/videos/outputs/' + video_name)
    os.system(command)

    return Response(status=status.HTTP_200_OK)
