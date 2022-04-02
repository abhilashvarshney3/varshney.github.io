from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authy.forms import CreateUserForm
from authy.models import Profile
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Profile)

class RegisterUserAdmin(UserAdmin):
    add_form = CreateUserForm

admin.site.unregister(User)
admin.site.register(User, RegisterUserAdmin)