from rest_framework import generics, status, pagination
from .models import Listing, Room, Reservation
from .serializers import ReservationSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render


class CustomPagination(pagination.PageNumberPagination):
    """
    Custom pagination class to return custom response
    """
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'current_page_number': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
        

class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckAvailabilityAPIView(generics.GenericAPIView):
    start_date_param_config = openapi.Parameter('start_date', in_=openapi.IN_QUERY, description='Start Date', type=openapi.FORMAT_DATE)
    end_date_param_config = openapi.Parameter('end_date', in_=openapi.IN_QUERY, description='End Date', type=openapi.FORMAT_DATE)
    number_of_rooms_param_config = openapi.Parameter('number_of_rooms', in_=openapi.IN_QUERY, description='Number of rooms', type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(manual_parameters=[start_date_param_config, end_date_param_config, number_of_rooms_param_config])
    def get(self, request, *args, **kwargs):
        listing_id = self.kwargs['listing_id']
        number_of_rooms = request.query_params.get('number_of_rooms', None)
        start_date = request.query_params.get('start_date', None)
        if not start_date or not number_of_rooms:
            return Response(
                {"error": "start_date and number_of_rooms is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        if Reservation.objects.filter(room__listing_id=listing_id, start_date__lte=start_date, end_date__gte=start_date).count() >= int(number_of_rooms) \
        or Room.objects.filter(listing_id=listing_id).count() < int(number_of_rooms):
            return Response(
                {"error": "Number of rooms requested is not available."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({"message": "Rooms are available for the requested dates"}, status=status.HTTP_200_OK)
    

class ReservationListAPIView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = CustomPagination
    start_date_param_config = openapi.Parameter('start_date', in_=openapi.IN_QUERY, description='Start Date', type=openapi.FORMAT_DATE)
    end_date_param_config = openapi.Parameter('end_date', in_=openapi.IN_QUERY, description='End Date', type=openapi.FORMAT_DATE)
    
    @swagger_auto_schema(manual_parameters=[start_date_param_config, end_date_param_config])
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        reservations = super().get_queryset().filter(room__listing__id=self.kwargs['listing_id'])
        if start_date and end_date:
            return reservations.filter(start_date__gte=start_date, end_date__lte=end_date).order_by('pk')
        
        return reservations.order_by('pk')
    

class ReservationListView(generics.GenericAPIView):
    serializer_class = ReservationSerializer

    def get(self, request, *args, **kwargs):
        reservations = Reservation.objects.filter(room__listing_id=self.kwargs['listing_id'])
        # Render the data in the template
        return render(request, 'reservations_list.html', {'reservations': reservations})

