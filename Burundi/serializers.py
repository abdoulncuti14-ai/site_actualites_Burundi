from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Commentaire
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff
        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'is_superuser']
        



class CommentaireSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.ReadOnlyField(source='auteur.username')
    responses = serializers.SerializerMethodField()

    class Meta:
        model = Commentaire
        fields = [
            'id', 'article', 'parent',
            'auteur',       
            'auteur_nom',   
            'contenu',
            'date_published',
            'responses'    
        ]
        read_only_fields = [
            'auteur',           
            'date_published',
            'auteur_nom',
            'responses'
        ]

    def get_responses(self, obj):
        """Retourne les réponses directes à ce commentaire (1 niveau)"""
        if obj.responses.exists():
            return CommentaireSerializer(obj.responses.all(), many=True).data
        return []



class ArticleSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.SerializerMethodField()
    nb_commentaires = serializers.IntegerField(source='commentaires.count', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'titre', 'comment',
            'date_published', 'nb_commentaires',
            'auteur_nom'
        ]
        read_only_fields = ['date_published', 'nb_commentaires', 'auteur_nom']

    def get_auteur_nom(self, obj):
        if obj.auteur:
            return obj.auteur.username
        return "Burundi News"