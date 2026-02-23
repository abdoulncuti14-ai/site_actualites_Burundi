from django.contrib import admin
from .models import Article, Commentaire

admin.site.site_header = "Administration Burundi News"
admin.site.site_title = "Burundi News Portal"
admin.site.index_title = "site d'actualites"



class CommentaireInline(admin.TabularInline):
    model = Commentaire
    extra = 1
    fields = ('auteur', 'contenu', 'parent')
    list_display = ('id', 'auteur', 'contenu', 'parent')
    search_fields = ('auteur', 'contenu')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'date_published')
    search_fields = ('titre',)
    ordering = ('-date_published',)
    inlines = [CommentaireInline]



class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'article', 'date_published', 'parent')
    list_filter = ('date_published', 'article')
    search_fields = ('auteur',)
    list_per_page = 25
    autocomplete_fields = ['article']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Commentaire, CommentaireAdmin)




