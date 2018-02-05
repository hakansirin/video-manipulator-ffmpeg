from django.db import models


def image_directory_path(instance, filename):
    return 'images/{0}'.format(filename)


def video_directory_path(instance, filename):
    return 'videos/{0}'.format(filename)
    # return 'media/videos/{0}/{1}'.format(instance.id, filename)


class Image(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = image_directory_path)


class Video(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to = video_directory_path)


class ImageTag(models.Model):
    video = models.ForeignKey(Video, related_name='image_tags', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, related_name='image_tags', on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    start_time = models.FloatField()
    end_time = models.FloatField()


class TextTag(models.Model):
    video = models.ForeignKey(Video, related_name='text_tags', on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    size = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    start_time = models.FloatField()
    end_time = models.FloatField()