# middleware.py
from django.core.mail import mail_admins
from django.conf import settings

class ErrorNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 500:
            subject = f"Server Error on {request.get_full_path()}"
            message = f"User: {request.user}\n\n{response.content.decode()}"
            mail_admins(subject, message, fail_silently=True)
            print('>>>>>>>>>>>>>>>>>>> calling middleware')
        return response
