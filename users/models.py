from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from dicts.models import BaseModel
from dicts.validators import validate_only_alphabetic

class CustomUser(AbstractBaseUser, BaseModel):
    email = models.EmailField(
        unique=True,
        validators=[validate_email],
        verbose_name=_("Adres email"), help_text=_("Adres email użytkownika"))
    first_name = models.CharField(
        max_length=32,
        blank=True,
        validators=[validate_only_alphabetic],
        verbose_name=_("Imię"), help_text=_("Imię użytkownika"))
    last_name = models.CharField(
        max_length=32,
        blank=True,
        validators=[validate_only_alphabetic],
        verbose_name=_("Nazwisko"), help_text=_("Nazwisko użytkownika"))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Czy aktywny"), help_text=_("Czy użytkownik aktywny"))
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Czy dostęp do admina"), help_text=_("Czy użytkownik ma dostęp do admina")
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    groups = []

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions to view the app `app_label`.
        You can also override this method to apply custom logic.
        """
        return True

    class Meta:
        abstract = True


class ClientProfile(CustomUser):
    def __str__(self):
        return f"Client: {self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<ClientProfile(id={self.id}, first_name={self.full_name}, is_active={self.is_active})>'

    class Meta:
        verbose_name = _("Klient")
        verbose_name_plural = _("Klienci")
        db_table = "clients"


class ManagerProfile(CustomUser):
    def __str__(self):
        return f"Manager: {self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<ManagerProfile(id={self.id}, full_name={self.full_name}, is_active={self.is_active})>'

    class Meta:
        verbose_name = _("Menadżer")
        verbose_name_plural = _("Menadżerowie")
        db_table = "managers"


class AdminProfile(CustomUser):
    def __str__(self):
        return f"Admin: {self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<AdminProfile(id={self.id}, first_name={self.full_name}, is_active={self.is_active})>'

    class Meta:
        verbose_name = _("Administrator")
        verbose_name_plural = _("Administratorzy")
        db_table = "admins"