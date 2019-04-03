from django.urls import path
from . import views
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,



                    )

from .forms import UserAddDateProgramme, UserUpdateExercise


urlpatterns = [
    path('', PostListView.as_view(), name='users-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='users-about'),
    path('logprogramme/', views.log_programme, name='log-programme'),
    path('logprogramme/add-more/', views.log_programme, name='add-more'),
    path('addexercise/', views.add_exercise, name='add-exercise'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('make-predictions/', views.generate_prediction, name='make-prediction'),

]