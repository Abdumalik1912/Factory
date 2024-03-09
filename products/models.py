from django.db import models

# Bu yerda modellar yaratdim


class Product(models.Model):
    product_name = models.CharField(max_length=500)
    product_code = models.IntegerField()


class Material(models.Model):
    material_name = models.CharField(max_length=500)


class ProductMaterial(models.Model):
    product_id = models.ForeignKey(Product, models.CASCADE, related_name="product_material")
    material_id = models.ForeignKey(Material, models.CASCADE, related_name="material_product")
    quantity = models.FloatField()


class Warehouse(models.Model):
    material_id = models.ForeignKey(Material, models.CASCADE, related_name="material_warehouse")
    remainder = models.FloatField()
    price = models.FloatField()


# Ushbu modellarimizga datalarni postgeSQL database da kiritdim.