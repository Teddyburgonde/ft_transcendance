from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView


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

class UserList(APIView):
	def get(self, request, format=None):
		
		nickname = request.query_params.get("nickname", "").strip()

		if nickname:
			users = User.objects.filter(nickname__icontains=nickname)
		else:
			users = User.objects.all()
	
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)