from form.image.form_blob_image_upload import BlobImageUploadForm
from _include.Chimera.Chimera.models import Album, Blob
from django.core.files.base import ContentFile
from google_cloud import GoogleCloudStorage
from django.http import HttpResponse
from json import dumps, loads
from base64 import b64decode


def home(request):
    response = {
        'message': 'This is the MealSloth Blob API. For more information about MealSloth, visit the URL.',
        'url': 'mealsloth.com',
    }
    return HttpResponse(dumps(response), content_type='application/json')


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

        response = {'result': 1000}
        return HttpResponse(dumps(response), content_type='application/json')

        # if form.is_valid():
        #     print('Valid form')
        #     return HttpResponse('Valid form on Hydra')
        #     gcs = GoogleCloudStorage()
        #
        #     album = Album()
        #     album.save()
        #
        #     blob = Blob(
        #         album_id=album.id,
        #         content_type='image/jpeg'
        #         # content_type=request.POST['content_type'],
        #     )
        #
        #     blob.save()
        #     blob.gcs_id = gcs.save('user/profile-photo/' + str(blob.id), request.FILES['file'])
        #     blob.save()
        #
        #     response = {'result': 1000}
        #     return HttpResponse(dumps(response), content_type='application/json')
        # else:
        #     response = {'message': 'Invalid form'}
        #     return HttpResponse(response)
    else:
        response = {'result': 9001, 'message': 'Only accessible by POST'}
        return HttpResponse(dumps(response), content_type='application/json')


def blob_image_view(request):
    pass