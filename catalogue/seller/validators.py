from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Add your custom password validation logic here
        if len(password) < 8:
            raise ValidationError(
                _("Your password must contain at least 8 characters."),
                code='password_too_short',
            )

    def get_help_text(self):
        # Help text for the user
        return _(
            "Your password must contain at least 8 characters."
        )