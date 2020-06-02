from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def pre_checkout(request):
    """ checks if user info is complete and show a summery of the order """

    if not request.user.has_address:
        return redirect('address_create')
    elif not request.user.has_name:
        return redirect('info_change')

    return render(request, "checkout/pre_checkout.html")


