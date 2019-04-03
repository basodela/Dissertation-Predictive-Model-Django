from django.contrib import admin
from .models import Account
from .models import Exercise
from .models import Post, Programme, Sets, MachineLearningModel


# Register your models here.

admin.site.register(Post)
admin.site.register(Account)
admin.site.register(Exercise)
admin.site.register(Programme)
admin.site.register(Sets)
admin.site.register(MachineLearningModel)








