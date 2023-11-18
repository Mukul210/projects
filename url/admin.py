from django.contrib import admin

# Register your models here.
from .models import Shortener, Category


admin.site.register(Shortener)
admin.site.register(Category)