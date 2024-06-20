from django.contrib import admin
from .models import ActiveSubstance, Drug, AddedSubstance, Patient


admin.site.register(ActiveSubstance)
admin.site.register(Drug)
admin.site.register(AddedSubstance)
admin.site.register(Patient)