from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:landing')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:landing')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:landing')

@login_required
def profile(request):
    from apps.practice.models import Score
    raw_scores = Score.objects.filter(user=request.user).order_by('-session_date')

    scores = []
    for s in raw_scores:
        scores.append({
            'session_date':   s.session_date,
            'minimal_pair':   s.minimal_pair,
            'correct':        s.correct,
            'total':          s.total,
            'accuracy':       round((s.correct / s.total) * 100) if s.total > 0 else 0,
            'duration_chosen': s.duration_chosen,
        })

    return render(request, 'accounts/profile.html', {'scores': scores})