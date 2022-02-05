from django.urls import path
from snippets import views

app_name = 'snippets'

urlpatterns = [
    path('', views.snippet_list, name='list'),
    path('<int:pk>/', views.snippet_detail, name='detail'),
]