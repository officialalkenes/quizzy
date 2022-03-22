from datetime import date
from email.policy import default
from tabnanny import verbose
from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, username, fullname, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        user = self.model(email=email,
                         username=username,
                         fullname=fullname,
                         **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, fullname, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') == False:
            raise ValueError("Superuser must have staff set to 'True'.")
        if kwargs.get('is_superuser') == False:
            raise ValueError("Admin must have superuser set to 'True'.")
        return self.create_user(self, email, username, fullname, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True,
                              verbose_name=_("Email Address"))
    username = models.CharField(max_length=150, unique=True,
                              verbose_name=_("Username"))
    fullname = models.CharField(max_length=250, verbose_name=_("Full Name"),
                              help_text='FirstName, LastName and/or OtherNames are required here')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELDS = 'email'
    OTHER_FIELDS = ('username', 'fullname')

    def __str__(self) -> str:
        return f'{self.email}- {self.is_staff}- {self.email_verified}'

    class Meta:
        ordering = ['-date_joined']


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
