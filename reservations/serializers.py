from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    
    def validate(self, attrs):
        # check if the room is available for the requested dates
        start_date = attrs.get('start_date')
        if Reservation.objects.filter(room_id=attrs.get('room'), start_date__lte=start_date, end_date__gte=start_date).exists():
            raise serializers.ValidationError("Room is not available for the requested dates")
        
        return attrs
    
    class Meta:
        model = Reservation
        fields = '__all__'
