from django.forms import *


class BlobPhotoUploadForm(Form):
    file = FileField(required=True)
