from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Profile(models.Model):
    user_Name = models.CharField(max_length=50, blank=True)
    first_Name = models.CharField(max_length=50, blank=True)
    last_Name = models.CharField(max_length=50, blank=True)
    phone_Number = models.CharField(max_length=25, blank=True)
    user_Email = models.EmailField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True,
                             help_text='Enter the two letters code for your State')
    zipcode = models.CharField(max_length=15, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.last_Name}, {self.first_Name}'


class Blog(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField()
    content = models.TextField(max_length=2000)
    img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def summary(self):
        return self.content[:100]

    def pub_date(self):
        return self.publication_date.strftime('%b %e %Y')
