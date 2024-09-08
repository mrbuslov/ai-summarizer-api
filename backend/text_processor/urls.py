from django.urls import path
from .views import SummarizePDF

urlpatterns = [
    path('summarize/', SummarizePDF.as_view(), name='summarize-pdf'),
]
