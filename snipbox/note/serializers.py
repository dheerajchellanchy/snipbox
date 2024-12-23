from rest_framework import serializers
from .models import Snippet, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title"]


class SnippetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Snippet
        fields = ["id", "title", "note", "created_at", "updated_at", "user", "tags"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        snippet = Snippet.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(title=tag_data["title"])
            snippet.tags.add(tag)

        return snippet

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)
        instance.title = validated_data.get("title", instance.title)
        instance.note = validated_data.get("note", instance.note)
        instance.save()

        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(title=tag_data["title"])
                instance.tags.add(tag)

        return instance
