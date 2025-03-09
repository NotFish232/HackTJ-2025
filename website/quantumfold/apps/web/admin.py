from django.contrib import admin
from quantumfold.apps.web import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Protein)
admin.site.register(models.ProteinResult)