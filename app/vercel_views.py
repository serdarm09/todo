from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  
def vercel_test(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Django is working on Vercel!',
        'method': request.method
    })