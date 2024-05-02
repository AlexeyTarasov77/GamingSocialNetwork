from rest_framework import views, status
from rest_framework.response import Response
from . import client

class BaseSearchAPIView(views.APIView):
    index_name = None
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        tags = request.GET.get("tags")
        if not query:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        res = client.perform_search(self.index_name, query, author=user, tags=tags)
        return Response(res, status=status.HTTP_200_OK)
        