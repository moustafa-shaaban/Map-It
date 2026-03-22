from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import validate_birth_date


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        if self.username:
            self.username = self.username.lower()
        super().save(*args, **kwargs)



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default="avatars/Avatar.jpg", null=True, blank=True)
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        validators=[validate_birth_date]  # Apply the validator here
    )
    bio = models.TextField(max_length=500, blank=True)

    # def clean(self):
    #     """Override for additional model-wide validation if needed."""
    #     super().clean()
    #     # Call your validator explicitly if not using field validators
    #     if self.date_of_birth:
    #         validate_birth_date(self.date_of_birth)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
