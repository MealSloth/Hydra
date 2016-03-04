from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='/'),
    url(r'^album/create/', views.album_create, name='album/create/'),
    url(r'^album/delete/', views.album_delete, name='album/delete/'),
    url(r'^bucket/url/', views.bucket_url, name='bucket/url/'),
    url(r'^blob/upload/', views.blob_upload, name='blob/upload/'),
    url(r'^blob/delete/', views.blob_delete, name='blob/delete/'),
)
