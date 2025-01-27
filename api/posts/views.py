from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.posts.documents import Post
from rest_framework.pagination import PageNumberPagination
from bson import ObjectId


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
        data = request.data
        title = data.get('title')
        content = data.get('content')
        author_id = request.user.id

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

    def get(self, request):
        paginator = PostPagination()
        author_params = request.query_params.get('author_id')

        if author_params:
            posts = Post.objects(author_id=author_params)
        else:
            posts = Post.objects()

        result_page = paginator.paginate_queryset(posts, request, view=self)
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
        ])


class PostDetailAPIView(PostPermissons, APIView):
    """
    게시글 상세 조회, 수정, 삭제 API
    """
    def get(self, request, post_id):
        post = Post.objects.get(
            id=ObjectId(post_id)
        )
        return Response({
            'id': str(post.id),
            'title': post.title,
            'content': post.content,
            'author_id': post.author_id,
            'created_at': post.created_at
        })

    def put(self, request, post_id):
        post = Post.objects.get(id=ObjectId(post_id))
        data = request.data

        post.title = data.get('title')
        post.content = data.get('content')
        post.save()

        return Response({
            'id': str(post.id),
            'title': post.title,
            'content': post.content,
            'author_id': post.author_id,
            'created_at': post.created_at
        })

    def delete(self, request, post_id):
        post = Post.objects.get(id=ObjectId(post_id))
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
