from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3


# admin.site.register(Question)
# admin.site.register(Choice)

