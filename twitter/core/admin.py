from django.contrib import admin
from core.models import Tweet, Hashtag, Person

# Register your models here.
admin.site.register(Tweet)
admin.site.register(Hashtag)
admin.site.register(Person)