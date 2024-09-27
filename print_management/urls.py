"""
URL configuration for print_management project.

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
from django.shortcuts import redirect
from django.urls import path
from django.conf.urls.static import static
from print_management import settings
from printers.views import CustomLoginView, CustomUserCreateView, CustomUserDetailView, CustomUserUpdateView, HomePageView, PrintJobCreateView, PrintJobListView, PrinterCreateView, PrinterUpdateView, UserListView, dashboard
from django.contrib.auth.views import (LogoutView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-user/', CustomUserCreateView.as_view(), name='create_user'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<slug:slug>/edit/', CustomUserUpdateView.as_view(), name='edit_user'),
    path('users/<slug:slug>/details/', CustomUserDetailView.as_view(), name='user_details'),
    # path('printers/', PrinterListView.as_view(), name='printers_list'),
    path('print/', PrintJobCreateView.as_view(), name='submit_print_job'),
    path('print/jobs/', PrintJobListView.as_view(), name='print_job_list'),
    path('printers/create/', PrinterCreateView.as_view(), name='create_printer'),
    path('printers/<slug:slug>/edit/', PrinterUpdateView.as_view(), name='edit_printer'),
    path('logout/', LogoutView.as_view(), name='logout')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
