

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Article, Commentaire
from .serializers import (
    ArticleSerializer, CommentaireSerializer,
    UserSerializer, MyTokenObtainPairSerializer
)

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly,
    IsAdminUser, IsAuthenticated
)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView



class IsAuthorOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, 'auteur'):
            return obj.auteur == request.user or request.user.is_staff
        return request.user.is_staff




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        """Un admin voit tous les users. Un user normal ne voit que lui-même."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-date_published')
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'titre': ['icontains'],
        'date_published': ['gte', 'lte'],
    }

    def get_permissions(self):
        
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsAuthorOrAdmin()]

    def perform_create(self, serializer):
        
        serializer.save(auteur=self.request.user)



class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all().order_by('-date_published')
    serializer_class = CommentaireSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['auteur', 'article']

    def get_permissions(self):
        
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsAuthorOrAdmin()]

    def perform_create(self, serializer):
        
        serializer.save(auteur=self.request.user)



@api_view(['POST'])
@permission_classes([AllowAny])
def api_inscription(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')
    email = request.data.get('email', '').strip()

    
    if not username or not password:
        return Response({"error": "Nom d'utilisateur et mot de passe obligatoires."}, status=400)

    if len(password) < 6:
        return Response({"error": "Le mot de passe doit contenir au moins 6 caractères."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Ce nom d'utilisateur est déjà pris."}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({
        "message": "Compte créé avec succès !",
        "user_id": user.id,
        "username": user.username
    }, status=201)



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