from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import random
import datetime

from quantumfold.apps.web.models import User

import logging

import molviewspec as mvs

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')


def visualizer(request):
    return render(request, 'visualizer.html')


def protein_search(request):
    return render(request, 'protein_search.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        logger.warning(username)


        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(
                request,
                "login.html",
                {
                    "error": "The user does not exist.",
                    "username": username,
                },
            )

        user = authenticate(username=user.username, password=password)
        if user is not None:
            auth_login(request, user)

            if request.GET.get("next"):
                try:
                    url = reverse(request.GET.get("next").replace("/", ""))
                    return redirect(url)
                except:
                    pass

            return redirect(reverse("home"))

        return render(
            request,
            "login.html",
            {
                "error": "The credentials you entered were incorrect. Please try again.",
                "username": username,
            },
        )

    return render(request, "login.html")


@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect(reverse("login"))
