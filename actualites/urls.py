"""
URL configuration for actualites project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from Burundi import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'commentaires', views.CommentaireViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('inscription/', views.inscription, name='inscription'),
    path('check-role/', views.redirection_post_connexion, name='check_role'),
    path('flux/', views.flux_actualites, name='flux_actualites'),
    path('dashboard/', views.dashboard_superuser, name='dashboard_superuser'),
    path('supprimer/<int:article_id>/', views.supprimer_article, name='supprimer_article'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/', include(router.urls)),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.api_inscription, name='api_register'),
    path('api-auth/', include('rest_framework.urls')),

]