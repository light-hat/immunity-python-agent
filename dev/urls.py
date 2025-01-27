"""dev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.http import HttpResponse
from django.urls import path
import pickle
import yaml


def call_me(request):
    a = 1
    b = request.GET.get("a")
    c = "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
    e = "INSERT INTO users (name) VALUES ('John')"
    q = a + b
    print(e)

    return HttpResponse("Hello World")

def vulnerable_view_1(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        # Десериализуем данные с помощью pickle
        deserialized_data = pickle.loads(data)
        return HttpResponse(f'Deserialized data: {deserialized_data}')
    else:
        return HttpResponse("Method not allowed")

def vulnerable_view_2(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        # Десериализуем данные с помощью yaml
        deserialized_data = yaml.load(data, Loader=yaml.FullLoader)
        return HttpResponse(f'Deserialized data: {deserialized_data}')
    else:
        return HttpResponse("Method not allowed")

class VulnerableObject:
    def __reduce__(self):
        return (eval, ("__import__('os').system('ls')",))

def vulnerable_view_3(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        try:
            deserialized_data = pickle.loads(data.encode())
            return HttpResponse(f'Deserialized object: {deserialized_data}')
        except Exception as e:
            return HttpResponse(f'Error: {e}')
    else:
        return HttpResponse("Method not allowed")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("call_me/", call_me),
    path("/deserialize/4/", vulnerable_view_1),
    path("/deserialize/5/", vulnerable_view_2),
    path("/deserialize/6/", vulnerable_view_3),
]
