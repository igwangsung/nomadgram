from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """ User Model """

    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female'),
        ('not-specified','Not specified')
    )
    # First Name and Last Name do not cover name patterns
    # around the globe.
    profile_image = models.ImageField(null=True) #null과 blank 의 차이점.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    website = models.URLField(_("website of User"), null=True)
    bio = models.TextField(_("bio of User"), null=True)
    phone = models.CharField(_("phone of User"),  max_length=140, null=True)
    gender = models.CharField(_("gender of User"),  max_length=80, null=True, choices=GENDER_CHOICES)
    followers = models.ManyToManyField("self",blank=True)
    following = models.ManyToManyField("self",blank=True)

    @property
    def post_count(self):
        return self.images.all().count()

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()

    # def get_absolute_url(self):
    #     return reverse("users:detail", kwargs={"username": self.username})
