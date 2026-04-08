from django.core.management.base import BaseCommand
from nltk.corpus import cmudict
from apps.content.models import Language, MinimalPair, Word


# Define which sound pairs to seed
TARGET_PAIRS = [
    ('B', 'P'),
    ('E', 'I'),
    ('L', 'R'),
    ('V', 'W'),
    ('N', 'NG'),
]

# How many word pairs to seed per minimal pair (keep it manageable)
MAX_PAIRS_PER_MP = 10


class Command(BaseCommand):
    help = 'Seed English minimal pairs from CMU Pronouncing Dictionary'

    def handle(self, *args, **kwargs):
        entries = cmudict.dict()

        # Get or create English language
        language, _ = Language.objects.get_or_create(name='English', code='en')
        self.stdout.write(f'Language: {language.name}')

        for sound_1, sound_2 in TARGET_PAIRS:
            self.stdout.write(f'\nProcessing: {sound_1} / {sound_2}')

            # Get or create the minimal pair
            mp, _ = MinimalPair.objects.get_or_create(
                language=language,
                sound_1=sound_1.lower(),
                sound_2=sound_2.lower(),
            )

            pairs_found = 0

            for word, pronunciations in entries.items():
                if pairs_found >= MAX_PAIRS_PER_MP:
                    break

                phonemes = pronunciations[0]  # use first pronunciation

                # Check if this word contains sound_1
                if sound_1 not in phonemes:
                    continue

                # Build the partner word by swapping sound_1 → sound_2
                partner_phonemes = [
                    sound_2 if p == sound_1 else p for p in phonemes
                ]

                # Find a real word matching those partner phonemes
                partner_word = None
                for candidate, candidate_pronunciations in entries.items():
                    if candidate == word:
                        continue
                    if candidate_pronunciations[0] == partner_phonemes:
                        partner_word = candidate
                        break

                if not partner_word:
                    continue

                # Skip if already seeded
                if Word.objects.filter(minimal_pair=mp, text=word).exists():
                    continue
                if Word.objects.filter(minimal_pair=mp, text=partner_word).exists():
                    continue

                # Create both words
                w1 = Word.objects.create(
                    minimal_pair=mp,
                    text=word,
                    sound=sound_1.lower(),
                )
                w2 = Word.objects.create(
                    minimal_pair=mp,
                    text=partner_word,
                    sound=sound_2.lower(),
                )

                # Link as partners
                w1.partner = w2
                w2.partner = w1
                w1.save()
                w2.save()

                pairs_found += 1
                self.stdout.write(f'  ✓ {word} / {partner_word}')

            self.stdout.write(f'  → {pairs_found} pairs seeded for {sound_1}/{sound_2}')

        self.stdout.write('\nSeeding complete.')