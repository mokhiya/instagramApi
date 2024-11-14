from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated

from posts.models import PostModel
from posts.paginations import PostsPagination
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer


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
