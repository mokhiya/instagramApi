from rest_framework import serializers, generics, permissions
from rest_framework.response import Response

from posts.models import PostModel
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
