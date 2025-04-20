import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class HasUpperCaseLetter:
    """
     Validate that the password is not entirely lower case.
     """

    def validate(self, password, user=None):
        if not bool(re.search(r'[A-Z]', password)):
            raise ValidationError(
                _("Password does not have an uppercase letter."),
                code="password_does_not_have_alphanumeric_character",
            )

    def get_help_text(self):
        return _("Password does not have an uppercase letter.")


class HasSpecialCharacter:
    """
     Validate that the password is not entirely lower case.
     """

    def validate(self, password, user=None):
        if not bool(re.search(r'[!@#$%^&*()\-_=+{};:,<.>/?[\]\'\"\\|`~]', password)):
            raise ValidationError(
                _("Password does not have a special character."),
                code="password_does_not_have_special_character",
            )

    def get_help_text(self):
        return _("Password does not have a special character.")


class HasNumericDigit:
    """
     Validate that the password is not entirely lower case.
     """

    def validate(self, password, user=None):
        if not bool(re.search(r'\d', password)):
            raise ValidationError(
                _("Password does not have a numeric digit."),
                code="password_does_not_have_numeric_digit",
            )

    def get_help_text(self):
        return _("Password does not have numeric digit.")

