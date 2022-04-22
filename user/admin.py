from django.contrib import admin

# Register your models here.
from user.models import User  # 引入user类

class user_admin(admin.ModelAdmin):  # 定义user_admin类
    list_display = ('user_id', 'user_name',)  # 设置在管理界面列表中显示的字段


admin.site.register(User, user_admin)
