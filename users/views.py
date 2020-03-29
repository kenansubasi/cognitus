from rest_framework import status, views, viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import User

from users.serializers import UserLoginSerializerV1, UserSerializerV1, UserRetrieveSerializerV1


class UserLoginViewV1(views.APIView):
    """
    Use this endpoint to login user (create user authentication token).
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = UserLoginSerializerV1(data=request.data)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.user)
            data = UserRetrieveSerializerV1(instance=serializer.user).data
            data.update({
                "auth_token": token.key
            })
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutViewV1(views.APIView):
    """
    Use this endpoint to logout user (remove user authentication token).
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class UserViewSetV1(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = "username"

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserRetrieveSerializerV1
        else:
            return UserSerializerV1

    def get_authenticators(self):
        authentication_classes = (TokenAuthentication,)
        return [auth() for auth in authentication_classes]

    def get_permissions(self):
        permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]
