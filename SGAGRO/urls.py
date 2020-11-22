"""SGAGRO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from  django.conf import  settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import  url, include
from security.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('security.urls', 'security'), namespace='security')),
    path('catalog/',include(('catalog.urls','catalog'),namespace='catalog')),
    path('sale/',include(('sale.urls','sale'),namespace='sale')),
    path('purchase/',include(('purchase.urls','purchase'),namespace='purchase')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)