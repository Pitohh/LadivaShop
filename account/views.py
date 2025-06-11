from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from account.forms import UserLoginForm
from .serializers import RegisterSerializer, UserSerializer
from .permissions import HasRole

import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Configuration des loggers
logger = logging.getLogger('django')
history_logger = logging.getLogger('history')

class RegisterView(generics.CreateAPIView):
    """Vue pour l'inscription."""
    serializer_class = RegisterSerializer

class UserProfileView(APIView):
    """Vue pour le profil utilisateur."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

def LoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    logger.debug(f"Connexion réussie pour: {email}")
                    history_logger.info(f"Utilisateur connecté: {email}")
                    messages.success(request, "Connexion réussie.")
                    return redirect("dashboard")
                else:
                    logger.warning(f"Tentative de connexion échouée pour: {email}")
                    messages.error(request, "Email ou mot de passe invalide.")
            except Exception as e:
                logger.error(f"Erreur lors de la connexion: {str(e)}")
                messages.error(request, "Une erreur est survenue lors de la connexion. Veuillez réessayer.")
        else:
            logger.warning(f"Formulaire de connexion invalide: {form.errors}")
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserLoginForm()
    return render(request, "account/login.html", {"form": form})


def user_logout(request):
    try:
        user_email = request.user.email
        logout(request)
        logger.debug(f"Déconnexion réussie pour: {user_email}")
        history_logger.info(f"Utilisateur déconnecté: {user_email}")
        messages.success(request, "Vous avez été déconnecté avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la déconnexion: {str(e)}")
        messages.error(request, "Une erreur est survenue lors de la déconnexion. Veuillez réessayer.")
    return redirect('login')
