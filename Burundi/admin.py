
from django.contrib import admin
from .models import Article, Commentaire

admin.site.site_header  = "Administration Burundi News"
admin.site.site_title   = "Burundi News Portal"
admin.site.index_title  = "Site d'actualités"


class CommentaireInline(admin.TabularInline):
    model        = Commentaire
    extra        = 1
    fields       = ('auteur', 'contenu', 'parent')
    raw_id_fields = ['auteur']


class ArticleAdmin(admin.ModelAdmin):
    list_display   = ('id', 'titre', 'auteur', 'date_published')
    search_fields  = ('titre', 'auteur__username')
    ordering       = ('-date_published',)
    list_filter    = ('date_published',)
    inlines        = [CommentaireInline]


class CommentaireAdmin(admin.ModelAdmin):
    list_display   = ('auteur', 'article', 'date_published', 'parent')
    list_filter    = ('date_published', 'article')
    search_fields  = ('auteur__username', 'contenu')
    list_per_page  = 25
    raw_id_fields  = ['article', 'auteur']


admin.site.register(Article,     ArticleAdmin)
admin.site.register(Commentaire, CommentaireAdmin)