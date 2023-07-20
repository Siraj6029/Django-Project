from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from user.models import CustomUser
from user.serializers import (
    GetUserQuerySerializer,
    RegularUserSerializer,
    StaffUserSerializer,
    SuperUserSerializer,
)
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from user.permissions import IsOwnerPermission, IsSuperUserOnly, IsStaffUserOnly
from rest_framework.generics import get_object_or_404
from django.http import Http404


class GetUserView(APIView):
    """
    A custom API view for handling user related operations

    ...

    GET:
    retrive specific user

    Request Data:
    - id (int, query-params): id of user

    Returns JSON:
    - id (int): Id of user
    - username (str): user name of user
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUserOnly | IsOwnerPermission | IsStaffUserOnly]

    def get(self, request: Request):
        try:
            query_serializer = GetUserQuerySerializer(data=request.query_params)
            query_serializer.is_valid(raise_exception=True)
            breakpoint()

            user_id = query_serializer.validated_data.get("id")
            try:
                user = get_object_or_404(CustomUser, id=user_id)
            except Http404:
                raise NotFound("User not found")

            self.check_object_permissions(request, user)

            if request.user.is_superuser:
                serializer = SuperUserSerializer(instance=user)
            elif request.user.is_staff:
                serializer = StaffUserSerializer(instance=user)
            else:
                serializer = RegularUserSerializer(instance=user)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except NotFound as e:
            return Response({"error": e.detail}, status=status.HTTP_404_NOT_FOUND)

        except PermissionDenied as e:
            return Response({"error": e.detail}, status=status.HTTP_403_FORBIDDEN)

        except ValidationError as e:
            return Response(
                {"error": e.detail}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateUserView(generics.CreateAPIView):
    serializer_class = RegularUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
