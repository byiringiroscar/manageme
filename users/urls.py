from django.urls import path
from django.contrib.auth import views as auth_view
from . import views
from django.contrib.auth import views as auth_view

name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.sign_in, name='sign_in'),  # login
    path('logout', auth_view.LogoutView.as_view(), name='logout'),
    path('verify/', views.verify_view, name='verify-view'),  # check user code lessor
    path('verify_tenant/', views.verify_tenant, name='verify-tenant'),  # check user code tenant
    path('signup/', views.sign_up, name='sign_up'),  # sign up for new user
    path('dashboard/', views.lessor, name='dashboard'),  # dashboard for lessor
    path('tenant/', views.tenant, name='tenant'),  # dashboard for lessor
    path('register_property/', views.post_property, name='post_property'),
    # view property posted
    path('view_car/', views.view_property_car, name='view_car'),
    path('view_land/', views.view_property_land, name='view_land'),
    path('view_house/', views.view_property_house, name='view_house'),
    path('view_others/', views.view_property_others, name='view_others'),
    # search new lessor
    path('search_property/', views.search_property, name='search_property'),
    # search property for tenant
    path('search_property_tenant/', views.search_property_tenant, name='search_property_tenant'),
    # make request
    path('request_pro/', views.request_pro, name='request_pro'),
    path('test/', views.test_view, name='test'),


]

