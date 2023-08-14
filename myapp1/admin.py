from django.contrib import admin
from .models import  Cas , Patient,SharedCase



admin.site.register(Cas)
# admin.site.register(Simulation)
admin.site.register(SharedCase)
admin.site.register(Patient)

