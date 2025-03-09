from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
import datetime


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    USERNAME_FIELD = "username"
    username = models.CharField(max_length=512, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


class Protein(models.Model):
    uniprot_accession = models.CharField(max_length=512, unique=True)
    entry_id = models.CharField(max_length=512)
    uniprot_id = models.CharField(max_length=512)

    uniprot_description = models.CharField(max_length=512)
    uniprot_sequence = models.TextField()

    def __str__(self):
        return self.uniprot_accession

class ProteinResult(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE, null=True, blank=True)

    alphafold_result = models.FileField()
    quantum_result = models.FileField()

    def __str__(self):
        return self.protein.uniprot_accession
    