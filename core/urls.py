from django.urls import path

from core.views import UsersView


urlpatterns = [
    path('', UsersView.as_view(), name='users'),
]
