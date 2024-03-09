from .views import ProductGetMaterialsView
from django.urls import path

urlpatterns = [
    path("products/", ProductGetMaterialsView.as_view(), name="products")
]
# Postman dan request jo'natishda ko'ylak=30&shim=20 kabi query parameterlar bilan birga jo'nating. Masalan:
# http://127.0.0.1:8000/products/?ko%27ylak=30&shim=20
