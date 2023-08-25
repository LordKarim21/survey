from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Survey, Question, UserResponse, Choice
from .serializers import SurveySerializer, QuestionSerializer, UserResponseSerializer, ChoiceSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.filter(active=True)
    serializer_class = SurveySerializer


class UserResponseViewSet(viewsets.ModelViewSet):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer

    @action(detail=False, methods=['get'])
    def completed_surveys(self, request):
        user = request.user
        completed_surveys = user.user_responses.values('survey').distinct()
        serializer = self.get_serializer(completed_surveys, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def survey_details(self, request, pk=None):
        user = request.user
        user_responses = UserResponse.objects.filter(user=user, survey=pk)
        serializer = self.get_serializer(user_responses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_responses(self, request, pk=None):
        user = request.user
        survey = get_object_or_404(Survey, pk=pk)

        if not survey.start_time:
            return Response({'detail': 'The survey has not started yet.'}, status=status.HTTP_400_BAD_REQUEST)

        for question_id, answer_data in request.data.items():
            question = get_object_or_404(Question, pk=question_id)
            text_response = answer_data.get('text_response', None)
            choice_response_ids = answer_data.get('choice_response', [])
            choice_response = Choice.objects.filter(pk__in=choice_response_ids)

            user_response = UserResponse.objects.create(
                user=user,
                survey=survey,
                question=question,
                text_response=text_response
            )
            user_response.choice_response.set(choice_response)

        survey.complete_survey()
        return Response({'detail': 'Responses submitted successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def submit_begin(self, request, pk=None):
        user_response = self.get_object()
        original_survey = user_response.survey

        new_survey = Survey.objects.create(
            title=original_survey.title,
            description=original_survey.description,
            start_time=timezone.now(),
            finish_time=original_survey.finish_time,
            active=True,
            is_passed=False
        )

        for user_response in original_survey.user_responses.filter(user=user_response.user):
            new_user_response = UserResponse.objects.create(
                user=user_response.user,
                survey=new_survey,
                question=user_response.question,
                text_response=user_response.text_response
            )
            new_user_response.choice_response.set(user_response.choice_response.all())

        return Response({'detail': 'Survey has been started.'}, status=status.HTTP_200_OK)
