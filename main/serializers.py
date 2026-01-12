
from rest_framework import serializers
from .models import Article, Comment, Tag, ArticleReaction, Follow
from django.contrib.auth import get_user_model


User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'created_at']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    author = SignUpSerializer(read_only=True)
    tag_names = serializers.ListField(child=serializers.CharField(), write_only=True)
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'tags', 'tag_names', 'likes_count', 'dislikes_count']

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def create(self, validated_data):
        print(validated_data)
        tag_names = validated_data.pop("tag_names")
        article = Article.objects.create(**validated_data)
        
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            article.tags.add(tag)
        
        return article 


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user']


class ArticleReactionSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = ArticleReaction
        fields = ['id', 'reaction', 'user']
