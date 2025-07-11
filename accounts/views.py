from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


# Create your views here.
def profile(request):
    """
    Render the user profile page.
    """
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        context = {
            'user': user,
        }
        return render(request, 'accounts/profile.html', context)
    return render(request, 'accounts/profile.html', context={'user': 'You are not authenticated'})

def signup(request):
    """
    Render the signup page and send verification email.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Generate activation token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
            )
            # Send activation email
            send_mail(
                'Activate your account',
                f'Click the link to activate your account: {activation_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'registration/activation_sent.html')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Activation view
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('profile')
    else:
        return render(request, 'registration/activation_invalid.html')