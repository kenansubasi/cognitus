from rest_framework import serializers

from data.models import Data
from users.serializers import UserSerializerV1


class DataSerializerV1(serializers.ModelSerializer):
    creator = UserSerializerV1(read_only=True)

    class Meta:
        model = Data
        fields = ("id", "text", "label", "creator", "created_at", "updated_at")


class DataListSerializerV1(DataSerializerV1):
    pass


class DataCreateSerializerV1(DataSerializerV1):

    class Meta:
        model = Data
        fields = ("id", "text", "label")


class DataRetrieveSerializerV1(DataSerializerV1):
    pass


class DataUpdateSerializerV1(DataSerializerV1):

    class Meta:
        model = Data
        fields = ("id", "text", "label")
