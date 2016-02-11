from django.forms import *


class BlobImageUploadForm(Form):
    content_type = ''
    file = FileField(required=True)

    def set_content_type(self, content_type):
        self.content_type = content_type
