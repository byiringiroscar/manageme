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
    path('tenant/', views.tenant, name='tenant'),  # dashboard for tenant
    path('register_property/', views.post_property, name='post_property'),
    # view property posted
    path('view_car/', views.view_property_car, name='view_car'),
    path('view_land/', views.view_property_land, name='view_land'),
    path('view_house/', views.view_property_house, name='view_house'),
    path('view_others/', views.view_property_others, name='view_others'),
    # view property detail lessor
    path('view_property_detail/<int:pk>/', views.view_property_detail, name='view_property_detail'),
    # search new lessor
    path('search_property/', views.search_property, name='search_property'),
    # search property for tenant
    path('search_property_tenant/', views.search_property_tenant, name='search_property_tenant'),
    # view property detail from search in tenant
    path('view_property_detail_tenant/<int:pk>/', views.view_property_detail_tenant, name='view_property_detail_tenant'),
    # make request
    path('request_pro/<int:pk>/', views.request_pro, name='request_pro'),
    path('test/', views.test_view, name='test'),
    # view detail info for people who made request
    path('notification_detail/<int:id>/', views.notification_detail, name='notification_detail'),
    # view all notification
    path('all_notification_lessor/', views.all_notification_lessor, name='all_notification_lessor'),
    # view all notification tenant
    path('all_notification_tenant/', views.all_notification_tenant, name='all_notification_tenant'),
    # decline and delete request of property tenant made
    path('decline_request_property/<int:pk>/', views.decline_request_property, name='decline_request_property'),
    # view all request from tenant
    path('view_request_tenant_all/', views.view_request_tenant_all, name='view_request_tenant_all'),
    # view detail for request tenant made
    path('view_request_tenant_detail/<int:id>/', views.view_request_tenant_detail, name='view_request_tenant_detail'),
    # approve to use this property
    path('approve_property/<int:pk>/', views.approve_property, name='approve_property'),
    # denied to use this property
    path('deny_property/<int:pk>/', views.deny_property, name='deny_property'),
    # car approved by lessor
    path('car_tenant_approved/', views.car_tenant_approved, name='car_tenant_approved'),
    # house approved by lessor to tenant
    path('house_tenant_approved', views.house_tenant_approved, name='house_tenant_approved'),
    # land approved by lessor to tenant
    path('land_tenant_approved', views.land_tenant_approved, name='land_tenant_approved'),
    # other approved by lessor to tenant
    path('other_tenant_approved', views.other_tenant_approved, name='other_tenant_approved'),
    # View Renting car property and payment option
    path('view_rent_car_detail/<int:id>/', views.view_rent_car_detail, name='view_rent_car_detail'),
    # view renting house and payment option
    path('view_rent_house_detail/<int:id>/', views.view_rent_house_detail, name='view_rent_house_detail'),
    # view renting land and payment option
    path('view_rent_land_detail/<int:id>/', views.view_rent_land_detail, name='view_rent_land_detail'),
    # view renting other and payment option
    path('view_rent_other_detail/<int:id>/', views.view_rent_other_detail, name='view_rent_other_detail'),
    # profile tenant
    path('profile_tenant/', views.profile_tenant, name='profile_tenant'),
    # profile lessor
    path('profile_lessor/', views.profile_lessor, name='profile_lessor'),
    path('home_tenant/', views.home_tenant, name='home_tenant'),
    path('pay_rent_car/<int:id>/', views.pay_rent_car, name='pay_rent_car'),
    path('pay_rent_house/', views.pay_rent_house, name='pay_rent_house'),
    path('pay_rent_land/', views.pay_rent_land, name='pay_rent_land'),
    path('pay_rent_other/', views.pay_rent_other, name='pay_rent_other'),

    # payment
    path('payment_landlord/<int:pk>/', views.payment_landlord, name='payment_landlord'),



]

