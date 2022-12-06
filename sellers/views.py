import qrcode as qrcode
from django.db.models import Avg
from rest_framework import status
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, \
    RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Seller, Product
from .permissions import APIPermission
from .serializers import SellerSerializer, ProductSerializer, \
    SellerUpdateSerializer, SellerCreateSerializer
from .tasks import send_qr_email


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [APIPermission]


class SellerListView(ListAPIView):
    queryset = Seller.objects.prefetch_related('products').\
        select_related('employees').select_related('parent').all()
    serializer_class = SellerSerializer
    permission_classes = [APIPermission]

    def get(self, request, *args, **kwargs):
        country = request.GET.get('country')
        if country:
            self.queryset = self.queryset.filter(country__icontains=country)

        id_product = request.GET.get('id_product')
        if id_product:
            self.queryset = self.queryset.filter(products__id__exact=id_product)

        self.queryset = self.queryset.filter(employees__id__exact=request.auth.user_id)
        return super().get(request, *args, **kwargs)


class SellerDetailView(RetrieveAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [APIPermission]


class SellerCreateView(CreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerCreateSerializer
    permission_classes = [APIPermission]


class SellerUpdateView(UpdateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerUpdateSerializer
    permission_classes = [APIPermission]


class SellerDeleteView(DestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [APIPermission]


class SellerStatView(ListAPIView):
    avg_debt = Seller.objects.aggregate(Avg('debt'))
    queryset = Seller.objects.filter(debt__gte=avg_debt['debt__avg']).\
        prefetch_related('products').select_related('employees').select_related('parent').all()

    serializer_class = SellerSerializer
    permission_classes = [APIPermission]


class SellerQrCodeView(RetrieveAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [APIPermission]

    def get(self, request, *args, **kwargs):
        email = request.auth.user.email
        seller = Seller.objects.get(id=kwargs['pk'])
        contact = f'{seller.country}, {seller.city}, {seller.address}, {seller.email}'

        img = qrcode.make(contact)
        img.save('media/qr/qr.png')
        send_qr_email.delay(email)
        return Response(status=status.HTTP_200_OK)




