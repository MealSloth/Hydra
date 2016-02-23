from settings import GCS_CLIENT_ID, GOOGLE_CLOUD_STORAGE_URL
from _include.Chimera.Chimera.models import Album, Blob
from _include.Chimera.Chimera.results import Result
from django.core.files.base import ContentFile
from google_cloud import GoogleCloudStorage
from django.http import HttpResponse
from datetime import datetime
from json import dumps, loads
from base64 import b64decode
import imghdr


def home(request):
    response = dumps({
        'message': 'This is the MealSloth Blob API. For more information about MealSloth, visit the URL.',
        'url': 'mealsloth.com',
    })
    return HttpResponse(response, content_type='application/json')


def bucket_url(request):
    response = {'url': GOOGLE_CLOUD_STORAGE_URL + GCS_CLIENT_ID + '/'}
    Result.append_result(response, Result.SUCCESS)
    response = dumps(response)
    return HttpResponse(response, content_type='application/json')


def blob_upload(request):
    if request.method == 'POST':
        body = loads(request.body)

        if not body.get('file'):
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        decoded_image = b64decode(body['file'])
        image_file = ContentFile(decoded_image)

        url_suffix = body.get('url_suffix')

        gcs = GoogleCloudStorage()

        if not body.get('album_id'):
            album = Album(time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f"))
            album.save()
        else:
            album = Album.objects.filter(pk=body.get('album_id'))
            if album.count() > 0:
                album = album[0]
            else:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')

        blob = Blob(
            album_id=album.id,
            content_type='image/' + imghdr.what(image_file),
            time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        )

        try:
            blob.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_BLOB)
            return HttpResponse(response, content_type='application/json')
        try:
            blob.gcs_id = gcs.save(url_suffix + str(blob.id), image_file)
        except StandardError:
            response = Result.get_result_dump(Result.STORAGE_CANNOT_SAVE_BLOB)
            return HttpResponse(response, content_type='application/json')
        try:
            blob.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_BLOB)
            return HttpResponse(response, content_type='application/json')

        response = Result.get_result_dump(Result.SUCCESS)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')


def blog_image_upload(request):
    if request.method == 'POST':
        body = loads(request.body)
        decoded_image = b64decode(body['file'])

        image_file = ContentFile(decoded_image)

        gcs = GoogleCloudStorage()

        album = Album(
            id=body['album_id'],
            time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        )

        try:
            album.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_ALBUM)
            return HttpResponse(response, content_type='application/json')

        blob = Blob(
            album_id=album.id,
            content_type='image/' + imghdr.what(image_file),
            time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        )

        try:
            blob.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_BLOB)
            return HttpResponse(response, content_type='application/json')

        try:
            blob.gcs_id = gcs.save('siren/blog/' + str(blob.id), image_file)
        except IOError:
            response = Result.get_result_dump(Result.STORAGE_CANNOT_SAVE_BLOB)
            return HttpResponse(response, content_type='application/json')

        try:
            blob.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_BLOB)
            return HttpResponse(response, content_type='application/json')

        response = Result.get_result_dump(Result.SUCCESS)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')


def blob_image_view(request):
    pass
