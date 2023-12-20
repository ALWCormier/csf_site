from django import template
from ..models import Product

register = template.Library()


@register.filter(name="process_sizes")
def process_sizes(size_list):
    outlist = []
    for item in size_list:
        outlist.append(item.split(":")[-1])
    return outlist


@register.filter(name="fill_space")
def fill_space(value, fill_char):
    return value.replace(" ", fill_char)


@register.filter(name="getimage")
def getimage(d):
    product_obj = Product.objects.filter(id=d["pid"]).first()
    return product_obj.image.url


@register.filter(name="getsizes")
def getsizes(d):
    product_obj = Product.objects.filter(id=d["pid"]).first()
    return product_obj.sizes


@register.filter(name="getname")
def getname(d):
    product_obj = Product.objects.filter(id=d["pid"]).first()
    return product_obj.name


@register.filter(name="getid")
def getid(d):
    return d["pid"]


@register.filter(name="size")
def size(d):

    return d["size"]


@register.filter(name="quantity")
def quantity(d):

    return d["quant"]


@register.filter(name="makename")
def makename(d, type):

    return "select-" + type + "-" + d["pid"]

