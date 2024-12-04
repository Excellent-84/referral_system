from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)


class PhoneAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class VerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)


class UsersSerializer(serializers.ModelSerializer):
    activated_invites_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'invite_code', 'activated_invites_count')

    def get_activated_invites_count(self, obj):
        return obj.referrals.count()
