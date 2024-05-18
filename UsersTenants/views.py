from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Home</h1>")

def inventory_list(request):
    return HttpResponse("<h1>Inventory</h1>")

def staff_list(request):
    return HttpResponse("<h1>Staff</h1>")
