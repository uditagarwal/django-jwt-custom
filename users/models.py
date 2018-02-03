from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
import hashlib
import urllib

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=60, blank=True)
    avatar = models.URLField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def save(self, *args, **kwargs):
        # whenever the model saves, save the avatar from gravatar for the user
        size = 40
        default = "https://example.com/static/images/defaultavatar.jpg"
        self.avatar = "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(self.email.lower()).hexdigest(), urllib.urlencode({'d':default, 's':str(size)}))
        super(User, self).save(*args, **kwargs)
