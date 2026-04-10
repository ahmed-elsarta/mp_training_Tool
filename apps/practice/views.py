from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from apps.content.models import MinimalPair, Word
from .models import Score


def session(request, mp_id):
    minimal_pair = get_object_or_404(MinimalPair, id=mp_id)

    words = Word.objects.filter(
        minimal_pair=minimal_pair,
        partner__isnull=False,
        sound=minimal_pair.sound_1
    ).select_related('partner')

    pairs = []
    for w in words:
        pairs.append({
            'word': {
                'id': w.id,
                'text': w.text,
                'sound': w.sound,
                'audio_url': w.audio_file.url,
            },
            'partner': {
                'id': w.partner.id,
                'text': w.partner.text,
                'sound': w.partner.sound,
                'audio_url': w.partner.audio_file.url,
            },
        })

    context = {
        'minimal_pair': minimal_pair,
        'pairs':        json.dumps(pairs),
        'durations': [
            {'label': '1 minute',   'seconds': 60},
            {'label': '5 minutes',  'seconds': 300},
            {'label': '10 minutes', 'seconds': 600},
            {'label': '20 minutes', 'seconds': 1200},
        ]
    }
    return render(request, 'practice/session.html', context)

def results(request):
    correct  = request.GET.get('correct', 0)
    total    = request.GET.get('total', 0)
    duration = request.GET.get('duration', 0)

    percentage = round((int(correct) / int(total)) * 100) if int(total) > 0 else 0

    context = {
        'correct':    correct,
        'total':      total,
        'duration':   int(duration) // 60,   # convert seconds to minutes
        'percentage': percentage,
    }
    return render(request, 'practice/results.html', context)

@require_POST
def save_score(request):
    data = json.loads(request.body)

    Score.objects.create(
        user=request.user if request.user.is_authenticated else None,
        minimal_pair_id=data['minimal_pair_id'],
        correct=data['correct'],
        total=data['total'],
        duration_chosen=data['duration_chosen'],
    )

    return JsonResponse({'status': 'ok'})
