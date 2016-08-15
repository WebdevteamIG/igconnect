from django.contrib import admin
from forum.models import Thread,Answer,Comment

admin.site.register(Thread)
admin.site.register(Answer)
admin.site.register(Comment)