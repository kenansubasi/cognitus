from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from data.models import Data
from data.serializers import DataSerializerV1, DataListSerializerV1, DataRetrieveSerializerV1


class DataViewSetV1(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Data.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == "list":
            return DataListSerializerV1
        elif self.action == "retrieve":
            return DataRetrieveSerializerV1
        else:
            return DataSerializerV1

    def get_authenticators(self):
        authentication_classes = (TokenAuthentication,)
        return [auth() for auth in authentication_classes]

    def get_permissions(self):
        permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]
