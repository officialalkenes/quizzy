from django.contrib import admin

from .models import Answer, Question, Quiz

# Register your models here.
class InlineAnswer(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inline = InlineAnswer


admin.site.register((Answer, Quiz))