from django.urls import path
from .views import APIRoot, BMICalculate, DiabetesRisk, HealthAdvice, DiabetesNNPredict
from .views import GeminiChat

urlpatterns = [
    path('', APIRoot.as_view()),
    path('bmi/', BMICalculate.as_view()),
    path('risk/', DiabetesRisk.as_view()),
    path('advice/', HealthAdvice.as_view()),
    path('nn_predict/', DiabetesNNPredict.as_view()),
    path('api/gemini_chat/', GeminiChat.as_view(), name='gemini_chat'),
]