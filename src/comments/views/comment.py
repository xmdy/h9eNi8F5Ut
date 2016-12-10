import datetime
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

    def filter_queryset(self, queryset):
        object_type = self.request.GET.get('object_type')
        object_id = self.request.GET.get('object_id')

        user_id = self.request.GET.get('user_id')

        created__gte = self.request.GET.get('created__gte')
        created__lte = self.request.GET.get('created__lte')

        if object_type and object_id:
            queryset = queryset\
                .filter(object_type=object_type, object_id=object_id, parent__isnull=True)
        elif user_id:
            queryset = queryset \
                .filter(user_id=user_id)

        if created__gte:
            try:
                datetime.datetime.strptime(created__gte, '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Created__gte incorrect data format, should be YYYY-MM-DD")

            queryset = queryset.filter(created__gte=created__gte)

        if created__lte:
            try:
                datetime.datetime.strptime(created__lte, '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Created__lte incorrect data format, should be YYYY-MM-DD")

            queryset = queryset.filter(created__lte=created__lte)

        return queryset

    @detail_route(methods=['get'], url_path='tree')
    def comments_tree(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        children_path = comment.path + '.' + str(comment.pk)
        obj_list = Comment.objects.filter(Q(pk=pk) | Q(path__dore=children_path))
        return Response(data=self.serializer_class(obj_list, many=True).data)

    @detail_route(methods=['get'], url_path='tree')
    def comments_tree(self, request, pk=None):
        include_self = 'include_self' in self.request.GET

        comment = Comment.objects.get(pk=pk)

        children_path = comment.path + '.' + str(comment.pk)

        condition = Q(path__dore=children_path)
        if include_self:
            condition |= Q(pk=pk)

        obj_list = Comment.objects.filter(condition)

        return Response(data=self.serializer_class(obj_list, many=True).data)
