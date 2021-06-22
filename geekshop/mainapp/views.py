from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import os, datetime, json, random
from shop import settings
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     else:
#         return []


def get_hot_product():
    # products_list = Product.objects.all()
    products_list = Product.objects.filter(category__is_active=True)
    # print(products_list)
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    # products = Product.objects.all()[:4]
    products = Product.objects.filter(category__is_active=True)[:4]

    # basket = get_basket(request.user)
    content = {'title': 'Магазин',
               'products': products,
               # 'basket': basket
               }
    return render(request, 'mainapp/index.html', content)

# Пагинотор
# def products(request, pk=None):
#     title = 'Каталог'
#     # links_menu = ProductCategory.objects.all()
#     links_menu = ProductCategory.objects.filter(is_active=True)
#     basket = get_basket(request.user)
#
#     if pk is not None:
#         if pk == 0:
#             category = {'pk': 0, 'name': 'все'}
#             products = Product.objects.all().order_by('price')
#         else:
#             category = get_object_or_404(ProductCategory, pk=pk)
#             products = Product.objects.filter(category__pk=pk)
#
#         content = {
#             'title': title,
#             'links_menu': links_menu,
#             'category': category,
#             'products': products,
#             'basket': basket,
#
#         }
#
#         if 'page' in request.GET:
#             page = request.GET.get('page')
#             paginator = Paginator(products, 2)
#             try:
#                 product_paginator = paginator.page(page)
#             except PageNotAnInteger:
#                 product_paginator = paginator.page(1)
#             except EmptyPage:
#                 product_paginator = paginator.page(paginator.num_pages)
#             content['products'] = product_paginator
#
#         return render(request, 'mainapp/products_list.html', content)
#
#     hot_product = get_hot_product()
#     same_products = get_same_products(hot_product)
#
#     content = {
#         'title': title,
#         'links_menu': links_menu,
#         'hot_product': hot_product,
#         'same_products': same_products,
#         'basket': basket,
#     }
#     return render(request, 'mainapp/products.html', content)


def products(request, pk=None, page=1):
    title = 'Каталог'
    # links_menu = ProductCategory.objects.all()
    links_menu = ProductCategory.objects.filter(is_active=True)
    # basket = get_basket(request.user)

    if pk is not None:
        if pk == 0:
            category = {'pk': 0, 'name': 'все'}
            products = Product.objects.all().order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk)

        paginator = Paginator(products, 4)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': product_paginator,
            # 'basket': basket,

        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        # 'basket': basket,
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
        # 'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    # basket = get_basket(request.user)

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
    content = {'title': title,
               'visit_date': visit_date,
               'locations': locations,
               # 'basket': basket
               }
    return render(request, 'mainapp/contact.html', content)
