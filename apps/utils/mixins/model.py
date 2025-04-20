import secrets

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        return self._create_user(email, password, **extra_fields)


class AbstractUserMixin(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    class Validators:
        NameValidator = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabets are allowed.')

    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("username already exists."),
        },
    )
    # temp keep email
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    first_name = models.CharField(_("First Name"), max_length=50, null=True, blank=True,
                                  validators=[Validators.NameValidator])
    last_name = models.CharField(_("Last Name"), max_length=50, null=True, blank=True,
                                 validators=[Validators.NameValidator])
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)


    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def personal_socket_room_id(self):
        return f'sk_{self.id}'

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """email this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class BaseModel(models.Model):
    date_added = models.DateTimeField(auto_now_add=True,help_text=_(f"Date and time when the object was created"))
    date_last_modified = models.DateTimeField(auto_now=True,help_text=_(f"Date and time when the object was last modified"))

    def instance_exists(self):
        return self.__class__.objects.filter(id=self.id).exists()

    def instance(self):
        return self.__class__.objects.get(id=self.id)

    @classmethod
    def get_token(cls):
        return get_random_string(length=32)

    @classmethod
    def generate_random_identifier(cls):
        return secrets.token_hex(5) + str(int(timezone.now().timestamp()))

    def __str__(self):
        return f"< {type(self).__name__}({self.id})"

    class Meta:
        abstract = True
