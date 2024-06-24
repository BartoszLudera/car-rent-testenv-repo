from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from .send_email import send_email  

from django.core.files.base import ContentFile
import base64
import six
import uuid
from rest_framework import serializers

from .models import Category, Item, ItemImage, Reservation, Brand, EngineType, DriveType, ItemPrice
from .serializers import CategorySerializer, ItemSerializer, ItemImageSerializer, ItemPriceSerializer,ReservationSerializer, BrandSerializer, EngineTypeSerializer, DriveTypeSerializer
from .forms import ItemPriceForm

class DriveTypeList(APIView):
    def get(self, request):
        driveTypes = DriveType.objects.all()
        serializer = DriveTypeSerializer(driveTypes, many=True)
        return Response(serializer.data)

class EngineTypeList(APIView):
    def get(self, request):
        engineTypes = EngineType.objects.all()
        serializer = EngineTypeSerializer(engineTypes, many=True)
        return Response(serializer.data)

# class CarModelList(APIView):
#     def get(self, request):
#         carModels = CarModel.objects.all()
#         serializer = CarModelSerializer(carModels, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CarModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BrandList(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ItemList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        data = request.data
        images_data = data.pop('images', {})
        serializer = ItemSerializer(data=data)

        if serializer.is_valid():
            item = serializer.save(created_by=request.user)
            send_email(serializer.data['created_by_email'], 'Twoja oferta wynajmu samochodu już za chwilę będzie widoczna!', 'Dziękujemy za dodanie nowego ogłoszenia w serwisie, Twoje ogłoszenie jest obecnie werfikowane i pojawi się do 24h, jeśli wybrałeś płatny pakiet, faktura zostanie przesłana do 24h a samo ogłoszenie będzie widoczne na stronie po zaksięgowaniu wpłaty! W przypadku jakichkolwiek pytań lub problemów zachęcamy do kontaktu z naszym działem obsługi klienta. Pozdrawiamy! Email konatkowy: XXX@xxx.pl Telefon kontaktowy: 1234567890')
            send_email('bartosz.ludera.naptime@gmial.com', 'Nowa oferta do akceptacji', 'Wpadła nowa oferta do akceptacji')
            for key, image_data in images_data.items():
                image_data = image_data.split('base64,')[1]  # Extract base64 part
                ItemImage.objects.create(item=item, image=ContentFile(base64.b64decode(image_data), name=f"{uuid.uuid4().hex}.jpg"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        items = Item.objects.filter(is_active=True)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


class ItemDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Item, pk=pk)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationList(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()
            try:
                send_email(reservation.customer_mail, 'Informacje dotyczące Twojej rezerwacji samochodu', 'Cześć, przekazaliśmy informacje dotyczące twojej rezerwacji do właściciela samochodu. Możesz spodziewać się wiadomości zwrotnej lub telefonicznej. W przypadku jakichkolwiek problemów lub pytań zachęcamy do kontaktu pod ten adres email.  Informacje odnośnie rezerwacji: ' + str(reservation) + ' Pozdrawiamy! Email konatkowy:')
                send_email(reservation.company_visible_mail, 'Nowa rezerwacja na Twój samochód', 'A new reservation has been made')
            except Exception as e:
                return Response({"error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Reservation, pk=pk)

    def get(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ItemPriceList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [FormParser, JSONParser]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        prices = ItemPrice.objects.all()
        serializer = ItemPriceSerializer(prices, many=True)
        return Response(serializer.data)