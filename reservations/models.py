from django.db import models


class Listing(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed

    def __str__(self):
        return self.name


class Room(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.listing.name} - {self.name}"


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.start_time} to {self.end_time}"
