"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('signup/',views.register,name='register'),
    path('login',views.user_login_no,name='login'),
    path('login/<slug:slug>/',views.user_login,name='login_param'),
    path('logout',views.user_logout,name='logout'),
    path('sell',views.sell,name='sell'),
    path('buy',views.buy,name='buy'),
    path('purchase/<int:pk>',views.purchase,name='purchase'),
    path('product/<int:pk>',views.productDetailView.as_view(),name='prodetail')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
