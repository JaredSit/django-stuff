from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.
def home(request):
    return render(request, "index.html")

def challenges(request):
    return render(request, "challenges.html")


def challengesform(request):
    if request.method =='POST':
        form = challengesform(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'challengesform.html', {'form':form,'success':True})

    else: 
        form = ChallengeForm



    return render(request,'challengesform.html', {'form':form})