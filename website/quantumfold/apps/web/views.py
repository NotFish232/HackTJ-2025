from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import random
import datetime

from quantumfold.apps.web.models import User

from quantumfold.apps.backend.search import search_proteins
from website.quantumfold.apps.backend.alphafold_folding import run_full_protein_folding

import logging


logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')


def visualizer(request):
    return render(request, 'visualizer.html')


def protein_folding(request, uniprot_accession):
    run_full_protein_folding(uniprot_accession)
    alphafold_result = f"/media/{uniprot_accession}/alphafold.pdb"
    return redirect(reverse("visualizer") + f"?url={alphafold_result}")


def personalized_compare(request):
    return render(request, 'personalized_compare.html')


def protein_search(request):
    if request.GET.get("search"):
        search_term = request.GET.get("search")
        proteins = search_proteins(search_term)

        return render(
            request,
            "protein_search.html",
            {"proteins": [
                {'name': protein[0], 'uniprot_accession': protein[1]}
                for protein in proteins
            ]},
        )
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
