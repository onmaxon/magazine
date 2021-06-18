
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm
from adminapp.forms import ProductCategoryEditForm
from adminapp.forms import ProductEditForm


# for class
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator


# class UsersListView(ListView):
#     model = ShopUser
#     template_name = 'adminapp/users.html'
#
#     # @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     # def dispatch(self, *args, **kwargs):
#     #     return super().dispatch(*args, **kwargs)
#     #
#     # def get_queryset(self):
#     #     self.get_queryset().filter(is_active=True)
#     #
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['title'] = 'админка.пользователи'
#     #     return context


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = "админка / пользователи"

    users_list = ShopUser.objects.all()
    content = {
        'title': title,
        'objects': users_list,
    }
    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = "пользователи / создание"

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {'title': title, 'update_form': user_form}
    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = "пользователи / редактирование"

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {'title': title, 'update_form': edit_form}
    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = "пользователи / удаление"
    user_item = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        if user_item.is_active:
            user_item.is_active = False
        else:
            user_item.is_active = True
        user_item.save()
        # Полное удаление из базы
        # user_item.delete()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user_item}
    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = "админка / категории"
    categories_list = ProductCategory.objects.all()
    content = {
        'title': title,
        'objects': categories_list,
    }
    return render(request, 'adminapp/categories.html', content)

#
# class ProductCategoryCreateView(CreateView):
#     model = ProductCategory
#     template_name = 'adminapp/category_update.html'
#     success_url = reverse_lazy('admin:categories')
#     fields = '__all__'
#     # form_class = ProductCategoryEditForm


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = "категории / создание"

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST)

        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm()

    content = {'title': title, 'update_form': category_form}
    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = "категории / редактирование"

    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, instance=edit_category)

        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm(instance=edit_category)

    content = {'title': title, 'update_form': category_form}
    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = "категории / удаление"
    category_item = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        if category_item.is_active:
            category_item.is_active = False
        else:
            category_item.is_active = True
        category_item.save()
        # Полное удаление из базы
        # user_item.delete()
        return HttpResponseRedirect(reverse('admin:categories'))

    content = {'title': title, 'category_to_delete': category_item}
    return render(request, 'adminapp/category_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = "админка / продукты"
    category_item = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category=category_item)
    content = {
        'title': title,
        'category': category_item,
        'objects': products_list,
    }
    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = "админка / создание"

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[category.pk]))
    else:
        edit_form = ProductEditForm()

    content = {'title': title,
               'update_form': edit_form,
               'category': category
    }
    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = "продукт / подробнее"
    product = get_object_or_404(Product, pk=pk)
    content = {
        'title': title,
        'object': product,
    }
    return render(request, 'adminapp/product_read.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = "продукт / редактирование"

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {'title': title, 'update_form': edit_form, 'category': edit_product.category}
    return render(request, 'adminapp/product_update.html', content)
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = "продукт / удаление"

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        # Полное удаление из базы
        # product.delete()
        return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))

    content = {'title': title, 'product_to_delete': product}
    return render(request, 'adminapp/product_delete.html', content)
