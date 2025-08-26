from django.contrib import admin
from .models import Flight

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name',)
    ordering = ('price',)