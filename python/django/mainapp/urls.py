from django.urls import path
from . import views

# TODO: Trailing slash issue

urlpatterns = [
    path('', views.index, name="index"),
    path('info/', views.info, name="info of all data"),
    path('go/<str:id>', views.go, name="go to page"),
    path('shortenurl/', views.shortenurl, name="generate new url"),
]
