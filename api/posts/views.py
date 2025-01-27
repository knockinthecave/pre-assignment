from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.posts.documents import Post
from rest_framework.pagination import PageNumberPagination
from bson import ObjectId
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostPermissons():
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class PostAPIView(PostPermissons, APIView):
    """
    게시글 API
    """
    def post(self, request):
        try:
            data = request.data
            title = data.get('title')
            content = data.get('content')
            author_id = request.user.id

            if not title or not content:
                return Response({
                    'msg': '제목과 내용을 모두 입력해주세요.'
                }, status=status.HTTP_400_BAD_REQUEST)

            post = Post(
                title=title,
                content=content,
                author_id=author_id
            )

            post.save()

            return Response({
                'id': str(post.id),
                'title': post.title,
                'content': post.content,
                'author_id': post.author_id,
                'created_at': post.created_at
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({
                'msg': '유효하지 않은 데이터입니다.',
                'errors': e.message_dict
            }, status=status.HTTP_400_BAD_REQUEST)
        except (InvalidToken, TokenError):
            return Response({
                'msg': '유효하지 않은 토큰입니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'msg': '서버 오류가 발생했습니다.',
                'errors': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            paginator = PostPagination()
            author_params = request.query_params.get('author_id')

            if author_params:
                posts = Post.objects(author_id=author_params)
            else:
                posts = Post.objects()

            result_page = paginator.paginate_queryset(posts,
                                                      request,
                                                      view=self)
            if result_page is not None:
                data = [
                    {
                        'id': str(post.id),
                        'title': post.title,
                        'content': post.content,
                        'author_id': str(post.author_id),
                        'created_at': post.created_at
                    } for post in result_page
                ]
                return paginator.get_paginated_response(data)

            return Response([
                {
                    'id': str(post.id),
                    'title': post.title,
                    'content': post.content,
                    'author_id': str(post.author_id),
                    'created_at': post.created_at
                } for post in posts
            ], status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'msg': '유효하지 않은 데이터입니다.',
                'errors': e.message_dict
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'msg': '서버 오류가 발생했습니다.',
                'errors': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetailAPIView(PostPermissons, APIView):
    """
    게시글 상세 조회, 수정, 삭제 API
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=ObjectId(post_id))
            return Response({
                'id': str(post.id),
                'title': post.title,
                'content': post.content,
                'author_id': post.author_id,
                'created_at': post.created_at
            }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({
                'msg': '존재하지 않는 게시글입니다.'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({
                'msg': '유효하지 않은 데이터입니다.',
                'errors': e.message_dict
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'msg': '서버 오류가 발생했습니다.',
                'errors': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=ObjectId(post_id))
            data = request.data

            post.title = data.get('title', post.title)
            post.content = data.get('content', post.content)
            post.save()

            return Response({
                'id': str(post.id),
                'title': post.title,
                'content': post.content,
                'author_id': post.author_id,
                'created_at': post.created_at
            }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({
                'msg': '존재하지 않는 게시글입니다.'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({
                'msg': '유효하지 않은 데이터입니다.',
                'errors': e.message_dict
            }, status=status.HTTP_400_BAD_REQUEST)
        except (InvalidToken, TokenError):
            return Response({
                'msg': '유효하지 않은 토큰입니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'msg': '서버 오류가 발생했습니다.',
                'errors': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=ObjectId(post_id))
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({
                'msg': '존재하지 않는 게시글입니다.'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({
                'msg': '유효하지 않은 데이터입니다.',
                'errors': e.message_dict
            }, status=status.HTTP_400_BAD_REQUEST)
        except (InvalidToken, TokenError):
            return Response({
                'msg': '유효하지 않은 토큰입니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'msg': '서버 오류가 발생했습니다.',
                'errors': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
