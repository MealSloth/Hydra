from django.forms import *


class BlobImageUploadForm(Form):
    file = FileField(required=True)
