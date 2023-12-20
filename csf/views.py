# Base Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings
from .models import Category
from .models import Product
from .models import SubCategory
from .forms import ContactForm

from wsgiref.util import FileWrapper
import os
import mimetypes
import pathlib


def home_view(request):

    s = process_search(request)
    if s:
        return HttpResponseRedirect(s)

    # check for quote items for badge
    if request.session.get("quote_items", False):
        num_quotes = len(request.session["quote_items"])
    else:
        request.session["quote_items"] = []
        num_quotes = 0

    context = {"num_quotes": num_quotes, "autocomplete_choices": Product.objects.all()}

    return render(request, 'home.html', context)


def product_view(request, sub_category=""):

    s = process_search(request)
    if s:
        return HttpResponseRedirect(s)
    request.session.flush()

    d = {}
    products = []
    selected_category = ""
    categories = Category.objects.all()
    # check for quote items for badge
    if request.session.get("quote_items", False):
        num_quotes = len(request.session["quote_items"])
    else:
        request.session["quote_items"] = []
        num_quotes = 0

    # build list of categories for product ranges
    for item in categories:
        try:
            subs_bycat = list(SubCategory.objects.filter(cat=item.id))
            d[item.name] = subs_bycat
        except:
            d[item.name] = []

    # if the page requests that a subcategory be displayed, send its products to context
    if sub_category and sub_category != "none":
        sub_category = sub_category.replace("_", " ")
        sc_object = SubCategory.objects.filter(name=sub_category).first()
        if sc_object:
            products = list(Product.objects.filter(subcat=sc_object.id))
            selected_category = sc_object.cat.name
        else:
            selected_category = "none"
    elif sub_category == 'none':
        selected_category = 'none'

    # if a product is added to the quote, update in the session info
    if request.method == 'POST':
        quantity = request.POST.get("quant")
        size = request.POST.get("size")
        product = request.POST.get("product_id")
        if quantity == "Quantity":
            quantity = 1
        if size != "Sizes Available":
            # if duplicate, update quantity
            duplicate = False
            for item in request.session["quote_items"]:
                if item["pid"] == product:
                    item["quant"] = quantity
                    duplicate = True
                    break
            # otherwise, add it to the quote
            if not duplicate:
                quote_item = {"pid": product, "size": size, "quant": quantity}
                request.session["quote_items"].append(quote_item)
                request.session.modified = True
                num_quotes += 1

    context = {"categories": d, "products": products, "selected_category": selected_category, "num_quotes": num_quotes,
               "autocomplete_choices": Product.objects.all()}

    return render(request, 'products.html', context)


def faq_view(request):

    s = process_search(request)
    if s:
        return HttpResponseRedirect(s)

    # check for quote items for badge
    if request.session.get("quote_items", False):
        num_quotes = len(request.session["quote_items"])
    else:
        request.session["quote_items"] = []
        num_quotes = 0

    context = {"num_quotes": num_quotes, "autocomplete_choices": Product.objects.all()}

    return render(request, 'faq.html', context)


def cart_view(request, item_to_remove=""):

    s = process_search(request)
    if s:
        return HttpResponseRedirect(s)

    # check for quote items for badge
    if request.session.get("quote_items", False):
        print("here")
        if item_to_remove:
            request.session["quote_items"] = [x for x in request.session["quote_items"] if
                                              not x["pid"] == item_to_remove]
            request.session.modified = True

        # build the quote number
        num_quotes = len(request.session["quote_items"])
        if num_quotes:
            quote_items_4template = request.session["quote_items"]
        else:
            quote_items_4template = []
    else:
        quote_items_4template = []
        request.session["quote_items"] = []
        num_quotes = 0

    if request.method == "POST":
        # update any changes made to the cart in the session information
        i = 0
        for item in request.session["quote_items"]:
            id = item["pid"]
            new_size = request.POST.get("select-size-" + id)
            print(new_size)
            if new_size != item["size"]:
                request.session["quote_items"][i]["size"] = new_size
                request.session.modified = True
            new_quant = request.POST.get("select-quantity-" + id)
            if new_quant != item["quant"]:
                request.session["quote_items"][i]["quant"] = new_quant
                request.session.modified = True
            i += 1

        form = ContactForm()
    else:
        form = ""

        # render the contact form

    context = {"num_quotes": num_quotes, "quote_items": quote_items_4template, "form": form,
               "autocomplete_choices": Product.objects.all()}

    if item_to_remove:
        return redirect("/cart")
    else:
        return render(request, 'cart.html', context)


def send_view(request):
    # check for quote items for badge
    if request.session.get("quote_items", False):
        num_quotes = len(request.session["quote_items"])
        if num_quotes:
            quote_items_4template = request.session["quote_items"]
        else:
            quote_items_4template = []
    else:
        quote_items_4template = []
        request.session["quote_items"] = []
        num_quotes = 0

    context = {"num_quotes": num_quotes, "autocomplete_choices": Product.objects.all()}

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            item_str = ""

            quote_items = request.session["quote_items"]
            i = 0
            for item in quote_items:
                p_obj = Product.objects.filter(id=item["pid"]).first()
                item_str += f"Item {str(i)}: {p_obj.name} | Size: {item['size']}, Quantity: {item['quant']} \n"
                i += 1

            msg = f'Quote from {name}.\n At: {email}.\n Items: \n' + item_str + " \n" + message

            send_mail(
                subject='Quote Request',
                message=msg,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.RECIPIENT_ADDRESS, email])

            request.session.flush()

        # else go back to cart but with a bound form
        else:
            return render(request, 'cart.html', {"num_quotes": num_quotes,
                                                 "quote_items": quote_items_4template, "form": form,
                                                 "autocomplete_choices": Product.objects.all()})

    # not POST? you shouldn't be here. get out
    else:
        return redirect("/")

    return render(request, 'sent.html', context)


def download_file(request, product_id):
    the_file = Product.objects.filter(id=product_id).first()
    if the_file:
        filepath = the_file.schematic.url
        filepath = str(settings.BASE_DIR) + "\\" + "csf" + "\\" + filepath
        full_filepath = pathlib.PurePath(filepath)
        filename = os.path.basename(full_filepath)
        chunk_size = 8192
        response = StreamingHttpResponse(
            FileWrapper(
                open(full_filepath, "rb"),
                chunk_size,
            ),
            content_type=mimetypes.guess_type(full_filepath)[0],
        )
        response["Content-Length"] = os.path.getsize(full_filepath)
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
    else:
        return render(request, 'product.html')


def process_search(request):
    base_path = request.get_full_path()
    base_path.split("/")
    print(base_path)

    if request.method == "POST" and request.POST.get('search', False):
        product = request.POST.get('search')
        product_cat = Product.objects.filter(name=product)
        if product_cat:
            product_cat = product_cat.first().subcat.name.replace(" ", "_")
            return f"http://{request.get_host()}/products/{product_cat}"
        elif product[0:4].lower() == "csf-":
            for obj in Product.objects.all():
                for size in obj.sizes:
                    if size.lower().find(product) != -1:
                        return f"http://{request.get_host()}/products/{obj.subcat.name.replace(' ', '_')}"
            return f"http://{request.get_host()}/products/none"
        else:
            return f"http://{request.get_host()}/products/none"

    return 0
