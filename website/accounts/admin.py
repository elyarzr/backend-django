from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','address']

admin.site.register(Profile,ProfileAdmin)#مدل خودمان را رجیستر میکنیم تا درون ادمین پنل مدل پروفایل را مانند مدل یوزر ببینیم
