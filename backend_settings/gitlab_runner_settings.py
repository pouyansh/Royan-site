from backend_settings.settings import *
import sys

DEBUG = False
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'asdproject',
		'USER': 'postgres',
		'PASSWORD': 'asdpassword',
		'HOST': 'postgres',
		'PORT': '5432',
	}
}
