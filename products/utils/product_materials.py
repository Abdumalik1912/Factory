# utils folder ochib, bu yerda xomashyo partiyalarini ushlab turuvchi class yaratdim, shu orqali serialize qilishimiz
# osonlashdi


class ProductMaterial:

    def __init__(self, warehouse_id, material_name, qty, price):
        self.warehouse_id = warehouse_id
        self.material_name = material_name
        self.qty = qty
        self.price = price
