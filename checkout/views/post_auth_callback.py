from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def host_to_host_callback(request):
    print(request.POST)
    return redirect('/')

