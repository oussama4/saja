from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from checkout.models import Order
from .models import Address
from .forms import UserCreationForm, AddressCreateForm

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class UserUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['email', 'first_name', 'last_name']
    success_url = reverse_lazy('profile')
    success_message = _("vos informations personnelles ont été mises à jour avec succès")
    template_name = 'users/user_change.html'


class ChangeAddress(LoginRequiredMixin, UpdateView):
    model = Address
    success_url = reverse_lazy('address')
    fields = ['line1', 'line2', 'postal_code', 'city', 'phone']
    template_name = 'users/address_change.html'


class OrdersList(LoginRequiredMixin, ListView):
    template_name = 'users/orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def create_address(request):
    if request.method == 'GET':
        form = AddressCreateForm()
        return render(request, 'users/address_create.html', {'form': form})
    elif request.method == 'POST':
        f = AddressCreateForm(request.POST)
        if f.is_valid():
            a = f.save()
            u = request.user
            u.address = a
            u.save()
            return redirect('profile')
        else:
            return render(request, 'users/address_create.html', {'form': f})


@login_required
def order_detail(request, oid):
    o = Order.objects.get(pk=oid)
    return render(request, 'users/order_detail.html', {'order': o})

