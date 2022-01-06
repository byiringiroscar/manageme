from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from codes.forms import CodeForm
from users.models import User, Request_Property
from .utilis import send_sms
from users.forms import UserForm, TestForm
from django.contrib.auth.forms import UserCreationForm
from users.models import Property_registration
from django.contrib.auth.decorators import login_required
from users.forms import Register_property_Form
from django.db.models import Q
from users.forms import RequestForm
from django.utils import timezone

now = timezone.now()


# Create your views here.

def home(request):
    return render(request, 'html/index.html')


def sign_in(request):
    form = AuthenticationForm
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.user_login == 'lessor':
            request.session['pk'] = user.pk

            return redirect('verify-view')
        elif user is not None and user.user_login == 'tenant':
            request.session['pk'] = user.pk
            return redirect('verify-tenant')

    return render(request, 'html/signin.html', {'form': form})


def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.name}: {user.code}"
        if not request.POST:
            print(code_user)
            print(user.user_login)
            # send code through twillio

            # send_sms(code_user, user.phone_number)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('sign_in')

    return render(request, 'html/verify_cre.html', {'form': form})


def verify_tenant(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.name}: {user.code}"
        if not request.POST:
            print(code_user)
            # send code to phone through twillio

            # send_sms(code_user, user.phone_number)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('tenant')
            else:

                return redirect('sign_in')

    return render(request, 'html/verify_cre.html', {'form': form})


def sign_up(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sign_in')
        else:
            return redirect('sign_up')
    context = {
        'form': form
    }

    return render(request, 'html/signup.html', context)


# @login_required
def lessor(request):
    user = request.user
    request_property_all = Request_Property.objects.filter(owner_name=user).filter(status_view='request').order_by(
        '-id')
    property_car_count = Property_registration.objects.filter(owner_name=user).filter(property_type='car').count()
    property_land_count = Property_registration.objects.filter(owner_name=user).filter(property_type='land').count()
    property_house_count = Property_registration.objects.filter(owner_name=user).filter(property_type='house').count()
    property_other_count = Property_registration.objects.filter(owner_name=user).filter(property_type='other').count()
    car_used_tenant = Request_Property.objects.filter(property_requested__owner_name=user).filter(
        property_requested__property_type='car').filter(status_view='approved').count()
    other_used_tenant = Request_Property.objects.filter(property_requested__owner_name=user).filter(
        property_requested__property_type='other').filter(status_view='approved').count()
    land_used_tenant = Request_Property.objects.filter(property_requested__owner_name=user).filter(
        property_requested__property_type='land').filter(status_view='approved').count()
    house_used_tenant = Request_Property.objects.filter(property_requested__owner_name=user).filter(
        property_requested__property_type='house').filter(status_view='approved').count()
    context = {
        'property_car': property_car_count,
        'property_land': property_land_count,
        'property_house': property_house_count,
        'property_other': property_other_count,
        'user': user,
        'notification': request_property_all,
        'used_car': car_used_tenant,
        'used_other': other_used_tenant,
        'used_land': land_used_tenant,
        'used_house': house_used_tenant,
    }

    return render(request, 'html/lessor.html', context)


# car tenant approved
def car_tenant_approved(request):
    user = request.user
    tenant_property_approved = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='car')

    context = {
        'car_approved': tenant_property_approved,
    }
    return render(request, 'html/car_tenant_approved.html', context)


# house tenant approved
def house_tenant_approved(request):
    user = request.user
    tenant_property_approved = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='house')

    context = {
        'house_approved': tenant_property_approved,
    }
    return render(request, 'html/house_tenant_approved.html', context)


# land tenant approved
def land_tenant_approved(request):
    user = request.user
    tenant_property_approved = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='land')

    context = {
        'land_approved': tenant_property_approved,
    }
    return render(request, 'html/land_tenant_approved.html', context)


# other tenant approved
def other_tenant_approved(request):
    user = request.user
    tenant_property_approved = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='other')

    context = {
        'other_approved': tenant_property_approved,
    }
    return render(request, 'html/other_tenant_approved.html', context)


@login_required
def tenant(request):
    user = request.user
    view_request_made = Request_Property.objects.filter(user_request=user).order_by('-id')
    car_renting = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='car').count()
    house_renting = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='house').count()
    land_renting = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='land').count()
    other_renting = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='other').count()
    # notification related with denied and approve request
    all_notification_deny_and_approve = Q(Q(status_view='approved') | Q(status_view='denied'))
    request_property_all_deny_approve = Request_Property.objects.filter(all_notification_deny_and_approve).filter(
        user_request=user).order_by('-id')

    context = {
        'user': user,
        'notification': view_request_made,
        'car_renting': car_renting,
        'house_renting': house_renting,
        'land_renting': land_renting,
        'other_renting': other_renting,
        # notification related with deny and approving
        'notification_all': request_property_all_deny_approve,

    }
    return render(request, 'html/tenant.html', context)


@login_required
def post_property(request):
    form = Register_property_Form()
    if request.method == 'POST':
        form = Register_property_Form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner_name = request.user
            form.save()
            return redirect('dashboard')
        else:
            form = Register_property_Form()
    context = {
        'form': form
    }
    return render(request, 'dashboard-owner/register_property.html', context)


@login_required
def view_property_car(request):
    user = request.user
    car_property = Property_registration.objects.filter(property_type='car').filter(owner_name=user)
    context = {
        'car_detail': car_property
    }
    return render(request, 'html/view_car.html', context)


@login_required
def view_property_others(request):
    user = request.user
    other_property = Property_registration.objects.filter(property_type='other').filter(owner_name=user)
    context = {
        'other_detail': other_property
    }
    return render(request, 'html/view_other.html', context)


@login_required
def view_property_land(request):
    user = request.user
    land_property = Property_registration.objects.filter(property_type='land').filter(owner_name=user)
    context = {
        'land_detail': land_property
    }
    return render(request, 'html/view_land.html', context)


@login_required
def view_property_house(request):
    user = request.user
    house_property = Property_registration.objects.filter(property_type='house').filter(owner_name=user)
    context = {
        'house_detail': house_property
    }
    return render(request, 'html/view_house.html', context)


# view property full detail
def view_property_detail(request, pk):
    user = request.user
    Property_detail = get_object_or_404(Property_registration, id=pk)
    Property_detail_id = Property_detail.id
    view_tenant_in_property = Request_Property.objects.filter(status_view='approved').filter(
        property_requested__id=Property_detail_id)

    context = {
        'prop_detail': Property_detail,
        'property_tenant': view_tenant_in_property,

    }
    return render(request, 'html/view_property_detail.html', context)


# view property full detail tenant from search
def view_property_detail_tenant(request, pk):
    user = request.user
    Property_detail = get_object_or_404(Property_registration, id=pk)
    remove_btn_request = Request_Property.objects.filter(property_requested=Property_detail)
    remove_btn_user = Request_Property.objects.filter(user_request=user)

    context = {
        'prop_detail': Property_detail,
        'remove_request': remove_btn_request,
        'remove_btn_user': remove_btn_user,

    }
    return render(request, 'html/view_property_detail_tenant.html', context)


# search function area for lessor
@login_required
def search_property(request):
    user = request.user
    if request.method == 'POST':
        searched = request.POST['searched']
        search_prop = Property_registration.objects.filter(property_name__contains=searched)

        context = {
            'searched': searched,
            'search_prop': search_prop
        }
        return render(request, 'html/search_property.html', context)
    else:
        return render(request, 'html/search_property.html')


# search area for tenant
@login_required
def search_property_tenant(request):
    if request.method == 'POST':
        q = request.POST['q']

        multiple_q = Q(Q(property_name__icontains=q) | Q(owner_name__phone_number__icontains=q))
        search_prop = Property_registration.objects.filter(multiple_q).filter(available=True)

        context = {

            'search_prop': search_prop
        }
        return render(request, 'html/search_property_tenant.html', context)
    else:
        return render(request, 'html/search_property_tenant.html')


# request area
@login_required
def request_pro(request, pk):
    requesting_property = get_object_or_404(Property_registration, pk=pk)
    user = request.user
    form = RequestForm(request.POST or None)
    # if request.method == 'POST':
    instance = form.save(commit=False)
    instance.user_request = user
    instance.property_requested = requesting_property
    instance.owner_name = requesting_property.owner_name
    instance.status_view = 'request'
    instance.time_done = now
    instance.save()

    context = {
        'form': form
    }
    return redirect('tenant')


def notification_detail(request, id):
    notification_det = Request_Property.objects.filter(pk=id)
    context = {
        'notification': notification_det
    }
    return render(request, 'html/notification_profile.html', context)


# view all notification lessor
def all_notification_lessor(request):
    user = request.user
    request_property_all = Request_Property.objects.filter(owner_name=user).filter(status_view='request').order_by(
        '-id')
    context = {
        'notification': request_property_all
    }

    return render(request, 'html/all_notification_lessor.html', context)


# view all notification tenant
def all_notification_tenant(request):
    user = request.user
    all_notification_deny_and_approve = Q(Q(status_view='approved') | Q(status_view='denied'))
    request_property_all_deny_approve = Request_Property.objects.filter(all_notification_deny_and_approve).filter(
        user_request=user).order_by('-id')
    print('not all:', request_property_all_deny_approve)
    context = {
        'notification_tenant': request_property_all_deny_approve
    }
    return render(request, 'html/all_notification_tenant.html', context)


# section to decline request you made on property
def decline_request_property(request, pk):
    user = request.user
    Property_detail = get_object_or_404(Property_registration, id=pk)
    user_who_requested = Request_Property.objects.filter(user_request=user).filter(property_requested=Property_detail)

    user_who_requested.delete()

    return redirect("tenant")


# section to see all request  for tenant
def view_request_tenant_all(request):
    user = request.user
    view_request_made = Request_Property.objects.filter(user_request=user).order_by('-id')
    context = {
        "notification": view_request_made
    }
    return render(request, 'html/view_request_tenant_all.html', context)


# section to approve property
def view_request_tenant_detail(request, id):
    user = request.user
    request_tenant_detail = Request_Property.objects.filter(pk=id)
    Property_detail = Property_registration.objects.filter(pk=id)
    user_who_requested = Request_Property.objects.filter(user_request=user).filter(
        property_requested=Property_detail)  ## error
    context = {
        'notification': request_tenant_detail,
        'user_who_requested': user_who_requested,

    }
    return render(request, 'html/view_request_tenant_detail.html', context)


def approve_property(request, pk):
    property_to_approve = get_object_or_404(Request_Property, pk=pk)
    prop_to = property_to_approve.property_requested.id
    form = RequestForm(request.POST or None, instance=property_to_approve)
    instance = form.save(commit=False)
    instance.property_requested.available = False
    instance.status_view = 'approved'
    instance.time_done = now
    instance.save()
    Property_registration.objects.filter(pk=prop_to).update(available=False)
    return redirect('dashboard')


# deny tenant to use this property
def deny_property(request, pk):
    property_to_approve = get_object_or_404(Request_Property, pk=pk)
    form = RequestForm(request.POST or None, instance=property_to_approve)
    instance = form.save(commit=False)
    instance.status_view = 'denied'
    instance.time_done = now
    instance.save()
    return redirect('dashboard')


# view car renting property and payment options

def view_rent_car_detail(request, id):
    user = request.user
    tenant_property_approved = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='car').filter(pk=id)
    context = {
        'car_approved': tenant_property_approved,
    }
    return render(request, 'html/view_rent_car_detail.html', context)


def view_rent_house_detail(request, id):
    user = request.user
    tenant_property_approved = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='house').filter(pk=id)
    context = {
        'house_approved': tenant_property_approved,
    }
    return render(request, 'html/view_rent_house_detail.html', context)


def view_rent_land_detail(request, id):
    user = request.user
    tenant_property_approved = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='land').filter(pk=id)
    context = {
        'land_approved': tenant_property_approved,
    }
    return render(request, 'html/view_rent_land_detail.html', context)


def view_rent_other_detail(request, id):
    user = request.user
    tenant_property_approved = Request_Property.objects.filter(user_request=user).filter(status_view='approved').filter(
        property_requested__property_type='other').filter(pk=id)
    context = {
        'other_approved': tenant_property_approved,
    }
    return render(request, 'html/view_rent_other_detail.html', context)


def profile_tenant(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'html/profile_tenant.html', context)


# profile for lessor
def profile_lessor(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'html/profile_lessor.html', context)


def test_view(req):
    form = TestForm()
    if req.method == 'POST':
        form = TestForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TestForm()
    return render(req, 'html/test.html', {'form': form})
