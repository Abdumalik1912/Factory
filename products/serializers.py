from rest_framework import serializers

# Bu yerda partiyalarimizni serialize qilib olish uchun custom serializer yaratdim


class WarehouseSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField()
    material_name = serializers.CharField(max_length=500)
    qty = serializers.FloatField()
    price = serializers.FloatField()
