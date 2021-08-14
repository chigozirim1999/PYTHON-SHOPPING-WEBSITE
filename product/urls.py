from django.urls import path, include

from . import views #importing the wviews from the same folder

urlpatterns = [
    #/home
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('colors/', views.colors, name='colors'),

]