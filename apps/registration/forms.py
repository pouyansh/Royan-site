from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.registration.models import *


class SignUpOrganization(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpOrganization, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل"
        self.fields['email'].required = True
        self.fields['username'].label = "نام کاربری"
        self.fields['password1'].label = "رمز عبور"
        self.fields['password2'].label = "تکرار رمز عبور"
        self.fields['fax'].required = False

    class Meta:
        model = Organization
        fields = (
            'organization_name', 'post', 'submit_id', 'economic_id', 'email', 'phone_number', 'fax', 'address',
            'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        user_exists = Customer.objects.filter(username=username)
        if user_exists:
            raise forms.ValidationError("نام کاربری تکراری است.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user_exists = Customer.objects.filter(email=email)
        if len(user_exists) > 0:
            raise forms.ValidationError("ایمیل وارد شده تکراری است.")
        return email

    def clean_organization_name(self):
        org_name = self.cleaned_data['organization_name']
        user_exists = Organization.objects.filter(organization_name=org_name)
        if len(user_exists) > 0:
            raise forms.ValidationError("نام شرکت تکراری است.")
        return org_name

    def clean_economic_id(self):
        eid = self.cleaned_data['economic_id']
        user_exists = Organization.objects.filter(economic_id=eid)
        if user_exists:
            raise forms.ValidationError("شماره اقتصادی تکراری است.")
        return eid

    def clean_submit_id(self):
        sid = self.cleaned_data['submit_id']
        user_exists = Organization.objects.filter(submit_id=sid)
        if user_exists:
            raise forms.ValidationError("شماره ثبت تکراری است.")
        return sid


class SignUpPerson(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpPerson, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل"
        self.fields['email'].required = True
        self.fields['username'].label = "نام کاربری"
        self.fields['first_name'].label = "نام"
        self.fields['first_name'].required = True
        self.fields['last_name'].label = "نام خانوادگی"
        self.fields['last_name'].required = True
        self.fields['password1'].label = "رمز عبور"
        self.fields['password2'].label = "تکرار رمز عبور"
        self.fields['fax'].required = False

    class Meta:
        model = Person
        fields = (
            'first_name', 'last_name', 'national_id', 'education', 'org',
            'email', 'phone_number', 'cellphone_number', 'fax', 'address',
            'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        user_exists = Customer.objects.filter(username=username)
        if user_exists:
            raise forms.ValidationError("نام کاربری تکراری است.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user_exists = Customer.objects.filter(email=email)
        if len(user_exists) > 0:
            raise forms.ValidationError("ایمیل وارد شده تکراری است.")
        return email

    def clean_national_id(self):
        nid = self.cleaned_data['national_id']
        user_exists = Person.objects.filter(national_id=nid)
        if user_exists:
            raise forms.ValidationError("کد ملی تکراری است.")
        if len(str(nid)) != 10:
            raise forms.ValidationError("کد ملی باید 10 رقمی باشد.")
        return nid


class VerifyEmailForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(VerifyEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل"
        self.fields['username'].label = "نام کاربری"

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        customer = Customer.objects.filter(username=username, email=email)
        if len(customer) == 0:
            raise forms.ValidationError("حساب کاربری با این نام کاربری و ایمیل یافت نشد.")
        return super(VerifyEmailForm, self).clean()

    def raise_error(self):
        raise forms.ValidationError("نام کاربری وارد شده با لینک منطبق نمی‌باشد.")


class UpdateOrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateOrganizationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل"
        self.fields['email'].required = True
        self.fields['fax'].required = False

    class Meta:
        model = Organization
        fields = (
            'organization_name', 'post', 'submit_id', 'economic_id', 'email', 'phone_number', 'fax', 'address')

    def clean_email(self):
        organization = Organization.objects.get(email=list(self.initial.values())[0])
        email = self.cleaned_data['email']
        if organization.email != email:
            user_exists = Customer.objects.filter(email=email)
            if len(user_exists) > 0:
                raise forms.ValidationError("ایمیل وارد شده تکراری است.")
        return email

    def clean_organization_name(self):
        organization = Organization.objects.get(email=list(self.initial.values())[0])
        org_name = self.cleaned_data['organization_name']
        if organization.organization_name != org_name:
            user_exists = Organization.objects.filter(organization_name=org_name)
            if len(user_exists) > 0:
                raise forms.ValidationError("نام شرکت تکراری است.")
        return org_name

    def clean_economic_id(self):
        organization = Organization.objects.get(email=list(self.initial.values())[0])
        eid = self.cleaned_data['economic_id']
        if organization.economic_id != eid:
            user_exists = Organization.objects.filter(economic_id=eid)
            if user_exists:
                raise forms.ValidationError("شماره اقتصادی تکراری است.")
        return eid

    def clean_submit_id(self):
        organization = Organization.objects.get(email=list(self.initial.values())[0])
        sid = self.cleaned_data['submit_id']
        if organization.submit_id != sid:
            user_exists = Organization.objects.filter(submit_id=sid)
            if user_exists:
                raise forms.ValidationError("شماره ثبت تکراری است.")
        return sid
