from django.conf.urls import url

from . import views

app_name = 'refer'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^comprehension', views.comprehension, name='comprehension'),
    url(r'^generation', views.generation, name='generation'),
    url(r'^upload', views.file_upload, name='upload'),
    url(r'^refer_using_image_url/', views.upload_image_using_url, name='upload-url'),
]