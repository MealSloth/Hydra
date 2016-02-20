from settings import GCS_CLIENT_ID, GOOGLE_CLOUD_STORAGE_URL
from _include.Chimera.Chimera.models import Album, Blob
from django.core.files.base import ContentFile
from google_cloud import GoogleCloudStorage
from django.http import HttpResponse
from json import dumps, loads
from base64 import b64decode
import imghdr


def home(request):
    response = dumps({
        'message': 'This is the MealSloth Blob API. For more information about MealSloth, visit the URL.',
        'url': 'mealsloth.com',
    })
    return HttpResponse(response, content_type='application/json')


def get_bucket_url(request):
    response = dumps({'url': GOOGLE_CLOUD_STORAGE_URL + GCS_CLIENT_ID + '/', 'result': 1000})
    return HttpResponse(response, content_type='application/json')


def blob_image_upload(request):
    if request.method == 'POST':
        body = loads(request.body)
        decoded_image = b64decode(body['file'])

        image_file = ContentFile(decoded_image)

        gcs = GoogleCloudStorage()

        album = Album()
        album.save()

        blob = Blob(
            album_id=album.id,
            content_type='image/jpeg'
        )

        blob.save()
        blob.gcs_id = gcs.save('user/profile-photo/' + str(blob.id), image_file)
        blob.save()

        response = dumps({'result': 1000})
        return HttpResponse(response, content_type='application/json')
    else:
        response = dumps({'result': 9001, 'message': 'Only accessible by POST'})
        return HttpResponse(response, content_type='application/json')


def blob_image_upload_for_album_id(request):
    if request.method == 'POST':
        body = loads(request.body)
        decoded_image = b64decode(body['file'])
        album_id = body['album_id']

        image_file = ContentFile(decoded_image)

        gcs = GoogleCloudStorage()

        blob = Blob(
            album_id=album_id,
            content_type='image/jpeg'
        )

        blob.save()
        blob.gcs_id = gcs.save('' + str(blob.id), image_file)
        blob.save()

        response = dumps({'result': 1000})
        return HttpResponse(response, content_type='application/json')
    else:
        response = dumps({'result': 9001, 'message': 'Only accessible by POST'})
        return HttpResponse(response, content_type='application/json')


def blog_image_upload(request):
    if request.method == 'POST':
        body = loads(request.body)
        decoded_image = b64decode(body['file'])

        image_file = ContentFile(decoded_image)

        gcs = GoogleCloudStorage()

        album = Album(
            id=body['album_id']
        )

        try:
            album.save()
        except StandardError, error:
            response = dumps({'result': 2041, 'message': 'Cannot save Album to DB', 'error': error})
            return HttpResponse(response, content_type='application/json')

        blob = Blob(
            album_id=album.id,
            content_type='image/' + imghdr.what(image_file)
        )

        try:
            blob.save()
        except StandardError, error:
            response = dumps({'result': 2042, 'message': 'Cannot save Blob to DB', 'error': error})
            return HttpResponse(response, content_type='application/json')
        blob.gcs_id = gcs.save('siren/blog/' + str(blob.id), image_file)
        blob.save()

        response = dumps({'result': 1000})
        return HttpResponse(response, content_type='application/json')
    else:
        response = dumps({'result': 9001, 'message': 'Only accessible by POST'})
        return HttpResponse(response, content_type='application/json')


def blob_image_view(request):
    pass
