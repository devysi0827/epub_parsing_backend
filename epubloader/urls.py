from django.urls import path
from . import views


urlpatterns = [
    path('getfile/', views.getfile),
    path('opf/', views.opfController),
    path('finder/', views.finder),
]

