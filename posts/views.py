from rest_framework import viewsets, permissions, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import PostModel, PostLikeModel, CommentModel, CommentLikeModel
from posts.paginations import PostsPagination
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = PostModel.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    pagination_class = PostsPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return PostModel.objects.filter(parent__isnull=True)


class PostChildListApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostsPagination

    def get_queryset(self):
        parent = self.request.query_params.get('parent')
        if parent is None:
            return Response({
                'success': False,
                'message': 'Parent field is required'
            })


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = CommentModel.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostCommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostsPagination

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if not post_id:
            raise ValidationError({'detail': 'Post ID is required.'})
        return CommentModel.objects.filter(post_id=post_id)


class CommentReplyListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        parent_id = self.request.query_params.get('parent')
        if not parent_id:
            return CommentModel.objects.none()
        return CommentModel.objects.filter(parent_id=parent_id)

    def list(self, request, *args, **kwargs):
        parent_id = self.request.query_params.get('parent')
        if not parent_id:
            return Response({
                "success": False,
                "message": "The 'parent' query parameter is required."
            }, status=400)
        return super().list(request, *args, **kwargs)


class CommentLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(CommentModel, id=comment_id)
        CommentLikeModel.objects.get_or_create(user=request.user, comment=comment)
        response = {
            'message': 'Comment liked successfully'
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, comment_id):
        comment = get_object_or_404(CommentModel, id=comment_id)
        like = CommentLikeModel.objects.filter(user=request.user, comment=comment).first()
        if like:
            like.delete()
            response = {
                'success': True,
                'message': 'Like removed successfully.'
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Like does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


class PostLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(PostModel, id=post_id)
        PostLikeModel.objects.get_or_create(user=request.user, post=post)
        response = {
            'success': True,
            'message': 'Post liked successfully'
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        post = get_object_or_404(PostModel, id=post_id)
        like = PostLikeModel.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            response = {
                'success': True,
                'message': 'Like removed successfully.'
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        response = {
            'success': True,
            'message': 'Like does not exist.'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
