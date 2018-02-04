from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
import hashlib
import urllib
import secrets
from datetime import datetime, timedelta
import jwt
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=60, blank=True)
    avatar = models.URLField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def jwt(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        """
        return self._generate_jwt_token()


    def _generate_gravatar_url(self):
        """
        Generates the Gravatar for the URL of the user

        """
        size = 40
        default = "https://example.com/static/images/defaultavatar.jpg"
        return "https://www.gravatar.com/avatar/%s?%s" % (
            hashlib.md5(self.email.encode('utf-8').lower()).hexdigest(),
            'identicon'
        )

    def _generate_refresh_token(self):
        """
        Generates a permanent refresh token which can be used to refresh
        the access token
        
        """
        return secrets.token_hex(24)

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        time of 10 minutes
        """
        dt = datetime.now() + timedelta(seconds=600)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s')),
            'refresh': self.refresh_token
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


    def save(self, *args, **kwargs):
        """
        Store the Gravatar and Generate a new Refresh Token and store it
        whenever the user saves
        
        """
        self.avatar = self._generate_gravatar_url()
        self.refresh_token = self._generate_refresh_token()
        super(User, self).save(*args, **kwargs)
