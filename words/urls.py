from django.urls import path
from . import views

# urls for each page
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path("homepage.html", views.homepage, name="homepage"),
    path("about.html", views.about, name="about"),
    path('<str:word>', views.wordpage, name="wordpage"),
    path('search/', views.get_search, name='get_search'),
]