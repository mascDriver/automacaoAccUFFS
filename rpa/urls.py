from django.urls import path, include
from rpa.views import AccFormView


urlpatterns = [
    path('', AccFormView.as_view(), name='acc'),
]