from django.contrib import admin

from .models import Answer, Question, Quiz

# Register your models here.
class InlineAnswer(admin.StackedInline):
    model = Answer
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [InlineAnswer,
    ]


admin.site.register((Answer, Quiz))