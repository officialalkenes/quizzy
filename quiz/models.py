import random
from django.db import models

# Create your models here.
class Quiz(models.Model):
    DIFFICULTY = (
        ('EASY', 'EASY'),
        ('MEDIUM', 'MEDIUM'),
        ('HARD', 'HARD')
    )
    quiz = models.CharField(max_length=100, verbose_name='Quiz')
    no_of_question = models.IntegerField(blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY)
    created = models.DateTimeField(auto_now_add=True)
    time_taken = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.quiz}- {self.difficulty}'

    def get_question_and_number(self, *args, **kwargs):
        questions = self.question.set.all()[:self.no_of_question]
        randorm_question = random(questions)

    class Meta:
        verbose_name_plural = 'Quizzes'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=400)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return f'{self.quiz.quiz}- {self.question}'


class Answer(models.Model):
    real_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=400)
    correct = models.BooleanField(default=False)

