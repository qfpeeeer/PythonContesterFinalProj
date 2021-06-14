from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('Users must have a username.')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "default_media/default_profile-image.png"


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)
    rating = models.IntegerField(default=0, blank=True)
    points = models.FloatField(default=0)

    objects = MyAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    input_description = models.TextField(max_length=1000)
    output_description = models.TextField(max_length=1000)
    complexity = models.CharField(default=None, blank=True, null=True, max_length=10)
    topics = ArrayField(models.CharField(default=list, blank=True, null=True, max_length=32))
    user_counter = models.IntegerField(blank=True, default=0)
    points = models.IntegerField()
    image = models.ImageField(default=None, blank=True, null=True, upload_to='task_image')
    note = models.TextField(default=None, blank=True, null=True)
    example = models.TextField(default=None, blank=True, null=True)
    # is_visible = models.BooleanField(default=None, blank=True, null=True)
    sample_number = models.IntegerField(default=1)
    first_tc_input = models.TextField(max_length=100)
    first_tc_output = models.TextField(max_length=100)
    second_tc_input = models.TextField(max_length=100)
    second_tc_output = models.TextField(max_length=100)
    third_tc_input = models.TextField(max_length=100)
    third_tc_output = models.TextField(max_length=100)

class Submit(models.Model):
    user_id = models.IntegerField()
    task_id = models.IntegerField()
    points = models.FloatField(max_length=100)
    is_accepted = models.BooleanField(default=False)
    document_id = models.IntegerField()
    submited_at = models.DateTimeField(auto_now_add=True)


class Contest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField()
    user_counter = models.IntegerField(default=0)
    tasks = models.ManyToManyField(Task)


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    docfile = models.FileField(upload_to='codes/',
                               default='codes/empty.txt')
    task_id = models.IntegerField(default=-1)
    is_author_code = models.BooleanField(default=False)


class SuggestedTask(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    isOriginal = models.BooleanField()
    description = models.TextField()
    solution = models.TextField()