from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserLoginSerializerV1(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False, style={"input_type": "password"})

    default_error_messages = {
        "inactive_account": "Your account is disabled.",
        "invalid_credentials": "Unable to login with provided credentials."
    }

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get("password"))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages["inactive_account"])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages["invalid_credentials"])


class UserSerializerV1(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")
        lookup_field = "username"
        extra_kwargs = {
            "url": {"lookup_field": "username"}
        }


class UserRetrieveSerializerV1(UserSerializerV1):
    pass
