from django.contrib.auth import get_user_model, authenticate, login
from django.core.mail import send_mail
from django.middleware.csrf import get_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django_ratelimit.decorators import ratelimit

from django.conf import settings
from .tokens import account_activation_token


User = get_user_model()

@ratelimit(key='ip', rate='1/m', method='POST', block=True)  # Limit to 5 requests per minute per IP
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


@csrf_protect
@ratelimit(key='ip', rate='5/m', method='POST', block=True)  # Limit to 5 requests per minute per IP
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        csrf_token = request.META.get('HTTP_X_CSRFTOKEN')

        # Check if CSRF token is valid
        if csrf_token is None or csrf_token != get_token(request):
            return JsonResponse({'error': 'CSRF token is missing or incorrect.'}, status=403)


        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                # Log in the user
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Account is inactive. Please activate your account.'}, status=403)
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)

    return JsonResponse({'error': 'Login via POST request only'}, status=405)


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


@csrf_exempt
def get_csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})