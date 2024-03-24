from rest_framework import serializers
from .models import Product, ProductMaterialModel, Material, Warehouse

# Bu yerda partiyalarimizni serialize qilib olish uchun custom serializer yaratdim


class WarehouseSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField()
    material_name = serializers.CharField(max_length=500)
    qty = serializers.FloatField()
    price = serializers.FloatField()


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = "__all__"


class ProductMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductMaterialModel
        fields = "__all__"


class WarehousePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = "__all__"
