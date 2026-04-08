from django.contrib import admin
from .models import Language, MinimalPair, Word


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(MinimalPair)
class MinimalPairAdmin(admin.ModelAdmin):
    list_display = ('language', 'sound_1', 'sound_2')
    list_filter = ('language',)
    search_fields = ('sound_1', 'sound_2')


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display  = ('text', 'sound', 'partner', 'minimal_pair', 'audio_file')
    list_filter   = ('minimal_pair', 'sound')
    search_fields = ('text',)
    list_editable = ('partner',)