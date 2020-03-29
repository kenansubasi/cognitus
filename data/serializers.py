from rest_framework import serializers

from data.models import Data
from users.serializers import UserSerializerV1


class DataSerializerV1(serializers.ModelSerializer):
    creator = UserSerializerV1(read_only=True)

    class Meta:
        model = Data
        fields = ("id", "label", "text", "creator", "created_at", "updated_at")


class DataListSerializerV1(DataSerializerV1):
    pass
