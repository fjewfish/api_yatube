from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Group, Post

from .permissions import IsOwnerOrIsAuthenticated
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrIsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrIsAuthenticated,)

    def _get_post(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        return post

    def get_queryset(self):
        return self._get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self._get_post())
