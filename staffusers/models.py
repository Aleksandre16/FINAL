from django.db import models
from django.conf import settings


class StaffUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username
