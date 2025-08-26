from django.db import models

class Flight(models.Model):
    FLIGHT_TYPES = [
        ('Nacional', 'Nacional'),
        ('Internacional', 'Internacional'),
    ]
    
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=15, choices=FLIGHT_TYPES)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.type}"