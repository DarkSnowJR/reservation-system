from django.urls import path
from .views import ReservationCreateView, ReservationListAPIView, CheckAvailabilityAPIView, ReservationListView


urlpatterns = [
    path('reservations/', ReservationCreateView.as_view(), name='reservation_list'),
    path('reservations/<int:listing_id>/', ReservationListAPIView.as_view(), name='reservation_list'),
    path('reservations/<int:listing_id>/check-availability/', CheckAvailabilityAPIView.as_view(), name='check_availability'),
    path('report/<int:listing_id>/', ReservationListView.as_view(), name='report')
]
