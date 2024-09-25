from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404

from django.conf import settings
from .tokens import account_activation_token


User = get_user_model()

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(email=email, password=password)
        user.is_active = False
        user.save()

        subject = 'Activate your account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))

        message = f'Hi {user.email},\n\nPlease click the link below to verify your email and activate your account:\n{activation_link}'

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


        return HttpResponse('Please confirm your email address to complete the registration')

    return HttpResponse('Register via POST request')


@csrf_exempt
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation.')
    else:
        return HttpResponse('Activation link is invalid!')