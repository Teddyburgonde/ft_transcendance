from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, nickname, email, password=None):
        if not email:
            raise ValueError("L'email doit être renseigné")
        email = self.normalize_email(email)
        user = self.model(nickname=nickname, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, email, password=None):
        user = self.create_user(nickname, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    url_avatar = models.CharField(max_length=1000)
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    
    # Champs d'authentification standard
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)  # Champ 'last_login'
    
    # On peut ajouter d'autres champs si nécessaire.
    
    objects = UserManager()  # Utilise notre gestionnaire personnalisé

    USERNAME_FIELD = 'nickname'  # Champ utilisé pour l'authentification
    REQUIRED_FIELDS = ['email']  # Champs supplémentaires à remplir lors de la création

    def __str__(self):
        return self.nickname