from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Choice(models.Model):
    """
    Модель для представления вариантов ответов.

    Поля:
    - question : Связь с вопросом, к которому относится вариант.
    - text : Текст варианта ответа.
    """
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Question(models.Model):
    """
    Модель для представления вопросов.

    Поля:
    - TYPE_QUESTION : Словарь для выбора типа вопроса.
    - survey : Связь с опросом, к которому относится вопрос.
    - text : Текст вопроса.
    - type : Тип вопроса.
    """
    TYPE_QUESTION = {
        "t": "text",
        "s": "single-choice",
        "m": "multiple-choice"
    }
    choices = models.ForeignKey(Choice, related_name='choices', on_delete=models.CASCADE)
    text = models.TextField()
    type = models.CharField(max_length=1, choices=TYPE_QUESTION, default="t")

    def __str__(self):
        return self.text


class Survey(models.Model):
    """
    Модель для представления опросов.

    Поля:
    - title : Название опроса.
    - description : Описание опроса.
    - start_time : Дата и время начала опроса.
    - finish_time : Дата и время окончания опроса.
    - active : Показывает, активен ли опрос в данный момент.

    """
    title = models.CharField(max_length=124)
    description = models.TextField(null=True, blank=True)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def complete_survey(self):
        """
        Завершает опрос, устанавливая дату и время завершения.
        """
        self.finish_time = timezone.now()
        self.save()

    def start_survey(self):
        """
        Начинает опрос, устанавливая дату и время начала.
        """
        self.start_time = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class UserResponse(models.Model):
    """
    Модель для хранения ответов пользователей.

    Поля:
    - user : Связь с пользователем, который дал ответ.
    - survey : Связь с опросом, к которому относится ответ.
    - question : Связь с вопросом, на который дан ответ.
    - text_response : Текстовый ответ пользователя.
    - choice_response : Связь с выбранными вариантами ответов пользователя.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    surveys = models.ManyToManyField(Survey)
