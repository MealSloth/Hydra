from _include.Chimera.Chimera.models import Album, Blob
from django.core.files.base import ContentFile
from google_cloud import GoogleCloudStorage
from django.http import HttpResponse
from json import dumps, loads


def home(request):
    response = {
        'message': 'This is the MealSloth Blob API. For more information about MealSloth, visit the URL.',
        'url': 'mealsloth.com',
    }
    return HttpResponse(dumps(response), content_type='application/json')


def blob_image_upload(request):
    if request.method == 'POST':
        if not request.body:
            return

        gcs = GoogleCloudStorage()

        album = Album()
        album.save()

        blob = Blob(
            album_id=album.id,
            content_type='image/jpeg'
            # content_type=request.POST['content_type'],
        )

        blob.save()
        blob.gcs_id = gcs.save('user/profile-photo/' + str(blob.id), ContentFile(request.body[5:]))
        blob.save()

        response = {'result': 1000}
        return HttpResponse(dumps(response), content_type='application/json')
    else:
        response = {'result': 9001, 'message': 'Only accessible by POST'}
        return HttpResponse(dumps(response), content_type='application/json')
