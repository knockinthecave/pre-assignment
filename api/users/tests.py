import unittest
from rest_framework.test import APIClient
from django.urls import reverse
from .models import User, RefreshTokenModel
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta


class UserSignUpTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.user = User.objects.create(
            email='test@example.com',
            password=make_password('test_password')
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_user_signup(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'new_password'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(
            email='newuser@example.com').exists()
                        )

    def test_user_signup_with_existing_email(self):
        """
        이미 존재하는 이메일로 회원가입 테스트
        """
        data = {
            'email': 'test@example.com',
            'password': 'test_password'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['msg'],
            'test@example.com은 이미 존재하는 이메일입니다.'
        )

    def test_user_signup_with_no_email(self):
        """
        이메일 없이 회원가입 테스트
        """
        data = {
            'password': 'test_password'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_signup_with_no_password(self):
        """
        비밀번호 없이 회원가입 테스트
        """
        data = {
            'email': 'test@example.com',
        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, 400)


class UserLoginTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.user = User.objects.create(
            email='test@example.com',
            password=make_password('test_password')
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_user_login(self):
        """
        사용자 로그인 테스트
        """
        data = {
            'email': 'test@example.com',
            'password': 'test_password'
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

    def test_user_login_with_no_email(self):
        """
        이메일 없이 로그인 테스트
        """
        data = {
            'password': 'test_password'
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_no_password(self):
        """
        비밀번호 없이 로그인 테스트
        """
        data = {
            'email': 'test@example.com',
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_wrong_password(self):
        """
        잘못된 비밀번호로 로그인 테스트
        """
        data = {
            'email': 'test@example.com',
            'password': 'wrong_password'
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['msg'],
            '비밀번호가 일치하지 않습니다.'
        )


class UserTokenRefreshTestCase(unittest.TestCase):
    def setUp(self):
        """
        로그인 후 리프레시 토큰 생성
        """
        self.client = APIClient()
        self.refresh_url = reverse('refresh')
        self.user = User.objects.create(
            email='test@example.com',
            password=make_password('test_password')
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(self.refresh)
        RefreshTokenModel.objects.create(
            user=self.user,
            refresh_token=self.refresh_token
        )

    def tearDown(self):
        User.objects.all().delete()
        RefreshTokenModel.objects.all().delete()

    def test_token_refresh(self):
        """
        토큰 갱신 테스트
        """
        data = {
            'refresh_token': self.refresh_token
        }
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_token_refresh_with_expired_token(self):
        """
        만료된 토큰으로 갱신 테스트
        """
        self.refresh.set_exp(lifetime=timedelta(seconds=-1))
        expired_refresh_token = str(self.refresh)

        data = {
            'refresh_token': expired_refresh_token
        }
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['msg'],
            '유효하지 않은 토큰입니다.'
        )

    def test_token_refresh_with_invalid_token(self):
        """
        유효하지 않은 토큰으로 갱신 테스트
        """
        data = {
            'refresh_token': 'invalid_token'
        }
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['msg'],
            '유효하지 않은 토큰입니다.'
        )


class UserLogoutTestCase(unittest.TestCase):
    def setUp(self):
        """
        로그인 후 로그아웃
        """
        self.client = APIClient()
        self.logout_url = reverse('logout')
        self.user = User.objects.create(
            email='test@example.com',
            password=make_password('test_password')
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(self.refresh)
        RefreshTokenModel.objects.create(
            user=self.user,
            refresh_token=self.refresh_token
        )

    def tearDown(self):
        User.objects.all().delete()
        RefreshTokenModel.objects.all().delete()

    def test_user_logout(self):
        """
        유효한 토큰으로 로그아웃 테스트
        """
        data = {
            'refresh_token': self.refresh_token
        }
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['msg'], '로그아웃 되었습니다.')
        self.assertFalse(RefreshTokenModel.objects.filter(
            refresh_token=self.refresh_token).exists())

    def test_user_logout_with_invalid_token(self):
        """
        유효하지 않은 토큰으로 로그아웃 테스트
        """
        data = {
            'refresh_token': 'invalid_token'
        }
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['msg'], '유효하지 않은 토큰입니다.')

    def test_user_logout_with_no_token(self):
        """
        토큰 없이 로그아웃 테스트
        """
        data = {}
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['msg'], '토큰이 제공되지 않았습니다.')
