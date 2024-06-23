from django.db import models

from django.contrib.auth.models import UserManager, AbstractUser


class CustomUserManager(UserManager):
    def create_user(self, username, email, password , first_name, last_name):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            return ValueError("User must have a last name")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name

        )
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, Status, username, email,  password, first_name, last_name):
        if not Status:
            raise ValueError("User must be a staff or admin user")
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            return ValueError("User must have a last name")
        

        email = self.normalize_email(email)
        user = self.model(
            Status=Status,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name

        )
        user.set_password(password)  # change password to hash
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_anonymous = False
        user.save(using=self._db)
        return user

    def create_staffuser(self, Status, username,  email,  password, first_name , last_name):
        if not Status:
            raise ValueError("User must be a staff or admin user")
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            return ValueError("User must have a last name")

        email = self.normalize_email(email)
        user = self.model(
            Status=Status,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name

        )
        user.set_password(password)  # change password to hash
        user.is_admin = False
        user.is_staff = True
        user.is_anonymous = False
        user.save(using=self._db)
        return user


class User(AbstractUser):
    ADMIN = "Admin"
    STAFF = "Staff"
    STATUS_CHOICES = [
        (ADMIN, ("Admin")),
        (STAFF, ("Staff"))
    ]
    Status = models.CharField(choices=STATUS_CHOICES,
                              max_length=255, default='Staff')

    username = models.CharField(('username'), unique=True, max_length=255)
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(('first_name'), max_length=255 )
    last_name = models.CharField(('last_name') , max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    @ staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @ staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return "{}".format(self.username)