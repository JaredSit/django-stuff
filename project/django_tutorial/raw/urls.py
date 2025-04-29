from django.urls import path
from .views import *
from .models import *

urlpatterns = [
    path('', home, name='home'),
    path('challenges/', challenges, name='challenges'),
    path('challengesform/', challengesform, name="challengesform"),

]