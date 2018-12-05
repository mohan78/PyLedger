from django.urls import path
from django.contrib.auth import views as authviews
from . import views

urlpatterns = [
    path('login/', authviews.login, name="login"),
    path('logout/', authviews.logout, name="logout"),
    path('signup/', views.register, name="signup")
]
