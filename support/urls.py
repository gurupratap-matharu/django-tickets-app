from django.urls import path

from . import views

app_name = 'support'
urlpatterns = [
    # ex: /
    path('', views.IndexView.as_view(), name='index'),
    # ex: /support/list
    path('list/', views.ListView.as_view(), name='list'),
    # ex: /support/2/detail
    path('<int:pk>/detail/', views.DetailView.as_view(), name='detail'),
    # ex: /support/register
    path('register/', views.RegisterView.as_view(), name='register'),

    ]
