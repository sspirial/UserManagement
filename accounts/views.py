from django.shortcuts import render
from django.contrib.auth.models import User

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