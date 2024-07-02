import os

from dotenv import load_dotenv
from rest_framework import status, views
from rest_framework.response import Response

from . import client

load_dotenv()


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
        app_id = os.getenv("ALGOLIA_APPLICATION_ID")
        search_api_key = os.getenv("ALGOLIA_SEARCH_ONLY_API_KEY")
        return Response({"app_id": app_id, "api_key": search_api_key}, status=status.HTTP_200_OK)
