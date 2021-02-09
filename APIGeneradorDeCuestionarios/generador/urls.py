from django.urls import path
from .views import Cuestionario
urlpatterns = [
    path('generador/', Cuestionario.as_view()),
]
