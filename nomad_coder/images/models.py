from django.db import models
from nomad_coder.users import models as user_models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from taggit.managers import TaggableManager

#request.user.id -> o request.get('user.id') -> x
# now = timezone.localtime()
# 아직 Admin 모델에 연결을 안해서 Admin에서 볼수 없는 것임.
# Create your models here.
@python_2_unicode_compatible
class TimeStampedModel(models.Model):
    
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

    class Meta: 
        abstract = True

@python_2_unicode_compatible
class Image(TimeStampedModel):

    """ Image Model """
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True, on_delete=models.CASCADE, related_name="images")
    tags = TaggableManager()
    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)

@python_2_unicode_compatible
class Comment(TimeStampedModel):

    """ Comment Model """
    message = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null=True, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.message
    

@python_2_unicode_compatible
class Like(TimeStampedModel):

    """ Like Model """
    creator = models.ForeignKey(user_models.User, null=True, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null=True, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return 'User:{} - Image Caption:{}'.format(self.creator.username, self.image.caption)
    