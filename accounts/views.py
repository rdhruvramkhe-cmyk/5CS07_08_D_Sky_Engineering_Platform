from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.utils import timezone
from datetime import timedelta
from .forms import CustomUserCreationForm


# SIGNUP VIEW 
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(request, f'Welcome {user.username}, your account was created successfully !')
            
            return redirect('teams_list')
        
        messages.error(request, 'Please correct the errors below.')
    
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })


# ==============================
# CUSTOM LOGIN VIEW 
# ==============================
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        # Check whether the user is currently blocked
        blocked_until = request.session.get('blocked_until')

        if blocked_until:
            blocked_until_time = timezone.datetime.fromisoformat(blocked_until)

            # If block time has not expired, keep user on login page
            if timezone.now() < blocked_until_time:
                messages.error(
                    request,
                    'Your account has been temporarily blocked. Please try again in 3 minutes.'
                )
                return render(request, self.template_name)

            # If 3 minutes passed, clear the block
            request.session.pop('blocked_until', None)
            request.session['failed_attempts'] = 0
            request.session.modified = True

        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        # Count failed login attempts
        failed_attempts = self.request.session.get('failed_attempts', 0)
        failed_attempts += 1
        self.request.session['failed_attempts'] = failed_attempts

        # Block after 3 wrong attempts
        if failed_attempts >= 3:
            blocked_until = timezone.now() + timedelta(minutes=3)
            self.request.session['blocked_until'] = blocked_until.isoformat()
            self.request.session.modified = True

            messages.error(
                self.request,
                'Your account has been temporarily blocked. Please try again in 3 minutes.'
            )

            return render(self.request, self.template_name, {'form': form})

        # Show attempts remaining
        remaining = 3 - failed_attempts
        messages.error(
            self.request,
            f'Incorrect login details. You have {remaining} attempt(s) remaining.'
        )

        self.request.session.modified = True
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        # Reset failed attempts after successful login
        self.request.session['failed_attempts'] = 0
        self.request.session.pop('blocked_until', None)
        self.request.session.modified = True

        return super().form_valid(form)
