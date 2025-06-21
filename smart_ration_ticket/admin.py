from django.contrib import admin
from .models import Supplier, DistributionSession, UserBooking

admin.site.register(Supplier)
admin.site.register(DistributionSession)
admin.site.register(UserBooking)
