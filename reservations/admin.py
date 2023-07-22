from django.contrib import admin
from .models import Listing, Reservation, Room


# Register your models here.
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
    
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'listing')    
    
    
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'room')
    