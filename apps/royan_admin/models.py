from django.contrib.auth.models import User
from django.db import models


class RoyanAdmin(User):
    level = models.IntegerField(default=1)
