# Generated by Django 5.0.3 on 2024-03-09 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=500)),
                ('product_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('material_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_product', to='products.material')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_material', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remainder', models.FloatField()),
                ('price', models.FloatField()),
                ('material_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_warehouse', to='products.material')),
            ],
        ),
    ]
