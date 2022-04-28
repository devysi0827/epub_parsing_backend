from django.urls import path
from . import views


urlpatterns = [
    path('opf/', views.opfController),
    path('find/', views.findFile),
    path('image/', views.imageController),

]

