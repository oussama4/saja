from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def pre_checkout(request):
    """ checks if user info is complete and show a summery of the order """

    if request.GET.get('conditions') == '1':
        return redirect('checkout:pre_payment')

    return render(request, "checkout/pre_checkout.html")


