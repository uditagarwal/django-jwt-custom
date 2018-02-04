from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User

class Ideas(models.Model):
    content = models.CharField(_('Content'), max_length=255)
    impact = models.IntegerField()
    ease = models.IntegerField()
    confidence = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Add a foreign Key to the User to attach users to their ideas
    user = models.ForeignKey(User, related_name='ideas')

    def __str__(self):
        return self.content

    @property
    def average_score(self):
        return round((self.impact + self.ease + self.confidence)/3, 2)
