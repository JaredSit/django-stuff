from django.urls import path
from .views import *
from .models import *

urlpatterns = [
    path('', views.home, name='home'),
    path('challenges/',views.challenges, name='challenges'),
    path('challengesform/',views.challengesform, name="challengesform"),

]