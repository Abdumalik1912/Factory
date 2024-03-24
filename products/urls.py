from .views import ProductGetMaterialsView, ProductViewSet, MaterialViewSet, WarehouseViewSet, ProductMaterialViewSet
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register("product", ProductViewSet)
router.register("material", MaterialViewSet)
router.register("productmaterial", ProductMaterialViewSet)
router.register("warehouses", WarehouseViewSet)


urlpatterns = [
    path("products/", ProductGetMaterialsView.as_view(), name="products"),
] + router.urls
# Postman dan request jo'natishda ko'ylak=30&shim=20 kabi query parameterlar bilan birga jo'nating. Masalan:
# http://127.0.0.1:8000/products/?ko%27ylak=30&shim=20
