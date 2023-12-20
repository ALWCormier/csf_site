from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve


from . import views

app_name = 'csf'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('products', views.product_view, name='products'),
    path('products/<sub_category>/', views.product_view, name='products'),
    path('download/<int:product_id>', views.download_file, name='download_file'),
    path('cart', views.cart_view, name='cart'),
    path('cart/<item_to_remove>', views.cart_view, name='cart'),
    path('sent', views.send_view, name='sent'),
    path('faq', views.faq_view, name='faq'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
