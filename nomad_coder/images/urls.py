# from django.conf.urls import url
# #import url is function!
# #module can include Class or Function so...
# from . import views
# app_name = "images" #NEW WAY

# urlpatterns = [
#     url(
#         regex=r'^all/$',
#         view=views.ListAllImages.as_view(), #ListAllImages is Class
#         name='all_images' #ORM name
#     )
# ]

from django.urls import path
from . import views

app_name = "images"
urlpatterns = [
    # path("all/", view=views.ListAllImages.as_view(), name="all_images"),
    # path("comments/", view=views.ListAllComments.as_view(), name="all_comments"),
    # path("likes/", view=views.ListAllLikes.as_view(), name="all_likes"),
    path("", view=views.Images.as_view(), name="feed"),
    path("<int:image_id>/", view=views.ImageDetail.as_view(), name="image_detail"), #name은 뭐지?
    path("<int:image_id>/likes/", view=views.LikeImage.as_view(), name="like_image"), #name은 뭐지?
    path("<int:image_id>/unlikes/", view=views.UnLikeImage.as_view(), name="unlike_image"), #name은 뭐지?
    path("<int:image_id>/comments/<int:comment_id>/", view=views.ModerateComment.as_view(), name="moderate_comment"),
    path("<int:image_id>/comments/", view=views.CommentOnImage.as_view(), name="comment_image"),
    path("comments/<int:comment_id>/", view=views.Comment.as_view(), name="comment"),
    path("search/", view=views.Search.as_view(), name="search"),

] 