from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers.comment import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_destroy(self, instance):

        if instance.children.exists():
            raise ValidationError('Children exists')

        return super(CommentViewSet, self).perform_destroy(instance)

    @detail_route(methods=['get'], url_path='tree')
    def comments_tree(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        children_path = comment.path + '.' + str(comment.pk)
        obj_list = Comment.objects.filter(Q(pk=pk) | Q(path__dore=children_path))
        return Response(data=self.serializer_class(obj_list, many=True).data)