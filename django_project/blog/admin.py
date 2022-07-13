from django.contrib import admin
from .models import Post, Activity, Comment

admin.site.register(Post)
admin.site.register(Activity)
admin.site.register(Comment)