from settings import GCS_CLIENT_ID, GOOGLE_CLOUD_STORAGE_URL
from _include.Chimera.Chimera.settings import TIME_FORMAT
from _include.Chimera.Chimera.utils import model_to_dict
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


def album_create(request):
    if request and request.method == 'POST':
        if not request or not request.method == 'POST':
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        album = Album(time=datetime.utcnow().strftime(TIME_FORMAT))

        try:
            album.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_ALBUM)
            return HttpResponse(response, content_type='application/json')

        response = {'album': model_to_dict(album)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')


def album_delete(request):
    if request.method == 'POST':
        body = loads(request.body)

        if not body.get('album_id'):
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        album = Album.objects.filter(id=body.get('album_id'))

        if album.count() > 0:
            album = album[0]
        else:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')

        blob_list = Blob.objects.filter(album_id=album.id)

        gcs = GoogleCloudStorage()

        for blob in blob_list:
            try:
                gcs.delete(blob.gcs_id)
            except IOError:
                response = Result.get_result_dump(Result.STORAGE_CANNOT_DELETE_BLOB)
                return HttpResponse(response, content_type='application/json')

        for blob in blob_list:
            try:
                blob.delete()
            except StandardError:
                response = Result.get_result_dump(Result.DATABASE_CANNOT_DELETE_BLOB)
                return HttpResponse(response, content_type='application/json')

        try:
            album.delete()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_DELETE_ALBUM)
            return HttpResponse(response, content_type='application/json')

        response = Result.get_result_dump(Result.SUCCESS)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
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

        filetype = imghdr.what(image_file)

        if filetype not in ('jpeg', 'png', 'gif'):
            response = Result.get_result_dump(Result.FILETYPE_INVALID)
            return HttpResponse(response, content_type='application/json')

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


def blob_delete(request):
    if request.method == 'POST':
        body = loads(request.body)

        if not body.get('blob_id'):
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        blob_id = body.get('blob_id')
        blob = Blob.objects.filter(pk=blob_id)

        if blob.count() > 0:
            blob = blob[0]
        else:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')

        gcs = GoogleCloudStorage()
        gcs_id = blob.gcs_id

        try:
            blob.delete()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_DELETE_BLOB)
            return HttpResponse(response, content_type='application/json')

        try:
            gcs.delete(gcs_id)
        except IOError:
            response = Result.get_result_dump(Result.STORAGE_CANNOT_DELETE_BLOB)
            return HttpResponse(response, content_type='application/json')

        response = Result.get_result_dump(Result.SUCCESS)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
