from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Snippet, Tag


class SnippetOverViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        snippets_query = Snippet.objects.filter(existence_status=1, created_by=request.user)

        snippets = [
            {
                "id": snippet.id,
                "title": snippet.title,
                "detail_url": reverse("snippet-detail", args=[snippet.id], request=request),
            }
            for snippet in snippets_query
        ]

        return Response({"total_count": snippets_query.count(), "snippets": snippets})


class SnippetViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            filter_args = {"id": kwargs["pk"]}
        else:
            filter_args = {}
        snippets = Snippet.objects.filter(created_by=request.user, existence_status=1, **filter_args)
        snippet_data = [
            {
                "id": snippet.id,
                "title": snippet.title,
                "note": snippet.note,
                "created_at": snippet.created_at,
                "updated_at": snippet.updated_at,
                "created_by": snippet.created_by.first_name,
                "tag_id": snippet.tag.id,
                "tag_title": snippet.tag.title,
            }
            for snippet in snippets
        ]
        return Response(snippet_data)

    def post(self, request, *args, **kwargs):
        title = request.data.get("title")
        note = request.data.get("note")
        tag_title = request.data.get("tag_title")
        if not title or not note or not tag_title:
            return Response({"detail": "Title, note, and tags are required."}, status=400)

        tag, created = Tag.objects.get_or_create(title=tag_title)

        snippet = Snippet.objects.create(title=title, note=note, created_by=request.user, tag=tag)

        snippet_data = {
            "id": snippet.id,
            "title": snippet.title,
            "note": snippet.note,
            "tag_id": tag.id,
            "tag_title": tag.title,
        }

        return Response(snippet_data, status=201)

    def put(self, request, *args, **kwargs):
        try:
            snippet = Snippet.objects.get(id=kwargs["pk"], created_by=request.user, existence_status=1)
        except Snippet.DoesNotExist:
            return Response({"detail": "Snippet not found."}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get("title")
        note = request.data.get("note")
        tag_title = request.data.get("tag_title")

        if not title or not note or not tag_title:
            return Response({"detail": "Title and note are required."}, status=status.HTTP_400_BAD_REQUEST)
        tag, created = Tag.objects.get_or_create(title=tag_title)

        snippet.title = title
        snippet.note = note
        snippet.tag = tag
        snippet.save()

        snippet_data = {
            "id": snippet.id,
            "title": snippet.title,
            "note": snippet.note,
            "created_at": snippet.created_at,
            "updated_at": snippet.updated_at,
            "tag_id": tag.id,
            "tag_title": tag.title,
        }

        return Response(snippet_data)

    def delete(self, request, *args, **kwargs):
        try:
            snippet = Snippet.objects.get(id=kwargs["pk"], created_by=request.user, existence_status=1)
        except Snippet.DoesNotExist:
            return Response({"detail": "Snippet not found."}, status=status.HTTP_404_NOT_FOUND)

        snippet.existence_status = 0
        snippet.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            try:
                tag = Tag.objects.get(pk=kwargs['pk'])
            except Tag.DoesNotExist:
                return Response({"detail": "Tag not found."}, status=status.HTTP_404_NOT_FOUND)

            snippets = tag.snippets.all()
            snippet_data = [
                {
                    "id": snippet.id,
                    "title": snippet.title,
                    "note": snippet.note,
                    "created_at": snippet.created_at,
                    "updated_at": snippet.updated_at,
                    "created_by": snippet.created_by.first_name,
                    "tag_id": snippet.tag.id,
                    "tag_title": snippet.tag.title,
                }
                for snippet in snippets
            ]
            return Response(snippet_data)

        tags_query = Tag.objects.filter()
        tags = [
            {
                "id": tag.id,
                "title": tag.title,
                "created_at": tag.created_at,
            }
            for tag in tags_query
        ]

        return Response({"tags": tags})
