from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserListCreate(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def delete(self, request, *args, **kwargs):
		User.objects.all().delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	lookup_field = "pk"