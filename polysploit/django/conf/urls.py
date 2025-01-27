"""
URL configuration for conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

import pickle
from yaml import *
import base64
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from example.models import *

import sys
sys.setrecursionlimit(150000)

@csrf_exempt
def vulnerable_view_1(request):

    if request.method == 'POST':
        data = request.POST.get('data')
        decoded_data = base64.b64decode(data.encode('utf-8'))
        # Десериализуем данные с помощью pickle
        deserialized_data = pickle.loads(decoded_data)
        return HttpResponse(f'Deserialized data: {deserialized_data}')
    else:
        return HttpResponse("Method not allowed")

@csrf_exempt
def vulnerable_view_2(request):

    if request.method == 'POST':
        data = request.POST.get('data')
        # Десериализуем данные с помощью yaml
        deserialized_data = unsafe_load(data)
        return HttpResponse(f'Deserialized data: {deserialized_data}')
    else:
        return HttpResponse("Method not allowed")

def recursive_function(n):
    if n == 0:
        return 1
    else:
        return n * recursive_function(n - 1)

def vulnerable_resource(request):

    n = int(request.GET.get('n', '10'))
    result = recursive_function(n)
    return HttpResponse(f'Factorial of {n}: {result}')

def vulnerable_resource_2(request):

    num_reports = int(request.GET.get('num', '10'))
    for i in range(num_reports):
        report = Report()
        report.title = f'Report #{i}'
        report.content = 'Some content'
        report.save()

    return HttpResponse(f'{num_reports} reports generated')

def view_profile(request, profile_id):

    profile = get_object_or_404(UserProfile, id=profile_id)
    context = {
        'phone_number': profile.phone_number,
    }
    return HttpResponse(f'{context}')

def view_profile_patched(request, profile_id):

    profile = get_object_or_404(UserProfile, id=profile_id, user=request.user)
    context = {
        'phone_number': profile.phone_number,
    }
    return HttpResponse(f'{context}')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("deserialize/1/", vulnerable_view_1),
    path("deserialize/2/", vulnerable_view_2),
    path("resource/1/", vulnerable_resource),
    path("resource/2/", vulnerable_resource_2),
    path("profile/<int:profile_id>/", view_profile),
    path("get_profile/<int:profile_id>/", view_profile_patched),
]
