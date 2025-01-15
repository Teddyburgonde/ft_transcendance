from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class RegisterUserSerializer(ModelSerializer):

	class Meta:
		model = User
		fields = ('username', 'password')

	
	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'],
		)
		user.set_password(validated_data['password'])
		user.save()
		return user