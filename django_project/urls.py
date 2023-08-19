"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from craft.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('sign',signup,name='sign'),
    path('login',handlelogin,name='login'),
    path('logout',handlelogout,name='logout'),
    path('activate/<uidb64>/<token>',ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email',RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',SetNewPasswordView.as_view(),name='set-new-password'),
    path('mainpage',mainpage,name='mainpage'),
    path('dreamcatchers',dreamcatchers,name='dreamcatchers'),
    #path('resinproducts',resinproducts,name='resinproducts'),
    path('gallery',gallery,name='gallery'),
    path('contact',contact,name='contact'),
    path('checkout', checkout, name="Checkout"),
    path('handlerequest', handlerequest, name="HandleRequest"),
    
    
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


