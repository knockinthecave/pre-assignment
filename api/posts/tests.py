import unittest
from rest_framework.test import APIClient
from django.urls import reverse
from .documents import Post
from api.users.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.post_url = reverse('posts')
        self.user = User.objects.create(
            email='test@example.com',
            password=make_password('test_password')
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.delete()

    def test_create_post(self):
        """
        게시글 생성 테스트
        """
        data = {
            'title': 'test title',
            'content': 'test content'
        }
        response = self.client.post(self.post_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.data['content'], 'test content')
        self.assertEqual(response.data['author_id'], self.user.id)
        self.assertTrue(
            Post.objects.filter(title='test title').count() == 1
        )
        self.assertTrue(
            Post.objects.filter(content='test content').count() == 1
        )
        self.assertTrue(
            Post.objects.filter(author_id=self.user.id).count() == 1
        )

    def test_create_post_with_no_credentials(self):
        """
        인증 없이 게시글 생성 테스트
        """
        self.client.credentials()
        data = {
            'title': 'test title',
            'content': 'test content'
        }
        response = self.client.post(self.post_url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_get_post(self):
        """
        게시글 조회 테스트
        """
        Post.objects.create(
            title='test title',
            content='test content',
            author_id=self.user.id
        )
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['title'],
                         'test title')
        self.assertEqual(response.data['results'][0]['content'],
                         'test content')
        self.assertEqual(response.data['results'][0]['author_id'],
                         str(self.user.id))


class PostParamterTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.post_url = reverse('posts')
        self.user = User.objects.create(
            email='test@example.com',
            password=make_password('test_password')
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.delete()

    def test_get_post_pagination(self):
        """
        게시글 페이징 조회 테스트
        """
        for i in range(1, 15):
            Post.objects.create(
                title=f'test title {i}',
                content=f'test content {i}',
                author_id=self.user.id
            )
        response = self.client.get(self.post_url, {'page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['results'][0]['title'],
                         'test title 1')
        self.assertEqual(response.data['results'][0]['content'],
                         'test content 1')
        self.assertEqual(response.data['results'][0]['author_id'],
                         str(self.user.id))
        self.assertEqual(response.data['results'][9]['title'],
                         'test title 10')
        self.assertEqual(response.data['results'][9]['content'],
                         'test content 10')
        self.assertEqual(response.data['results'][9]['author_id'],
                         str(self.user.id))

        response = self.client.get(self.post_url, {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 4)
        self.assertEqual(response.data['results'][0]['title'],
                         'test title 11')
        self.assertEqual(response.data['results'][0]['content'],
                         'test content 11')
        self.assertEqual(response.data['results'][0]['author_id'],
                         str(self.user.id))
        self.assertEqual(response.data['results'][3]['title'],
                         'test title 14')
        self.assertEqual(response.data['results'][3]['content'],
                         'test content 14')
        self.assertEqual(response.data['results'][3]['author_id'],
                         str(self.user.id))

    def test_get_post_with_author_id(self):
        """
        특정 사용자 게시글 조회 테스트
        """
        user2 = User.objects.create(
            email='test2@example.com',
            password=make_password('test_password')
        )

        Post.objects.create(
                title='test title user 2',
                content='test content user2',
                author_id=user2.id
            )

        author_id = user2.id

        response = self.client.get(self.post_url, {'author_id': author_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['author_id'],
                         str(user2.id))
        self.assertEqual(response.data['results'][0]['title'],
                         'test title user 2')
        self.assertEqual(response.data['results'][0]['content'],
                         'test content user2')


class PostDetailTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.post_url = reverse('posts')
        self.user = User.objects.create(
            email='test@example.com',
            password=make_password('test_password')
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.delete()

    def test_get_post_detail(self):
        """
        게시글 상세 조회 테스트
        """
        post = Post.objects.create(
            title='test title',
            content='test content',
            author_id=self.user.id
        )
        response = self.client.get(reverse('post-detail', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.data['content'], 'test content')
        self.assertEqual(response.data['author_id'], self.user.id)

    def test_put_post(self):
        """
        게시글 수정 테스트
        """
        post = Post.objects.create(
            title='test title',
            content='test content',
            author_id=self.user.id
        )
        data = {
            'title': 'test title updated',
            'content': 'test content updated'
        }
        response = self.client.put(reverse('post-detail', args=[post.id]),
                                   data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'test title updated')
        self.assertEqual(response.data['content'], 'test content updated')
        self.assertEqual(response.data['author_id'], self.user.id)

    def test_put_post_with_no_credentials(self):
        """
        인증 없이 게시글 수정 테스트
        """
        post = Post.objects.create(
            title='test title',
            content='test content',
            author_id=self.user.id
        )
        self.client.credentials()
        data = {
            'title': 'test title updated',
            'content': 'test content updated'
        }
        response = self.client.put(reverse('post-detail', args=[post.id]),
                                   data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Post.objects.filter(
            id=post.id).count(), 1)
        self.assertEqual(Post.objects.filter(
            title='test title').count(), 1)
        self.assertEqual(Post.objects.filter(
            content='test content').count(), 1)
        self.assertEqual(Post.objects.filter(
            author_id=self.user.id).count(), 1)

    def test_delete_post(self):
        """
        게시글 삭제 테스트
        """
        post = Post.objects.create(
            title='test title',
            content='test content',
            author_id=self.user.id
        )
        response = self.client.delete(reverse('post-detail', args=[post.id]))
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Post.objects.filter(
            id=post.id).count() == 0)
        self.assertTrue(Post.objects.filter(
            title='test title').count() == 0)
        self.assertTrue(Post.objects.filter(
            content='test content').count() == 0)
        self.assertTrue(Post.objects.filter(
            author_id=self.user.id).count() == 0)

    def test_delete_with_no_credentails(self):
        """
        인증 없이 게시글 삭제 테스트
        """
        post = Post.objects.create(
            title='test title',
            content='test content',
            author_id=self.user.id
        )
        self.client.credentials()
        response = self.client.delete(reverse('post-detail', args=[post.id]))
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Post.objects.filter(
            id=post.id).count() == 1)
        self.assertTrue(Post.objects.filter(
            title='test title').count() == 1)
        self.assertTrue(Post.objects.filter(
            content='test content').count() == 1)
        self.assertTrue(Post.objects.filter(
            author_id=self.user.id).count() == 1)
