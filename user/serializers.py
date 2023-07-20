from rest_framework import serializers
from rest_framework.fields import empty
from user.models import CustomUser
from django.contrib.auth.models import Permission, Group
from django.utils.translation import ngettext


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        exclude = ["content_type"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model: Group
        fields = "__all__"


class UserBaseSerializer(serializers.ModelSerializer):
    # extra_fields = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "password",
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "address",
            "room",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "room": {"read_only": True, "required": True},
            "username": {"required": True},
            "email": {"required": True},
            "mobile_number": {"required": True},
            "password": {"write_only": True, "required": True},
        }

    # def __init__(self, instance=None, data=..., **kwargs):
    #     super().__init__(instance, data, **kwargs)
    #     allowed_fields = set(self.fields.keys())
    #     provided_fields = set(self.initial_data.keys())
    #     extra_fields = provided_fields - allowed_fields
    #     if extra_fields:
    #         message = ngettext(
    #             "Unknown field",
    #             "Unknown fields",
    #             len(extra_fields),
    #         ) % {
    #             "field_name": extra_fields,
    #             "field_names": extra_fields,
    #         }
    #         raise serializers.ValidationError({"Error": {message: list(extra_fields)}})


class RegularUserSerializer(UserBaseSerializer):
    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value


class StaffUserSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + [
            "date_joined",
            "updated_at",
            "last_login",
        ]
        extra_kwargs = {
            "date_joined": {"read_only": True},
            "updated_at": {"read_only": True},
            "last_login": {"read_only": True},
            "password": {"write_only": True, "required": True},
        }


class SuperUserSerializer(StaffUserSerializer):
    class Meta(StaffUserSerializer.Meta):
        fields = StaffUserSerializer.Meta.fields + [
            "is_active",
            "is_staff",
            "is_superuser",
        ]


# class GetUserSerializerForAdmin(serializers.ModelSerializer):
#     user_permissions = UserPermissionSerializer(many=True)
#     groups = GroupSerializer(many=True)

#     class Meta:
#         model = CustomUser
#         fields = "__all__"
#         # exclude = ["user_permissions", "groups"]
#         extra_kwargs = {"password": {"write_only": True}}


class GetUserQuerySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)


# class DynamicFieldsModelSerializer(serializers.ModelSerializer):
#     """
#     A ModelSerializer that takes an additional `fields` argument that
#     controls which fields should be displayed.
#     """

#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop('fields', None)

#         # Instantiate the superclass normally
#         super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

#         if fields is not None:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)

# class SimplePersonSerializer(DynamicFieldsModelSerializer):
#     class Meta:
#         model = Person
#         fields = '__all__'
