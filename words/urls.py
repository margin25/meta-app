from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('<str:word>', views.wordpage, name="wordpage"),
]