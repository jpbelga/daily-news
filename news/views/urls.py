from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_view, name='news_home'),  # Your view for the news home
]