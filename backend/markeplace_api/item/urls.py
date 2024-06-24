from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import CategoryList, CategoryDetail, ItemList, ItemDetail, ReservationList, ReservationDetail, EngineTypeList, BrandList, DriveTypeList
urlpatterns = [
    path('drivetypes/', DriveTypeList.as_view(), name='drive-type-list'),
    path('enginetypes/', EngineTypeList.as_view(), name='engine-type-list'),
    path('brands/', BrandList.as_view(), name='carmodel-list'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('items/', ItemList.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
    path('reservations/', ReservationList.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', ReservationDetail.as_view(), name='reservation-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
