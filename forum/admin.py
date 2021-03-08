from django.contrib import admin
from .models import Profile, Blog


# Register your models here.


class UserProfile(admin.ModelAdmin):
    list_display = ('last_Name', 'first_Name',)
    list_filter = ('last_Name', 'first_Name',)
    search_fields = ('last_Name',)
    ordering = ['last_Name']


class Blogs(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date',)
    list_filter = ('author', 'title',)
    search_fields = ('author',)
    ordering = ['author']


admin.site.register(Profile, UserProfile)
admin.site.register(Blog, Blogs)
