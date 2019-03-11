from rest_framework import serializers
from . import models
from nomad_coder.users import serializers as user_serializers
from nomad_coder.images import serializers as image_serializers

class NotificationSerializer(serializers.ModelSerializer):

    creator = user_serializers.UserProfileSerializer()
    image = image_serializers.SmallImageSerializer() # tuple 이나 list 를 나타내기 위해서 , 를 마지막에 붙이는구나.

    class Meta:
        model = models.Notification
        fields = "__all__"


