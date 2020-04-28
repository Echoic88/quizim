"""quizim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import index
from home import urls as urls_index
from accounts import urls as urls_accounts
from quiz import urls as urls_quiz
from userarea import urls as urls_userarea
from store import urls as urls_store
from cart import urls as urls_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index),
    path('accounts/', include(urls_accounts)),
    path("home/", include(urls_index)),
    path("quiz/", include(urls_quiz)),
    path("userarea/", include(urls_userarea)),
    path("store/", include(urls_store)),
    path("cart/", include(urls_cart)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
