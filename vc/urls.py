"""VMware URL Configuration

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
from views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^vminfo/', info_vm_basic),
    url(r'^publicinfo/', info_public_data),
    url(r'^action/',  vm_public_action),
    url(r'^createvm/', create_vms),
    url(r'^getCreateStatus/', get_VM_CreateStatus),
    url(r'^getvm/', get_vmName),
    url(r'^updateNetlabel/', update_netlabel),
    url(r'^updateDatastoreEsxi/', update_datastoreAndEsxi_relation),

]