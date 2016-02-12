from form.image.form_blob_image_upload import BlobImageUploadForm
from django.http import HttpResponse, HttpResponseRedirect
from _include.Chimera.Chimera.models import Album, Blob
from google_cloud import GoogleCloudStorage
from json import dumps


def home(request):
    response = {
        'message': 'This is the MealSloth Blob API. For more information about MealSloth, visit the URL.',
        'url': 'mealsloth.com',
    }
    return HttpResponse(dumps(response), content_type='application/json')


def blob_image_upload(request):
    if request.method == 'POST':
        print(request)
        form = BlobImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            gcs = GoogleCloudStorage()

            album = Album()
            album.save()

            blob = Blob(
                album_id=album.id,
                content_type='image/jpeg',
            )

            blob.save()
            blob.gcs_id = gcs.save('user/profile-photo/' + str(blob.id), request.FILES['file'])
            print(blob.gcs_id)
            blob.save()

            response = {'result': 1000}
            return HttpResponse(dumps(response), content_type='application/json')
        else:
            response = {'result': 2020, 'message': 'Invalid form'}
            return HttpResponse(dumps(response), content_type='application/json')
    else:
        response = {'result': 9001, 'message': 'Only accessible by POST'}
        return HttpResponse(dumps(response), content_type='application/json')
