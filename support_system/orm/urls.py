"""orm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^delBook/(\d+)', views.delBook),
    url(r'^editBook/(\d+)', views.editBook),
    url(r'^addBook/', views.addBook),
    url(r'^authorindex/', views.authorindex),
    url(r'^delAuthor/(\d+)', views.delAuthor),
    url(r'^addAuthor/', views.addAuthor),
    url(r'^editAuthor/(\d+)', views.editAuthor),
    url(r'^publishIndex/', views.publishIndex),
    url(r'^addPublish/', views.addPublish),
    url(r'^delPublish/(\d+)', views.delPublish),
    url(r'^editPublish/(\d+)', views.editPublish),
    url(r'^logout/', views.log_out),
    url(r'^reg/', views.reg),

]
