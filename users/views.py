from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from codes.forms import CodeForm
from users.models import User
from .utilis import send_sms
from users.forms import UserForm, TestForm
from django.contrib.auth.forms import UserCreationForm
from users.models import Property_registration
from django.contrib.auth.decorators import login_required
from users.forms import Register_property_Form
from django.db.models import Q


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

            send_sms(code_user, user.phone_number)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('sign_in')
    user_acti = request.user
    # context = {
    #         'form': form,
    #
    #
    #     }
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

            send_sms(code_user, user.phone_number)
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
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign_in')
        else:
            return redirect('sign_up')
    context = {
        'form': form
    }

    return render(request, 'html/signup.html', context)


@login_required
def lessor(request):
    user = request.user
    property_car_count = Property_registration.objects.filter(owner_name=user).filter(property_type='car').count()
    property_land_count = Property_registration.objects.filter(owner_name=user).filter(property_type='land').count()
    property_house_count = Property_registration.objects.filter(owner_name=user).filter(property_type='house').count()
    property_other_count = Property_registration.objects.filter(owner_name=user).filter(property_type='other').count()
    # property_count = property_filter.count()
    context = {
        'property_car': property_car_count,
        'property_land': property_land_count,
        'property_house': property_house_count,
        'property_other': property_other_count,
        'user': user
    }

    return render(request, 'html/lessor.html', context)


@login_required
def tenant(request):
    user = request.user
    context = {
        'user': user
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


# search function area for lessor
@login_required
def search_property(request):
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

        multiple_q = Q(Q(property_name__icontains=q) | Q(location__icontains=q))
        search_prop = Property_registration.objects.filter(multiple_q)

        context = {

            'search_prop': search_prop
        }
        return render(request, 'html/search_property_tenant.html', context)
    else:
        return render(request, 'html/search_property_tenant.html')


# request area
@login_required
def request_pro(request, pk):
    req = Property_registration.objects.get(id=pk)

    return render(request, 'html/tenant.html')


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
