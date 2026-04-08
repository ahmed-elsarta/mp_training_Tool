from django.shortcuts import render
from django.http import JsonResponse
from apps.content.models import Language, MinimalPair
def landing(request):
    languages = Language.objects.all()
    return render(request, 'core/landing.html', {'languages': languages})

def minimal_pairs_by_language(request, language_id):
    pairs = MinimalPair.objects.filter(language_id=language_id).values(
        'id', 'sound_1', 'sound_2'
    )
    return JsonResponse({'minimal_pairs': list(pairs)})