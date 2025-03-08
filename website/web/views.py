from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import random
import datetime

from web import models

def home(request):
    return render(request, 'home.html')