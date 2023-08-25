from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'surveys', views.SurveyViewSet, basename='survey')
router.register(r'user', views.UserResponseViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]

