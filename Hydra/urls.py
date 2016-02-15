from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^blob-image-upload/', views.blob_image_upload, name='blob-image-upload'),
    url(r'^blog-image-upload/', views.blog_image_upload, name='blog-image-upload'),
    url(r'^get-bucket-url/', views.get_bucket_url, name='get-bucket-url'),
)
