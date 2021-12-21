from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=30, blank=True)
    gender = models.CharField(_('gender'), max_length=2, choices=GENDER_CHOICES)
    is_superuser = models.BooleanField(_('superuser'))
    active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(_('created'), auto_now_add = True)
    updated_at = models.DateTimeField(_('updated'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
