# Bu yerda ham qaysi mahsulot uchun partiyalardan qancha xomashyo olinayotganini kuzatib turish va saqlash uchun class
# ochdim.


from .product_materials import ProductMaterial


class ProductClass:

    def __init__(self, product_name, product_qty):
        self.product_name = product_name
        self.product_qty = product_qty
        self.product_materials = []

    def add_product_material(self, product_material: ProductMaterial):
        self.product_materials.append(product_material)
