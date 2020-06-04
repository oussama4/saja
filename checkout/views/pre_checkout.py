from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def pre_checkout(request):
    """ checks if user info is complete and show a summery of the order """
    print(request.GET.get('conditions'))
    if not request.user.has_address:
        return redirect('address_create')
    elif not request.user.has_name:
        return redirect('info_change')

    if request.GET.get('conditions') == '1':
        return redirect(reverse('checkout:pre_payment'))

    return render(request, "checkout/pre_checkout.html")


