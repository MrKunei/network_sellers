from django.urls import path
from rest_framework import routers

from sellers.views import (ProductViewSet, SellerStatView, SellerQrCodeView,
                          SellerListView, SellerCreateView, SellerDetailView,
                          SellerUpdateView, SellerDeleteView,
                           )

router = routers.SimpleRouter()
router.register('product', ProductViewSet)

urlpatterns = [
    path('seller/stat/', SellerStatView.as_view()),
    path('seller/', SellerListView.as_view()),
    path('seller/create/', SellerCreateView.as_view()),
    path('seller/<int:pk>/', SellerDetailView.as_view()),
    path('seller/<int:pk>/update/', SellerUpdateView.as_view()),
    path('seller/<int:pk>/delete/', SellerDeleteView.as_view()),

    path('seller/<int:pk>/qrcode/', SellerQrCodeView.as_view()),
]

urlpatterns += router.urls

