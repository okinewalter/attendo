from django.db import models
from station.models import Station

# Create your models here.
class Record(models.Model):
    # Fields for storing user details and attendance data
    fname = models.CharField(max_length=50)  # First Name
    lname = models.CharField(max_length=50)  # Last Name
    onames = models.CharField(max_length=100, blank=True)  # Other Names (optional)
    
    # Reference to Station model (dropdown-style selection)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, blank=True)
    
    time_in = models.DateTimeField(auto_now_add=True)  # Time when the person checks in
    time_out = models.DateTimeField(null=True, blank=True)  # Time when the person checks out
    
    signature = models.ImageField(upload_to='signature/', null=True, blank=True)  # Add this field
    
    def __str__(self):
        return f"{self.fname} {self.lname} - {self.onames} at {self.station.name if self.station else 'Unknown Station'}"