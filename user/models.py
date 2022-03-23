from datetime import date
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.dispatch import receiver
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from django.db.models.signals import post_save, pre_save

class MyManager(BaseUserManager):

    def create_user(self, username, email, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email,  fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, fullname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    fullname = models.CharField(_('Full Name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_verified =models.BooleanField(_('email_verify'),
        default=False,
        help_text=_(
            "Designates whether this user's email has been Verified. "
        ),
    )

    objects = MyManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    def __str__(self) -> str:
        return f'{self.email}'


class Profile(models.Model):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    NONE = 'NONE'
    GENDER = (
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
        (NONE, 'NONE'),
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'), null=True,
                                     editable=False, blank=True)
    bio = models.TextField(blank=True, null=False,
                                verbose_name= _("About Me"))
    gender = models.CharField(max_length=20, choices=GENDER, default='UNSPECIFIED')
    age = models.CharField(max_length=150, blank=True, null=True)
    number = models.PositiveBigIntegerField(_("Telephone Number"), blank=True, null=True)
    ref = models.CharField(max_length=12, verbose_name='Ref', blank=True)
    github = models.CharField(max_length=10, blank=True, null=True, verbose_name ='Github Profile Link')
    linkedIn = models.CharField(max_length=10, blank=True, null=True, verbose_name ='LinkedIn Profile Link')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def get_age(self):
        today = date.today()
        age = today-self.date_of_birth
        years = int((age).days/365.25)
        return years


    def save(self, *args, **kwargs):
        today = date.today()
        age = today-self.date_of_birth
        years = int((age).days/365.25)
        old = "Years Old"
        if not self.age:
            self.age = years + old
        return super().save(*args, **kwargs)


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, db_index=True, null=True, blank=True)
    login = models.DateTimeField(auto_now_add=True)
    logout = models.DateTimeField(null=True, default=None)
