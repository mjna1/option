from django.contrib import admin

# Register your models here.
# register model to admin
from tsetmc import models

admin.site.register(models.Stock)
