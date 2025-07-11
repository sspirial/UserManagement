from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


# Create your views here.
@login_required(login_url='login')
def index(request):
    """
    Manage all the user accounts. accessible only to users that are staff
    :param request: Django HttpRequest object
    :return: Rendered template with user list or redirect to profile
    """
    if request.user.is_staff:
        users = User.objects.all()
        print(users)
        context = {
            'users': users,
        }
        return render(request, 'accounts/index.html', context)
    else:
        return redirect('accounts:profile')

@login_required
def profile(request):
    """
    Render the user profile page.
    """
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        context = {
            'user': user,
        }
        if request.method == 'GET':
            return render(request, 'accounts/profile.html', context)
        elif request.method == 'POST':
            user.username = request.POST.get('username', user.username)
            user.email = request.POST.get('email', user.email)
            user.first_name = request.POST.get('first_name', user.first_name)
            user.save()
            context = {'user': user}
            return render(request, 'accounts/profile.html')

    return redirect('accounts:login')

def signup(request):
    """
    Render the signup page and send verification email.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
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
        form = CustomUserCreationForm()
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
        return redirect('accounts:profile')
    else:
        return render(request, 'registration/activation_invalid.html')