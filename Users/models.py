
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.urls import reverse
from django.dispatch import receiver

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.cache import cache

from rest_framework.authtoken.models import Token
from picklefield.fields import PickledObjectField
import pandas as pd
from scipy.stats import norm
from django.contrib.auth.models import AbstractUser
import pickle


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Extra(models.Model):

    BW_CHOICES = (

        ('W87+', "Women's 87Kg+"),
        ('W87', "Women's 87Kg"),
        ('W76', "Women's 76kg"),
        ('W71', "Women's 71kg"),
        ('W64', "Women's 64kg"),
        ('W59', "Women's 59kg"),
        ('W55', "Women's 55kg"),
        ('W49', "Women's 49kg"),
        ('M109+', "Men's 109kg+"),
        ('M109+', "Men's 109Kg"),
        ('M102', "Men's 102Kg+"),
        ('M96', "Men's 96kg"),
        ('M89', "Men's 89kg"),
        ('M81', "Men's 81kg"),
        ('M73', "Men's 73kg"),
        ('M67', "Men's 67kg"),
        ('M61', "Men's 61kg"),
        ('M56', "Men's 56kg"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bodyweight = models.CharField(max_length=6, choices=BW_CHOICES, default='Please choose a bodyweight')
    date_of_birth = models.DateField()


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user}'s Account"

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Exercise(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Sets(models.Model):
    sets = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    reps = models.IntegerField(default=3,)
    weight = models.DecimalField(default=10,decimal_places=2, max_digits=5)
    notes = models.CharField(max_length=1000, default="insert notes here")


class Programme(models.Model):
    date = models.DateField(blank=True, null=True)
    lifter = models.ForeignKey(User, on_delete=models.CASCADE)
    sets = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    reps = models.IntegerField(default=3, )
    weight = models.DecimalField(default=10, decimal_places=2, max_digits=5)
    notes = models.CharField(max_length=1000, default="insert notes here")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default='1')

    def __str__(self):
        return f"{self.lifter}'s Programme for {self.date}"

    class Meta:
        ordering = ['-date']


class MachineLearningModel(models.Model):
    training_data = models.FileField(upload_to='training_data')
    target_feature_name = models.CharField(max_length=60, help_text='The name of the target feature column as it '
                                                                    'appears in the training data')
    default = models.BooleanField(default=False, help_text='Is this the default model? (There can only be one)')
    pickled_model = PickledObjectField(editable=False, null=True, blank=True)

