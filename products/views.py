from rest_framework import views, viewsets
from rest_framework.response import Response
from .models import Material, Product, Warehouse, ProductMaterialModel
from .serializers import WarehouseSerializer, ProductSerializer, ProductMaterialSerializer, MaterialSerializer, WarehousePostSerializer
from .utils.product import ProductClass
from .utils.product_materials import ProductMaterial


# Bu yerda faqatgina GET request li APIView dan foydalandim.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class ProductMaterialViewSet(viewsets.ModelViewSet):
    queryset = ProductMaterialModel.objects.all()
    serializer_class = ProductMaterialSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehousePostSerializer


class ProductGetMaterialsView(views.APIView):
    def get(self, request):
        # Bu yerda query parameter larni olyabman va ko'ylak va shimning miqdorini o'zgaruvchiga saqlayabman
        koylak_qnt = request.GET.get("ko'ylak")
        shim_qnt = request.GET.get("shim")
        # Bu yerda ko'ylak uchun kerakli xomashyolarni olib, bizga berilgan miqdorga
        # qancha kerak ekanligini hisoblab chiqyabman
        koylak_materials = {}
        for material in Product.objects.get(product_name="Ko'ylak").product_material.all():
            koylak_materials[Material.objects.get(id=material.material_id.id).material_name] = material.quantity * \
                                                                                               float(koylak_qnt)
        # Bu yerda shim uchun kerakli xomashyolarni olib, bizga berilgan miqdorga
        # qancha kerak ekanligini hisoblab chiqyabman
        shim_materials = {}
        for material in Product.objects.get(product_name="Shim").product_material.all():
            shim_materials[Material.objects.get(id=material.material_id.id).material_name] = material.quantity * \
                                                                                             float(shim_qnt)
        # Bu yerda barcha partiyalarni list ga olib olmyabman,
        # shu orqali xomashyolar miqdorini nazorat qila olaman va database imizga ta'sir o'tkazmayman
        warehouses = [[warehouse.id, Material.objects.get(id=warehouse.material_id.id).material_name,
                       warehouse.remainder, warehouse.price] for warehouse in Warehouse.objects.all()]

        # Quyidagi kodlarimiz orqali partiyalardan mahsulotlarimiz uchun qancha xomashyo olinishini hisoblab chiqamiz va
        # har bir hioblangan mahsulot xomashyosini product_objects ga saqlab boramiz
        product_objects = []
        # Bu yerda barcha mahsulot xomashyolarini bir yerga jamlaymiz
        materials = [koylak_materials, shim_materials]
        # key_names va key_value shunchaki ProductClass imizga mahsulotimiz haqida ma'lumot kiritish uchun ochilgan
        key_names = [key for key, value in request.GET.items()]
        key_value = [value for key, value in request.GET.items()]
        # Quyidagi for loop imiz esa har bir mahsulotimiz uchun xomashyolarni partiyadan qancha olishimiz mumkinligini
        # hisoblash uchun.
        for i in range(len(request.GET)):
            # har bir mahsulotimiz uchun product_object ochib olyabmiz, masalan ProductClass(product_name='Ko'ylak',
            # product_qty=30). Shu orqali ularning xomashyolar miqdorini o'zlariga bog'lab ketishimiz osonlashadi.
            product_object = ProductClass(product_name=key_names[i], product_qty=key_value[i])
            # har bir mahsulot ichidagi xomashyolarni(materials[0] = koylak_materials)
            # warehouses(partiyalar)dan qancha olishimiz mumkinligini hisoblayabmiz
            for material in materials[i]:
                # masalan, bu yerda birinchi material imiz bu mato
                for n in range(len(warehouses)):
                    # har bir partiyalarimiz ustidan loop orqali yurib chiqyabmiz
                    if warehouses[n][1] == material and warehouses[n][2] > 0:  # agar partiyadagi xomashyo nomi material
                        # imiz nomi bilan bir xil bo'lsa va ushbu partiyaning qoldig'i(remainder) 0 dan katta bo'lsa..
                        if warehouses[n][2] < materials[i][material]:
                            # bizga kerak xomashyoning miqdoridan partiyadagi miqdor kichik yoki kattaligini tekshiramiz
                            materials[i][material] -= warehouses[n][2]
                            product_materials_object = ProductMaterial(warehouse_id=warehouses[n][0],
                                                                       material_name=warehouses[n][1],
                                                                       qty=warehouses[n][2],
                                                                       price=warehouses[n][3])
                            warehouses[n][2] = 0
                            product_object.add_product_material(product_materials_object)
                        #     agar partiyadagi xomashyo miqdori bizga kerak bo'lgan miqdordan kichik bo'lsa,
                        #     partiyadagi barcha xomashyoni olib, uni nolga tenglashtirib qo'yayabmiz va davom etyabmiz.
                        #     shu bilan birga ProductMaterial object ini yaratib unda partiya ma'lumotlarini kirityabmiz
                        #     va uni product_object ga qo'shib ketyabmiz.
                        else:
                            warehouses[n][2] = warehouses[n][2] - materials[i][material]
                            product_materials_object = ProductMaterial(warehouse_id=warehouses[n][0],
                                                                       material_name=warehouses[n][1],
                                                                       qty=materials[i][material],
                                                                       price=warehouses[n][3])
                            materials[i][material] = 0
                            product_object.add_product_material(product_materials_object)
                            # agar partiyadagi miqdor bizga kerak miqdordan katta bo'lsa, shunchaki bizga kerak miqdorni
                            # partiyadan olib yana tepadagi ishlarni takrorlayabmiz, lekin bu safar inner loop imizdan
                            # chiqib ketamiz, chunki allaqachon kerakli miqdorda xomashyo olib bo'ldik.
                            break
                if materials[i][material] > 0:
                    # agar partiyalarni aylanib chiqqanimizdan keyin ham bizga kerakli miqdordagi xomashyo chiqmasa,
                    # yetmagan miqdorini yozib, warehouse_id va price ni null qilib qo'yayabmiz.
                    product_materials_object = ProductMaterial(warehouse_id=None,
                                                               material_name=material,
                                                               qty=materials[i][material],
                                                               price=None)
                    product_object.add_product_material(product_materials_object)
            product_objects.append(product_object)  # so'nggida ushbu product_object(masalan, Ko'ylak)ni product_objects
        #     listimizga qo'shib qo'yayabmiz.
        # Response imizda product_objects(Ko'ylak, Shim)da loop qilib, product_name va product_qty ni olyabmiz va
        # WarehouseSerializer imizni ishlatib product_materials larimizni serialize qilib olyabmiz.
        return Response({"result": [{"product_name": product_object.product_name,
                                     "product_qty": product_object.product_qty,
                                     "product_materials": WarehouseSerializer(product_object.product_materials,
                                                                              many=True).data}
                                    for product_object in product_objects
                                    ]})
