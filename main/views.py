
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import SignUpSerializer, TagSerializer, ArticleSerializer, CommentSerializer, ArticleReactionSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet
from .models import Tag, Article, Comment, ArticleReaction
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import NotFound


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

@extend_schema(
        request=SignUpSerializer,
        responses={201: SignUpSerializer},
    )
class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer


class TagsModelViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


@extend_schema(
    tags=['User articles']
)
class UserArticleListCreateApiView(ListCreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)
    
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

@extend_schema(
    tags=['User articles']
)
class UserArticleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)
    

class CommentListCreatApiView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.kwargs['article_id']
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise NotFound(detail=f"Article with {article_id} not found")
        serializer.save(user=self.request.user, article=article)

    def get_queryset(self):
        article_id = self.kwargs['article_id']
        return Comment.objects.filter(article__id=article_id)

class ArticleReactionCreateDeleteApiView(ListCreateAPIView):
    serializer_class = ArticleReactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        reaction_type = serializer.validated_data["reaction"]
        article_id = self.kwargs['article_id']
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise NotFound(detail=f"Article with {article_id} not found")
        
        reaction, created = ArticleReaction.objects.get_or_create(user=self.request.user, article=article, reaction=reaction_type)
        if not created:
            reaction.delete()
            if reaction_type == 'dislike':
                article.dislikes_count -= 1
                article.save()
            else:
                article.likes_count -= 1
                article.save()
            return Response(data={
                "detail": "deleted"
            })
        if reaction_type == 'dislike':
            article.dislikes_count += 1
            article.save()
        else:
            article.likes_count += 1
            article.save()
        return Response(data={
            "detail": "created"
        })

    def get_queryset(self):
        article_id = self.kwargs['article_id']
        return ArticleReaction.objects.filter(article__id=article_id)