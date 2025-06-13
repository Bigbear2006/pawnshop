from django.contrib import admin
from django.contrib.auth.models import Group

from core import models

admin.site.register(models.Client)
admin.site.register(models.Branch)
admin.site.register(models.SpendOption)
admin.site.register(models.OnlineEvaluationGuide)
admin.site.register(models.Publication)
admin.site.register(models.OurSite)

admin.site.unregister(Group)
