from django.contrib import admin
from base.models import Lounge, Message, Topic

# Register your models here.

admin.site.register(Topic)
admin.site.register(Lounge)
admin.site.register(Message)