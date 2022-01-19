from django import forms
from django.core import validators
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from users.models import Property_registration, Request_Property, Payment_report

from property.models import Test

User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'password': 'password must match'})
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,
                                 error_messages={'password': 'password must match'})

    class Meta:
        model = User
        fields = ['phone_number', 'name', 'user_login', 'user_image', 'password', 'password_2']

    def clean_phone(self):
        '''
        Verify phone is available.
        '''
        phone_number = self.cleaned_data.get('phone_number')
        qs = User.objects.filter(phone_number=phone_number)
        if qs.exists():
            raise forms.ValidationError("phone number  is taken")
        return phone_number

    def clean(self):
        # verify both password
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['phone_number']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['name', 'phone_number', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# create form for properties

class Register_property_Form(forms.ModelForm):
    class Meta:
        model = Property_registration

        fields = ['property_name', 'amount_per_month', 'detail', 'location', 'property_type', 'property_image']


# create form for request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request_Property
        fields = ('status_view',)


class Payment_report_Form(forms.ModelForm):
    class Meta:
        model = Payment_report
        fields = ('amount_paid',)
