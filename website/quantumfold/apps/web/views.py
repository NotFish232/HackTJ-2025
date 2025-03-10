from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import random
import datetime
from django.http import HttpResponse
import json

from quantumfold.apps.web.models import User, Protein, ProteinResult

from quantumfold.apps.backend.search import search_proteins
from quantumfold.apps.backend.protein_folding import run_full_protein_folding, run_alphafold
from quantumfold.apps.backend.alphamissense import get_alphamissense_result

import logging


logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')


def visualizer(request):
    return render(request, 'visualizer.html')


def protein_folding(request, uniprot_accession):
    try:
        protein = Protein.objects.get(uniprot_accession=uniprot_accession)
        protein_result = ProteinResult.objects.get(protein=protein)
        if not protein_result.quantum_result or not protein_result.alphafold_result:
            run_full_protein_folding(uniprot_accession)
    except:
        run_full_protein_folding(uniprot_accession)
    alphafold_result = f"/media/{uniprot_accession}/alphafold.pdb"
    quantumfold_result = f"/media/{uniprot_accession}/quantumfold.pdb"
    return redirect(reverse("visualizer") + f"?url1={alphafold_result}&url2={quantumfold_result}")


def visualize_folding(request, uniprot_accession):
    try:
        protein = Protein.objects.get(uniprot_accession=uniprot_accession)
        protein_result = ProteinResult.objects.get(protein=protein)
        if not protein_result.alphafold_result:
            run_alphafold(uniprot_accession)
    except:
        run_alphafold(uniprot_accession)
    alphafold_result = f"/media/{uniprot_accession}/alphafold.pdb"
    return redirect(reverse("visualizer") + f"?url={alphafold_result}")


def personalized_compare(request, uniprot_accession):
    try:
        protein = Protein.objects.get(uniprot_accession=uniprot_accession)
        protein_result = ProteinResult.objects.get(protein=protein)
        if not protein_result.alphafold_result:
            run_alphafold(uniprot_accession)
    except:
        run_alphafold(uniprot_accession)
    return render(request, 'personalized_compare.html', {
        'uniprot_accession': uniprot_accession,
    })


def alphamissense(request, uniprot_id, residue_num):
    result = get_alphamissense_result(uniprot_id, residue_num)
    return HttpResponse(
        json.dumps(result),
        content_type="application/json",
    )



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
