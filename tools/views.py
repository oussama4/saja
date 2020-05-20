from django.shortcuts import render, redirect, get_object_or_404  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.exceptions import ObjectDoesNotExist

from anymail.message import AnymailMessage

from .forms import EmailForm 
from .models import EmailSubscriber 

import random 
import re 

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@csrf_protect
def new(request):
#    x = re.search("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$", request.POST['email'])

    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                sub = EmailSubscriber.objects.get(email = request.POST['email'])
            except ObjectDoesNotExist:
                sub = EmailSubscriber(email=request.POST['email'],conf_num =random_digits())
                sub.save()
                message = AnymailMessage(
                        subject='Newsletter confirmation',
                        body = f' confirmer votre email par cliquer ce lien: \
                                https://sajacosmetics.com/confirm/?email={sub.email}&conf_num={sub.conf_num}',
                        to = [sub.email],
                )
                message.attach_alternative(f"<a href='{request.build_absolute_uri('/confirm/')}?email={sub.email}&conf_num={sub.conf_num}'>click here html</a>",'text/html')
                message.send()

    return render(request,'home/home_page.html')


def confirm(request):
    message = ''
    sub = get_object_or_404(EmailSubscriber, email = request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        message = 'Your email has been confirmed ! And you are welcome to sajacosmetics newsletter from now on you\'ll be notified to see all our offers and news stay tuned '
    else:
        message = 'not confirmed'
    return render(request, 'partials/emailText.html', {'message':message})

def delete(request):
    message = ''
    sub = get_object_or_404(EmailSubscriber, email= request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        message = 'Your email has been deleted! You want be able to receive our news from now on. Thank you'
    else:
        message = 'not deleted'
    return render(request, 'partials/emailText.html', {'message':message})


'''
def confirm(request):
    sub = get_object_or_404(EmailSubscriber, email = request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()

    return redirect('/')
    
def delete(request):
    sub = get_object_or_404(EmailSubscriber, email = request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        pass
'''

