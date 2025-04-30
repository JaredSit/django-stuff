from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('challenges/', views.challenges,name='challenges'),
    path('challenges/<int:challenge_id>/', views.challenge_detail,name='challenge_details'),
    path('start_challenge/<int:challenge_id>/', views.start_challenge,name='start_challenge'),
    path('games/',views.games,name='games'),
    path('challengeform/',views.challengeform,name='challengeform'),
    path('participants/',views.participants,name='participants'),
    path('flagsubmit/',views.flagsubmit,name='flagsubmit'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path('register/',views.registration,name='register')
]