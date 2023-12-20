from django.db import models
from django_mysql.models import ListTextField


class Category(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return str(self.id) + " : " + self.name


class SubCategory(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    cat = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return str(self.id) + " : " + self.name



class Product(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, blank=False)
    cat = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    subcat = models.ForeignKey("SubCategory", on_delete=models.SET_NULL, null=True)

    description = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=30, null=True)

    image = models.ImageField(upload_to='product_images/', null=True)
    schematic = models.FileField(upload_to='schematics/', default='schematics/roomba-overlay.jpg')

    sizes = ListTextField(base_field=models.CharField(max_length=100), size=20, null=False, default="no sizes provided")

    @property
    def htmlid(self):
        return "A" + str(self.id)

    def __str__(self):
        return str(self.id) + " : " + self.name





