
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
=======
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
>>>>>>> servidor/master

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.cardapio.urls')),
    path('', include('apps.usuarios.urls')),
    path('pedido/', include('apps.pedido.urls')),
    path('painel/', include('apps.painel.urls')),
<<<<<<< HEAD
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> servidor/master
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
