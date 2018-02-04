from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class CustomPasswordValidator(object):

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d digit.') % {'min_length': self.min_length})
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d upper-case letter.') % {'min_length': self.min_length})
        if not any(char.islower() for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d lower-case letter.') % {'min_length': self.min_length})



    def get_help_text(self):
        return ""
