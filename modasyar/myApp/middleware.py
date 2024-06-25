from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                if not profile.is_completed:
                    if request.path not in [reverse('userdetail')]:
                        return redirect('userdetail')
        response = self.get_response(request)
        return response


