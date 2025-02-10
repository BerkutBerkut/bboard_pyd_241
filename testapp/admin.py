from django.contrib import admin

from testapp.models import Machine

# class MachineAdmin(admin.ModelAdmin):
#     filter_horizontal = ('spares',)


# admin.site.register(Machine, MachineAdmin)
admin.site.register(Machine)
