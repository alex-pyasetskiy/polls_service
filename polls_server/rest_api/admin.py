from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']})
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['question']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)