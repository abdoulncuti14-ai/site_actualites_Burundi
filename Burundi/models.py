from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    titre = models.CharField(max_length=90)
    comment = models.TextField()
    date_published = models.DateField(auto_now_add=True)
    auteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mes_articles',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['-date_published']
        verbose_name = "Article"
        verbose_name_plural = "Articles"


class Commentaire(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,      
        related_name='commentaires'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,     
        null=True,
        blank=True,
        related_name='responses'
    )
    auteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mes_commentaires'
    )
    contenu = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.article.titre}"

    class Meta:
        ordering = ['-date_published']
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"