from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from data.models import Data
from data.serializers import (
    DataSerializerV1, DataListSerializerV1, DataCreateSerializerV1, DataUpdateSerializerV1, DataRetrieveSerializerV1
)


class DataViewSetV1(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    def get_queryset(self):
        if self.action in ["update", "destroy"]:
            return Data.objects.filter(creator=self.request.user).order_by("-id")
        else:
            return Data.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == "list":
            return DataListSerializerV1
        elif self.action == "create":
            return DataCreateSerializerV1
        elif self.action == "retrieve":
            return DataRetrieveSerializerV1
        elif self.action == "update":
            return DataUpdateSerializerV1
        else:
            return DataSerializerV1

    def get_authenticators(self):
        authentication_classes = (TokenAuthentication,)
        return [auth() for auth in authentication_classes]

    def get_permissions(self):
        permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
