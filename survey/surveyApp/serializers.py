from rest_framework.serializers import ModelSerializer
from .models import Survey, Question, UserResponse, Choice


class ChoiceSerializer(ModelSerializer):
    """
    Сериализатор для вариантов ответов.

    """
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    """
    Сериализатор для вопросов.

    """
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class UserResponseSerializer(ModelSerializer):
    """
    Сериализатор для ответов пользователей.

    """
    class Meta:
        model = UserResponse
        fields = '__all__'


class SurveySerializer(ModelSerializer):
    """
    Сериализатор для опросов.

    """
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'
