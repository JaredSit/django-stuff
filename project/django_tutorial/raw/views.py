from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.http import JsonResponse
from .models import *
from .forms import *

try:
    notify = Notification.objects.first()
except:
    notify = ''

try:
    operations = Operation.objects.first()
except:
    operations = ''

# Create your views here.
def home(request):
    return render(request, 'index.html', {
        'notify':notify,
        'operations':operations,
    })
def challenges(request):
    challenges = Challenge.objects.all()
    participant = None
    solved_challenge_ids = []
    #if request.user.is_authenticated:
        #participant = Participant.objects.get(user=request.user)
        #solved_challenge_ids = participant.flags_solved.values_list('id',flat=True)

        #print(f"Participant {participant}, Type: {type(participant)}")
        #print(f"Solved Challenges: {solved_challenge_ids}")

    return render(request, 'challenges.html', {
        'challenges': challenges,
        'participant': participant,
        'solved_challenge_ids': solved_challenge_ids,
        'notify':notify,
        'operations':operations,
    })
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    return render(request, 'challenge_details.html',{
        'challenge': challenge,
        'notify':notify,
        'operations':operations,
    })
def start_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    participant,created = Participant.objects.get_or_create(user=request.user)

    completion,created = ChallengeCompletion.objects.get_or_create(
        participant=participant,
        challenge=challenge
    )

    if not completion.start_time():
        completion.start_time = timezone.now()
        completion.save()
        return JsonResponse({
            'status': "success",
            'message': "Challenge Started!",
            'notify':notify,
            'operations':operations,
        })
    
    return JsonResponse({
        'status': "exists",
        'message': "Challenge Already Started!",
        'notify':notify,
        'operations':operations,
    })
def games(request):
    return render(request, 'games.html',{
        'notify':notify,
        'operations':operations,
    })
def challengeform(request):

    #If they pressed the submit button
    if request.method == 'POST':
        form = ChallengeForm(request.POST)

        #Is the form valid
        if form.is_valid():
            form.save() #Save form data into the database with the correct fields
            messages.success(request, "Challenge Created!")
            return render(request, 'challengeform.html', {'form': form})

    #If they didn't submit the form, just display the empty form
    else:
        form = ChallengeForm()
    return render(request, 'challengeform.html', {
        'form':form,
        'notify':notify,
        'operations':operations,
    })

def participants(request):
    participants = Participant.objects.all()
    return render(request, 'participants.html', {
        'participants': participants,
        'notify':notify,
        'operations':operations,
    })
def flagsubmit(request):
    if request.method == 'POST':
        form = FlagForm(request.POST)
        if form.is_valid():
            flag_value = form.cleaned_data['flag_value']
            try:
                challenge = Challenge.objects.get(flag_value=flag_value)
                participant = Participant.objects.get(user=request.user)

                completion,created = ChallengeCompletion.objects.get_or_create(participant=participant, challenge=challenge)
                if not completion.start_time:
                    messages.error(request, "Start time is missing. Try refreshing the challenge page.")
                    return redirect('submit_flag',{
                        'notify':notify,
                        'operations':operations,
                    })
                
                if challenge not in participant.flags_solved.all():
                    participant.flags_solved.add(challenge)
                    participant.update_points()
                    completion.timestamp = timezone.now()
                    time_taken = completion.timestamp - completion.start_time
                    completion.save()

                    messages.success(request, f"Flag submitted sucessfully! You earned {challenge.points} points.")
                else:
                    messages.error(request, f"You have already submitted this flag.")
            except Challenge.DoesNotExist:
                messages.error(request, "Invalid flag. Please try again.")
    else:
        form = FlagForm()
    
    return render(request, 'flagsubmit.html',{
        'form':form,
        'notify':notify,
        'operations':operations,
    })
def leaderboard(request):
    participants = Participant.objects.all().order_by('-total_points')
    current_user_flags = request.user.participant.flags_solved.all()
    return render(request, 'leaderboard.html',{
        'participants':participants,
        'current_user_flags':current_user_flags,
        'notify':notify,
        'operations':operations,
    })
def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html',{
        'form':form,
        'notify':notify,
        'operations':operations,
    })