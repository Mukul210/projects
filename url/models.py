from django.db import models
from .utils import create_shortened_url

# Create your models here.
from accounts.models import Account


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField()
    user = models.ForeignKey(Account, related_name="topics", default=1, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name




class Shortener(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    times_followed = models.PositiveIntegerField(default=0)
    long_url = models.URLField()
    short_url = models.CharField(max_length=15, unique=True, blank=True)
    title =  models.CharField(max_length=200)

    category = models.ForeignKey(Category, related_name='short_links', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name="links", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        if not self.short_url:
            # We pass the model instance that is being saved
            self.short_url = create_shortened_url(self)

        super().save(*args, **kwargs)



    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f'{self.long_url} to {self.short_url}'