from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(request, f'Welcome {user.username}, your account was created successfully !')
            
            #Redirecting to Dashboard
            return redirect('teams_list')
        
        messages.error(request, 'Please correct the errors below.')
    
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })