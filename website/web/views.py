from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import random
import datetime

from web.models import User

def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(
                request,
                "login.html",
                {
                    "error": "The credentials you entered were incorrect. Please try again.",
                    "email": email,
                },
            )

        user = authenticate(username=user.email, password=password)
        if user is not None:
            auth_login(request, user)

            if request.GET.get("next"):
                try:
                    url = reverse(request.GET.get("next").replace("/", ""))
                    return redirect(url)
                except:
                    pass

            return redirect(reverse("index"))

        return render(
            request,
            "login.html",
            {
                "error": "The credentials you entered were incorrect. Please try again.",
                "email": email,
            },
        )

    return render(request, "login.html")


@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect(reverse("login"))
