from django.urls import path
from .views import shipment as shipment_views
from .views import car as car_views

urlpatterns = [
    path('cars/', car_views.ListCreateCarView.as_view(), name='list-create-car'),
    path('cars/<int:car_id>/', car_views.UpdateCarView.as_view(), name='get-update-delete-car'),
    path('shipments/', shipment_views.ListCreateShipmentsView.as_view(), name='list-create-shipment'),
    path('shipments/filter/', shipment_views.FilterShipmentsView.as_view(), name='filter-shipments'),
    path('shipments/<int:shipment_id>/', shipment_views.GetUpdateDeleteShipmentView.as_view(), name='get-update-delete-shipment'),
]
