from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from nomad_coder.images import models as image_models
from nomad_coder.users import models as user_models
#readOnly--> serializer에서 쓰이는데 정확히 무슨의미일까?


class Notification(image_models.TimeStampedModel):
    #like->DB, Like->admin
    TYPE_CHOICES = (
        ('like','Like'),
        ('comment','Comment'),
        ('follow','Follow'),
    )
    creator = models.ForeignKey(user_models.User, related_name='creator', on_delete=models.CASCADE)
    to = models.ForeignKey(user_models.User, related_name='to', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(image_models.Image, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    #blank-->isRequired? --> admin에서 생성시 안채워도 된다.
    class Meta:
        ordering=["-created_at"]

    def __str__(self):
        return "From: {} - To: {}".format(self.creator, self.to)