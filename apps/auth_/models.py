from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from apps.utils.helpers import identifier
from apps.utils.mixins import BaseModel, AbstractUserMixin


# Create your models here.
class User(
    AbstractUserMixin,
    BaseModel,
):
    """
        Stores a User, related to :model:`file_manager.FileModel` and :model:`file_manager.LargeFileUpload`.
    """
    balance = models.FloatField(
        _("Balance"),
        null=False,
        blank=False,
        default=0,
        validators=[MinValueValidator(0.0)],
    )

    @property
    def tokens(self):
        """generate access and refresh tokens"""
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.email}"


class PasswordResetToken(
    BaseModel,
):
    """
        Stores Password Rest Tokens for user forgot password emails, related to :model:`auth_.User`.
    """
    token = models.CharField(
        _("token"),
        max_length=150,
        unique=True,
        default=BaseModel.get_token,
        help_text=_(
            "Email Verification Token."
        ), )
    owner = models.ForeignKey(
        "auth_.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="token_as_owner",
        verbose_name=_("User")
    )

    @property
    def elapsed_time(self) -> int:
        """
            Calculates the time elapsed since the token was created.
        """
        time_elapsed_since_created = timezone.now() - self.date_added
        return int(time_elapsed_since_created.total_seconds() - settings.EMAIL_VERIFICATION_TIMEOUT_SECONDS)

    def __str__(self):
        return f"{self.owner.email} - {self.token}"
