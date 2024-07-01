from decouple import config
from rest_framework import status, views
from rest_framework.response import Response

from . import client


class SearchAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        tags = request.GET.get("tags")
        if not query:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        res = client.perform_search_v2(query, author=user, tags=tags)
        return Response(res, status=status.HTTP_200_OK)


class SearchAPICredetials(views.APIView):
    def get(self, request, *args, **kwargs):
        app_id = config("APPLICATION_ID")
        search_api_key = config("SEARCH_ONLY_API_KEY")
        return Response(
            {"app_id": app_id, "api_key": search_api_key}, status=status.HTTP_200_OK
        )


# class SearchAPIIndices(views.APIView):
#     def get(self, request, *args, **kwargs):
#         return Response({"indices": client.get_list_indices()}, status=status.HTTP_200_OK)
