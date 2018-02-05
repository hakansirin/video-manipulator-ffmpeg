from service.views import ImageViewSet, VideoViewSet, ImageTagViewSet, TextTagViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from hcm_video import settings
from service.views import generate_video



router = DefaultRouter()
router.register(r"images", ImageViewSet, base_name='image')
router.register(r"videos", VideoViewSet, base_name='video')
router.register(r"imageTags", ImageTagViewSet, base_name='image tag')
router.register(r"textTags", TextTagViewSet, base_name='text tag')


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^generateVideo/(?P<video_id>[0-9]+)/?$', generate_video),

    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
