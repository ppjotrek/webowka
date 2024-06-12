from django.contrib import admin
from .models import ActiveSubstance, Drug, AddedSubstance


admin.site.register(ActiveSubstance)
admin.site.register(Drug)
admin.site.register(AddedSubstance)
