import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-@a%z4jbv_6)4(*&82)$_$_da_9sb)d^qp*x1kgn&=kv5r8)af'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['172.155.0.7','0.0.0.0','localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.sites',
    'dynamic_raw_id',
    'django_select2',
    'proyectoApp',
    'pasajes',
    'depoapp',
    'personal',
    


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', '/proyectoApp/templates/','/var/www/djangoEjemplo/proyectoApp/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'proyecto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deposito',
        'USER': 'postgres',
        'PASSWORD': 'sistemasavp',
        'HOST': 'sysavp.chubut.gov.ar',
        'PORT': '33060',
    },
    'pasajes': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pasajes',
        'USER': 'postgres',
        'PASSWORD': 'sistemasavp',
        'HOST': '172.155.0.8',
        'PORT': '5432',
    },
    'personal':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'personal',
        'USER': 'postgres',
        'PASSWORD': 'sistemasavp',
        #'HOST': '172.155.0.8',
        #'PORT': '5432',
        'HOST': 'sysavp.chubut.gov.ar',
        'PORT': '33060',
    }
}
DATABASE_ROUTERS = ['proyecto.routerDeposito.RouterDeposito','proyecto.routerPasajes.RouterPasajes','proyecto.routerPersonal.RouterPersonal']

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
#Agrego conf para poder agregar imagenes

STATIC_URL = '/static/'

STATIC_ROOT = 'templates/'
#STATIC_ROOT = os.path.join(BASE_DIR, "allstaticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'proyectoApp/templates'),
    #os.path.join(BASE_DIR, '/var/www/djangoEjemplo/proyectoApp/templates'),
]

LOGIN_REDIRECT_URL = '/pasajes'

LOGOUT_REDIRECT_URL = '/'
