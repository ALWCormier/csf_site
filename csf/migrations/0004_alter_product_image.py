# Generated by Django 4.2.3 on 2023-07-23 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csf', '0003_product_desc_product_image_product_spec1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
