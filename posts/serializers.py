from rest_framework import serializers, generics, permissions
from rest_framework.response import Response

from posts.models import PostModel, CommentModel, PostLikeModel, CommentLikeModel, HistoryModel
from posts.paginations import PostsPagination


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        child_count = serializers.SerializerMethodField()
        model = PostModel
        fields = ['id', 'text', 'image', 'created_at', 'parent', 'child_count']
        extra_kwargs = {
            'image': {'required': False},
            'user': {'required': False},
            'parent': {'required': False},
        }

    def get_child_count(self, obj):
        return obj.children.count()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    class Meta:
        model = CommentModel
        fields = ['id', 'user', 'text', 'image', 'parent', 'created_at', 'replies']
        extra_kwargs = {
            'image': {'required': False},
        }

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PostLikeModel
        fields = ['id', 'user', 'post', 'created_at']


class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    comment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommentLikeModel
        fields = ['id', 'user', 'comment', 'created_at']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryModel
        fields = ['id', 'user', 'content', 'timestamp', 'expiration_time', 'visibility']