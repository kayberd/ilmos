from django.contrib import admin
from .models  import *
# Register your models here.

admin.site.register([Seat, User, Occupation, Queue])

admin.site.site_header = "ILMoS Admin"
admin.site.site_title = "ILMoS Admin Portal"
admin.site.index_title = "Welcome to ILMoS Portal"