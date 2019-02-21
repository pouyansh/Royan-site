from django.conf.urls import url
from django.urls import path

from apps.registration.views import *

urlpatterns = [
	path('login/', Login.as_view(), name='login'),
	path('register/', Register.as_view(), name='register'),
	path('login_success/', login_success, name="login_success"),
	path('logout/', log_out, name='logout'),
	path('change-password/', ChangePassword.as_view(), name='change_password'),
	path('edit_profile', EditProfile.as_view(), name='edit_profile'),
	url('verify/(?P<username>[0-9A-Za-z_\-]+)', verify_email, name='verify'),
	path('forget_password', ForgetPassword.as_view(), name='forget_password'),
	path('referral_code/', GetReferralCode.as_view(), name='referral-code'),
	url('reset_password/(?P<username>[0-9A-Za-z_\-]+)', reset_password, name='reset_password'),
]
