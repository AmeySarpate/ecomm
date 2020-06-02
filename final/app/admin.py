from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Color)
admin.site.register(models.City)
admin.site.register(models.Kind)
admin.site.register(models.Customer)
admin.site.register(models.Product)
admin.site.register(models.Purchase)
