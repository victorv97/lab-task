from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('task-list/', views.get_task_list, name='task-list'),
    path('user-task-list/<str:user_id>/', views.get_user_task_list, name='user-task-list'),
    path('task/<str:task_id>/', views.get_task, name='task'),
    path('create-task/', views.create_task, name='create-task'),
    path('update-task/<str:task_id>/', views.update_task, name='update-task'),
    path('delete-task/<str:task_id>/', views.delete_task, name='delete-task'),
    path('signup/', views.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
