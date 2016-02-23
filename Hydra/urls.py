from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^bucket/url/', views.bucket_url, name='get-bucket-url'),
    url(r'^blob/upload/', views.blob_upload, name='blob/upload'),
    url(r'^blob/delete/', views.blob_delete, name='blob/delete'),
    url(r'^blog/image/upload/', views.blog_image_upload, name='blog-image-upload'),
)
