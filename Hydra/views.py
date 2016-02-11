from django.http import HttpResponse
from json import dumps


def home(request):
    response = {
        'message': 'This is the MealSloth Blob API. For more information about MealSloth, visit the URL.',
        'url': 'mealsloth.com',
    }
    return HttpResponse(dumps(response), content_type='application/json')
