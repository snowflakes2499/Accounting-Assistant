from django.urls import path
from .views import *

urlpatterns = [
    path('record/', recording_control),
    path('recoversnap/', recoversnap),
    # path('record/', recording_control),
]

