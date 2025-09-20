"""
URL configuration for samlsample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, re_path, include
from samlsample.views import RootView, vulnerable_saml_acs, saml_sls_no_csrf, LoggedOutView, ToggleSignatureVerificationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('saml/acs/', vulnerable_saml_acs),
    path('saml/sls/', saml_sls_no_csrf),
    path('saml/', include('django_saml.urls')),
    path('logged-out/', LoggedOutView.as_view(), name="logged-out"),
    path('toggle-verification/', ToggleSignatureVerificationView.as_view(), name="toggle-verification"),
    path('', RootView.as_view(), name="index"),
]
