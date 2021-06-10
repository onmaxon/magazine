from django.shortcuts import render, get_object_or_404
import os, datetime, json, random
from shop import settings
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def get_hot_product():
    products_list = Product.objects.all()
    # print(products_list)
    return random.sample(list(products_list), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products

def main(request):
    products = Product.objects.all()[:4]
    basket =get_basket(request.user)
    content = {'title': 'Магазин', 'products': products, 'basket': basket}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'Каталог'
    links_menu = ProductCategory.objects.all()
    basket =get_basket(request.user)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все'}
            products_list = Product.objects.all()
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_list,
            'basket': basket,
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    title = 'продукт'
    links_menu = ProductCategory.objects.all()
    product = get_object_or_404(Product, pk=pk)
    # basket = get_basket(request,user)
    content = {
        'title': title,
        'links_menu': links_menu,
        'product': product,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    basket =get_basket(request.user)

    locations = [
        {
            'city': 'Москва',
            'phone': '+7-888-888-8888',
            'email': 'info@geekshop.ru',
            'address': 'В пределах МКАД',
        },
        {
            'city': 'Екатеринбург',
            'phone': '+7-777-777-7777',
            'email': 'info_yekaterinburg@geekshop.ru',
            'address': 'Близко к центру',
        },
        {
            'city': 'Владивосток',
            'phone': '+7-999-999-9999',
            'email': 'info_vladivostok@geekshop.ru',
            'address': 'Близко к океану',
        },
    ]
    content = {'title': title, 'visit_date':visit_date, 'locations': locations, 'basket': basket}
    return render(request, 'mainapp/contact.html', content)
