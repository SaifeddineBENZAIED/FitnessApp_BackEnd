from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from django.core.files.uploadedfile import UploadedFile

FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10mb

def file_validation(file):
    if not file:
        raise ValidationError("No file selected.")

    # For regular upload, we get UploadedFile instance, so we can validate it.
    # When using direct upload from the browser, here we get an instance of the CloudinaryResource
    # and file is already uploaded to Cloudinary.
    # Still can perform all kinds on validations and maybe delete file, approve moderation, perform analysis, etc.
    if isinstance(file, UploadedFile):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 10MB.")

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, age=None, height=None, weight=None, gender=None, fitness_goal=None, activity_level=None, experience_level=None, country=None, dietary_preferences=None, medical_conditions=None, phone_number=None, profile_image=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            age=age,
            height=height,
            weight=weight,
            gender=gender,
            fitness_goal=fitness_goal,
            activity_level=activity_level,
            experience_level=experience_level,
            medical_conditions=medical_conditions,
            dietary_preferences=dietary_preferences,
            country=country,
            phone_number=phone_number,
            profile_image=profile_image,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, username, password=password, **extra_fields)

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    age = models.IntegerField(null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female')
    ],null=True)
    fitness_goal = models.CharField(max_length=100, choices=[
        ('Lose Weight', 'Lose Weight'),
        ('Gain Muscle', 'Gain Muscle'),
        ('Maintain Fitness', 'Maintain Fitness')
    ], null=True)
    activity_level = models.CharField(max_length=100, choices=[
        ('Sedentary', 'Sedentary'),
        ('Lightly Active', 'Lightly Active'),
        ('Moderately Active', 'Moderately Active'),
        ('Very Active', 'Very Active'),
        ('Super Active', 'Super Active')
    ], null=True)
    dietary_preferences = models.TextField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    experience_level = models.CharField(max_length=100, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ], null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_image = CloudinaryField('image', blank=True, null=True, validators=[file_validation])
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def get_profile_image_url(self):
        if self.profile_image:
            return f"https://res.cloudinary.com/{settings.CLOUDINARY['cloud_name']}/{self.profile_image}"
            
        return None

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def clean(self):
        if not self.is_superuser:
            required_fields = ['age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'experience_level']
            for field in required_fields:
                if not getattr(self, field):
                    raise ValidationError(f'{field} is required for non-superuser accounts.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class MuscleGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle_groups = models.ManyToManyField(MuscleGroup, related_name='exercises')
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True, validators=[file_validation])
    video_url = models.URLField(blank=True)

    def get_image_url(self):
        if self.image:
            return f"https://res.cloudinary.com/{settings.CLOUDINARY['cloud_name']}/{self.image}"
            
        return None

    def __str__(self):
        return self.name

class NutritionRecommendation(models.Model):
    meal = models.CharField(max_length=100)
    ingredients = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.meal

class Trainer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    specialty = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    bio = models.TextField()
    profile_image = CloudinaryField('image', blank=True, null=True, validators=[file_validation])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def average_rating(self):
        reviews = ReviewOnTrainers.objects.filter(trainer=self)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return -1

class ReviewOnTrainers(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.trainer} by {self.user}'

class ReviewOnWebsite(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user.username}'
