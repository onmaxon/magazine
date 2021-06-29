from shop import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('contact/', mainapp.contact, name='contact'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('', include('social_django.urls', namespace='social')),
    path('order/', include('ordersapp.urls', namespace='order')),
    # path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
