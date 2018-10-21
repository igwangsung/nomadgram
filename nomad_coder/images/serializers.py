from rest_framework import serializers
from . import models
from nomad_coder.users import models as user_models
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
class SmallImageSerializer(serializers.ModelSerializer):

    '''Used For the notification'''

    class Meta:
        model = models.Image
        fields = (
            'file',
        )


class CountImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count',
        )

class FeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image',
        )

class CommentSerializer(serializers.ModelSerializer):

    #다른 유저가 사용하면 안되니까 읽기 전용
    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator',
        )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(TaggitSerializer, serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    tags = TagListSerializerField()

    #What about hashtags?
    class Meta:
        model = models.Image
        fields = (
        "id",
        "file",
        "location",
        "caption",
        "comments",
        "like_count",
        "creator",
        "tags",
        "created_at",
        )

class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'file',
            'location',
            'caption',

        )