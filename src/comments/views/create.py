from rest_framework.generics import CreateAPIView

from comments.models import Comment


class CreateCommentView(CreateAPIView):
    model = Comment

    def post(self, request, *args, **kwargs):
        pass