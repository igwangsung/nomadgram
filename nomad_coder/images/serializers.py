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
            'profile_image',
            'username',
            'name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
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
    is_liked = serializers.SerializerMethodField()

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
        "natural_time",
        "is_liked",
        "is_vertical",
        )
    def get_is_liked(self, obj):
        if 'request' in self.context:
            request = self.context['request']
        try: 
            models.Like.objects.get(creator__id=request.user.id, image__id=obj.id)
            return True
        except models.Like.DoesNotExist:
            return False
        return False


class InputImageSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = models.Image
        fields = (
            'file',
            'location',
            'caption',
            'tags',

        )