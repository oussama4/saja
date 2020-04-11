from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from .forms import UserCreationForm, AddressCreateForm

@login_required
def profile(request):
    return render(request, 'users/profile.html')

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


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

