from django.contrib import admin

from printers.models import CustomUser, Printer

# Register your models here.

class UserAdmin(admin.ModelAdmin):
  list_display = ("username", "first_name", 'password', "role")
admin.site.register(CustomUser, UserAdmin)

class PrinterAdmin(admin.ModelAdmin):
  list_display = ("name", "address", 'ink_level', "paper_remaining", 'created_on', 'status')
admin.site.register(Printer, PrinterAdmin)