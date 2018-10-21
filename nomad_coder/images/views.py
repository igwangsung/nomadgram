#from django.shortcuts import render #For using Template Concept of Django
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from nomad_coder.notifications import views as notification_views
from nomad_coder.users import models as user_models
from nomad_coder.users import serializers as user_serializers

class ListAllImages(APIView):

    def get(self, request, format=None): #form=None means returning JSON
        
        all_images = models.Image.objects.all()

        serializer = serializers.ImageSerializer(all_images, many=True) #serializer is Class
        
        return Response(data=serializer.data) #data  쓰는거 잊지말기!! 

class ListAllComments(APIView):

    def get(self, request, format=None):
        
        all_comments = models.Comment.objects.all()

        serializer = serializers.CommentSerializer(all_comments, many=True)

        return Response(data=serializer.data)

class ListAllLikes(APIView):

    def get(self, request, format=None):

        
        all_likes = models.Like.objects.all()

        serializer = serializers.LikeSerializer(all_likes, many=True)

        return Response(data=serializer.data)

class Images(APIView):

    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()

        image_list = []
        
        for following_user in following_users:

            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        my_images = user.images.all()[:2]

        for image in my_images:
            image_list.append(image)
        #There are some bugs bc of created_at, updated_at Field
        #InLine Function --> lambda
        sorted_list = sorted(image_list,key=lambda image:  image.created_at, reverse=True)  

        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(data=serializer.data)

    def post(self, request, format=None):

        user = request.user

        serializer = serializers.InputImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDetail(APIView):
    
    def find_own_image(self, image_id, user):

        try:
            image = models.Image.objects.get(id=image_id, creator=user)
            return image
        except models.Image.DoesNotExist:
            return None


    def get(self, request, image_id, format=None):

        user = request.user

        try:
            image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        #Is Single so, I don't need 'many=True'
        serializer = serializers.ImageSerializer(image)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def put(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        #부분 update 할때  partial 속성 이용하기
        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)

        if serializer.is_valid():
            
            serializer.save(creator=user)
            
            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, image_id, format=True):
        
        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeImage(APIView):
    
    #updated_at, created_at is datetime.datetime(), tzinfo=<UTC>
    #query 안의 데이터들을 추출할수있고 볼수있다!!!!!
    def get(self, request, image_id, format=None):
        
        likes = models.Like.objects.filter(image__id=image_id)

        like_creator_ids = likes.values('creator_id') # DB objects makes automatically creator_id...?
       
        users = user_models.User.objects.filter(id__in=like_creator_ids)

        serializer = user_serializers.ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, image_id, format=None):
        
        user = request.user

        #create notification for like

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try: 
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except models.Like.DoesNotExist:

            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )

            new_like.save()

            notification_views.create_notification(creator=user, to=found_image.creator, type='like', image=found_image)


            return Response(status=status.HTTP_201_CREATED)

            
class UnLikeImage(APIView):
    
    def delete(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try: 
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            preexisting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:

            return Response(status=status.HTTP_304_NOT_MODIFIED)

class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):
        
        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user, image=found_image)

            notification_views.create_notification(creator=user, to=found_image.creator, type='comment', image=found_image, comment=serializer.data["message"])

            return Response(data=serializer.data, status=status.HTTP_201_CREATED) #Response Django REST 에서 보이는거
        
        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class Comment(APIView):

    def delete(self, request, comment_id, format=None):

        user = request.user
        
        #create notification for Comment

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
#timezone.now() 공부하기

class ModerateComment(APIView):

    def delete(self, request, image_id, comment_id, format=None):

        user = request.user
        #Comment Model has the Image Attribute
        try: 
            comment_to_delete = models.Comment.objects.get(id=comment_id, image__id=image_id, image__creator=user)
            comment_to_delete.delete()
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)



class Search(APIView):

    def get(self, request, format=None):

        hashtags = request.query_params.get('hashtags', None)

        if hashtags is not None:
            hashtags = hashtags.split(',')

            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        