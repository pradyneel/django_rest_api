from django.urls import path
from .views import SignUp, Login, UserView, LogoutView, DeleteView, UpdateView
from . import views

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('login', Login.as_view()),
    path('user', UserView.as_view(), name='userinfo'),
    path('logout', LogoutView.as_view()),
    path('delete/<str:pk>/', DeleteView.as_view(), name='delete'),
    path('update/<str:pk>', UpdateView.as_view(), name = "update")
]
