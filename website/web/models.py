from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
import datetime


class User(AbstractBaseUser):
    USERNAME_FIELD = "email"

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(unique=True)


class Protein(models.Model):
    entry_id = models.CharField(max_length=512, unique=True)
    uniprot_id = models.CharField(max_length=512)
    
    uniprot_description = models.CharField(max_length=512)
    uniprot_sequence = models.TextField()

class ProteinResult(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)

    alphafold_result = models.FileField()
    quantum_result = models.FileField()