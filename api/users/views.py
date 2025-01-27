from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, RefreshTokenModel
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError


class UserSignUpAPIView(APIView):
    """
    회원가입 API
    """
    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get('email'))
            return Response({
                'msg': f'{user.email}은 이미 존재하는 이메일입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    """
    로그인 API
    """
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({
                    'msg': '이메일과 비밀번호를 모두 입력해주세요.'
                }, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=email)

            if not check_password(password, user.password):
                return Response({
                    'msg': '비밀번호가 일치하지 않습니다.'
                }, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            RefreshTokenModel.objects.create(
                user=user,
                refresh_token=refresh_token
            )

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'msg': '존재하지 않는 사용자입니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)
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


class UserTokenRefreshAPIView(APIView):
    """
    토큰 갱신 API
    """
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({
                    'msg': '토큰이 제공되지 않았습니다.'
                }, status=status.HTTP_400_BAD_REQUEST)

            refresh_token_obj = RefreshTokenModel.objects.filter(
                refresh_token=refresh_token
            ).first()

            if refresh_token_obj is None:
                return Response({
                    'msg': '유효하지 않은 토큰입니다.'
                }, status=status.HTTP_401_UNAUTHORIZED)

            refresh_token_obj.delete()
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            RefreshTokenModel.objects.create(
                user=refresh_token_obj.user,
                refresh_token=refresh_token
            )

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_200_OK)

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


class UserLogoutAPIView(APIView):
    """
    로그아웃 API
    """
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({
                    'msg': '토큰이 제공되지 않았습니다.'
                }, status=status.HTTP_400_BAD_REQUEST)

            refresh_token_obj = RefreshTokenModel.objects.filter(
                refresh_token=refresh_token
            ).first()

            if refresh_token_obj is None:
                return Response({
                    'msg': '유효하지 않은 토큰입니다.'
                }, status=status.HTTP_401_UNAUTHORIZED)

            refresh_token_obj.delete()
            return Response({'msg': '로그아웃 되었습니다.'},
                            status=status.HTTP_200_OK)
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
