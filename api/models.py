from django.db import models

# Create your models here.
class Users(models.Model):
	id = models.AutoField(primary_key=True)
	nickname = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)
	url_avatar = models.CharField(max_length=100)
	win = models.IntegerField()
	lose = models.IntegerField()
	def __str__(self):
		return self.name
