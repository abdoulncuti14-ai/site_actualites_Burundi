from django.db import models

# Create your models here.
class Article(models.Model):
    titre = models.CharField(max_length=90)
    comment = models.TextField()
    date_published = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titre

class commentaire(models.Model):
    #lien vers l'article avec la suppression en cascade
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='commentaires')
    #lien vers un autre commentaire pour les reponses
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='responses')
    auteur = models.CharField(max_length=100)
    contenu = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"commentaire de {self.auteur} sur {self.article.titre}"