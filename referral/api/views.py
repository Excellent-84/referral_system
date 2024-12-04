import random
from time import sleep

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from users.utils import generate_invite_code

from .serializers import (
    InviteCodeSerializer,
    PhoneAuthSerializer,
    UsersSerializer,
    VerifySerializer
)

User = get_user_model()

CODE_STORAGE = {}


class PhoneAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        if not User.validate_phone_number(phone_number):
            return Response(
                {'error': 'Неверный номер'},
                status=status.HTTP_400_BAD_REQUEST
            )

        code = str(random.randint(1000, 9999))
        CODE_STORAGE[code] = phone_number
        sleep(2)
        return Response({'message': f'Код активации: {code}'})


class VerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        phone_number = CODE_STORAGE.get(code)
        if not phone_number:
            return Response(
                {'error': 'Неверный код активации'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            user.invite_code = generate_invite_code()
            user.save()

        del CODE_STORAGE[code]

        token = AccessToken.for_user(user)
        return Response({'Токен': str(token)})


class ProfileView(APIView):
    def get(self, request):
        user = request.user
        referrals_count = user.referrals.count()
        activated_invite_code = (
            user.referred_by.invite_code if user.referred_by else None
        )

        return Response({
            'phone_number': user.phone_number,
            'invite_code': user.invite_code,
            'activated_invite_code': activated_invite_code,
            'referrals_count': referrals_count,
            'referrals': [
                {'phone_number': u.phone_number} for u in user.referrals.all()
            ],
        })


class ActivateInviteView(APIView):

    def post(self, request):
        user = request.user

        if user.referred_by:
            return Response(
                {'error': 'Активировать можно только один инвайт-код'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InviteCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite_code = serializer.validated_data['invite_code']

        if user.invite_code == invite_code:
            return Response(
                {'error': 'Свой инвайт-код использовать нельзя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        referred_user = User.objects.filter(invite_code=invite_code).first()

        if not referred_user:
            return Response(
                {'error': 'Недействительный инвайт-код'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.referred_by = referred_user
        user.save()
        return Response({'message': 'Инвайт-код активирован'})


class UsersListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
