"""
URL configuration for FinalYearProject project.

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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home),
    path("about.html/", views.about),
    path("contact.html/", views.contact),
    path("loans.html/", views.loan),
    path("admin.html/", views.admin),
    path("admin.html/viewtrans.html/", views.viewtrans, name='viewtrans'),
    path("pradhanmantriyojna.html/", views.pradhan),
    path("clcss.html/", views.clcss),
    path("Insurance.html/", views.Insurance),
    path("demat.html/", views.demat),
    path("user.html/", views.user),
    path("user.html/register.html/", views.register),
    path("user.html/register.html/subregister", views.subregister),
    path("user.html/login.html/", views.login),
    path("user.html/login.html/changepin.html/", views.changepin, name='changepin' ),
    path("user.html/login.html/fundtrans.html/", views.fundtrans, name='fundtrans'),
    path("user.html/login.html/fundtrans.html/submit", views.submit, name='submit'),
    path("user.html/login.html/fundtrans.html/fundform.html/", views.fundform, name='fundform'),
    path("user.html/login.html/fundtrans.html/fundform.html/my_view", views.my_view, name='my_view'),
    path("user.html/login.html/fundtrans.html/fundform.html/my_view", views.my_view, name='my_view'),


]
