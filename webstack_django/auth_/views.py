from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup_view(request):
    pass

@csrf_exempt
def signin_view(request):
    pass

@csrf_exempt
def check_email(request):
    pass

def retrieve_session(request):
    pass
