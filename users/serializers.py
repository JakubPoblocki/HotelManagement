from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from users.models import ClientProfile


class ClientProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True, help_text=_("Adres email"))
    first_name = serializers.CharField(read_only=True, help_text=_("Imię"))
    last_name = serializers.CharField(read_only=True, help_text=_("Nazwisko"))
    is_active = serializers.BooleanField(read_only=True, help_text=_("Czy aktywny"))

    class Meta:
        model = ClientProfile
        fields = ['pk',
                  'email',
                  'first_name',
                  'last_name',
                  'is_active']