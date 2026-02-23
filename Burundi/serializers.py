from rest_framework import serializers
from .models import Article, Commentaire
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'is_superuser']
from rest_framework import serializers
from .models import Article, Commentaire
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'is_superuser']
class CommentaireSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.ReadOnlyField(source='auteur.username')
    class Meta:
        model = Commentaire
        fields = ['id', 'article', 'parent', 'auteur', 'auteur_nom', 'contenu', 'date_published']
        read_only_fields = ['date_published']

class ArticleSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.SerializerMethodField()
    nb_commentaires = serializers.IntegerField(source='commentaires.count', read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'titre', 'comment', 'date_published', 'nb_commentaires', 'auteur_nom']

    def get_auteur_nom(self, obj):

        if obj.auteur:
            return obj.auteur.username
        return "Burundi News"

class ArticleSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.SerializerMethodField()
    nb_commentaires = serializers.IntegerField(source='commentaires.count', read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'titre', 'comment', 'date_published', 'nb_commentaires', 'auteur_nom']

    def get_auteur_nom(self, obj):

        if obj.auteur:
            return obj.auteur.username
        return "Burundi News"