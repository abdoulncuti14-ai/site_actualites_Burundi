from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Article, Commentaire, MyTokenObtainPairSerializer
from .serializers import ArticleSerializer, CommentaireSerializer, UserSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-date_published')
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'titre': ['icontains'],
        'date_published': ['gte', 'lte'],
    }
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all().order_by('-date_published')
    serializer_class = CommentaireSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['auteur', 'article']
    permission_classes = [IsAuthenticatedOrReadOnly]

@api_view(['POST'])
@permission_classes([AllowAny])
def api_inscription(request):

    username = request.data.get('username')
    password = request.data.get('password')
    if username and password:
        if User.objects.filter(username=username).exists():
            return Response({"error": "Utilisateur déjà existant"}, status=400)
        User.objects.create_user(username=username, password=password)
        return Response({"message": "Compte créé !"}, status=201)
    return Response({"error": "Données manquantes"}, status=400)



def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Succès ! Connectez-vous.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'inscription.html', {'form': form})

@login_required
def redirection_post_connexion(request):
    if request.user.is_superuser:
        return redirect('dashboard_superuser')
    return redirect('flux_actualites')

@login_required
def flux_actualites(request):
    articles = Article.objects.all().order_by('-date_published')
    return render(request, 'flux.html', {'articles': articles})

@login_required
def dashboard_superuser(request):
    if not request.user.is_superuser:
        return redirect('flux_actualites')
    articles = Article.objects.all().order_by('-date_published')
    return render(request, 'dashboard.html', {'articles': articles})

@login_required
def supprimer_article(request, article_id):
    if request.user.is_superuser:
        article = get_object_or_404(Article, id=article_id)
        article.delete()
    return redirect('dashboard_superuser')