from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tags", views.TagsModelViewSet)


urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', views.SignUpView.as_view(), name='sign-up'),
    path('api/user/articles', views.UserArticleListCreateApiView.as_view(), name='articles'),
    path('api/articles/<int:article_id>/comments', views.CommentListCreatApiView.as_view(), name='comments'),
    path('api/articles/<int:article_id>/reactions', views.ArticleReactionCreateDeleteApiView.as_view(), name='reactions'),
    path('api/user/articles/<int:pk>', views.UserArticleDetailView.as_view(), name='article-detail'),
    path('api/', include(router.urls)),
]

