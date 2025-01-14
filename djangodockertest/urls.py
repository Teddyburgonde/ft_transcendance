
from django.urls import path, include
from django.http import HttpResponse
from api.views import UserRetrieveUpdateDestroy 

urlpatterns = [
    path("users/", include("api.urls")),
    path("users/<int:pk>/", UserRetrieveUpdateDestroy.as_view(), 
    name="update"
    ),
]
