from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

user = settings.AUTH_USER_MODEL


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, user_login, password=None):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone address')
        if not name:
            raise ValueError('Users must have name')

        user = self.model(
            phone_number=phone_number,
            name=name,

        )
        user.set_password(password)
        user.user_login = user_login
        user.is_active = True
        user.save(using=self._db)
        return user

    # def create_user(self, phone_number, name, user_login, password=None):
    #     """
    #     Creates and saves a User with the given phone and password.
    #     """
    #     if not phone_number:
    #         raise ValueError('Users must have an phone address')
    #     if not name:
    #         raise ValueError('Users must have name')
    #     if not user_login:
    #         raise ValueError('user must have user type')
    #
    #     user = self.model(
    #         phone_number=phone_number,
    #         name=name,
    #         user_login=user_login,
    #         password=password,
    #
    #     )
    #
    #     user.is_active = True
    #     user.save(using=self._db)
    #     return user

    def create_staffuser(self, phone_number, name, user_login, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(

            phone_number,
            name=name,
            user_login=user_login,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, user_login, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            phone_number,
            name,
            password=password,
            user_login=user_login

        )

        user.staff = True
        user.admin = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_type = [
        ('lessor', 'lessor'),
        ('tenant', 'tenant'),
    ]
    name = models.CharField(max_length=255, null=False)
    phone_number = PhoneNumberField(unique=True)
    user_login = models.CharField(max_length=7, choices=user_type, default='lessor', blank=False, null=False)

    # username = None

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name', 'user_login']
    objects = UserManager()

    def get_full_name(self):
        return self.phone_number

    def get_short_name(self):
        return self.phone_number

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


###### create user property

#

class Property_registration(models.Model):
    property_type_p = [
        ('house', 'house'),
        ('car', 'car'),
        ('land', 'land'),
        ('other', 'other')

    ]
    location_name = [
        ('kigali', 'kigali'),
        ('south', 'south'),
        ('east', 'east'),
        ('west', 'west')
    ]
    property_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, choices=location_name, default='kigali')
    property_type = models.CharField(max_length=200, choices=property_type_p)
    amount_per_month = models.IntegerField(default=10000)
    detail = models.CharField(max_length=250, default='')
    property_image = models.ImageField(blank=True, null=True, upload_to='images')
    available = models.BooleanField(default=True)

    owner_name = models.ForeignKey(user, on_delete=models.CASCADE, related_name='owner', null=False)
    time_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property_name} {self.owner_name}'

    class Meta:
        verbose_name_plural = "Property_registration"
        ordering = ['id']


class Request_Property(models.Model):
    status = [
        ('initial', 'initial'),
        ('request', 'request'),
        ('approved', 'approved'),
        ('denied', 'denied'),
        ('canceled', 'canceled')]
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='requesting_users', null=False)
    property_requested = models.ForeignKey(Property_registration, on_delete=models.CASCADE, related_name='property_req',
                                           null=False)
    status_view = models.CharField(max_length=50, choices=status)

    def __str__(self):
        return f'{self.user} {self.property_requested}'

    class Meta:
        verbose_name_plural = "Request"
