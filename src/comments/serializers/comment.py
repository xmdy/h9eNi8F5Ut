from rest_framework import serializers
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError

from comments import constants
from comments.models import Comment


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)

    created_at = serializers.DateTimeField(allow_null=True)
    updated_at = serializers.DateTimeField(allow_null=True)

    user_id = serializers.CharField(max_length=36)
    parent_id = serializers.CharField(max_length=36)

    object_type = serializers.CharField(max_length=64)
    object_id = serializers.CharField(max_length=36)

    comment = serializers.CharField()

    def create(self, validated_data):
        object_type = validated_data['object_type'].lower()
        object_id = validated_data['object_id']

        path = '%s_%s' % (object_type, object_id)
        parent_id = None

        if object_type == constants.OBJECT_TYPE_COMMENT:
            comment = Comment.objects.filter(id=object_id).first()
            if not comment:
                raise ValidationError('bad comment id')
            parent_id = object_id
            path = comment.path + '.' + object_id

        validated_data['path'] = path
        validated_data['parent_id'] = parent_id

        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment = validated_data['comment']
        instance.save(update_fields=['comment', 'updated_at'])
        return instance

