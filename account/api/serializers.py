# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth import authenticate


# User = get_user_model()


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         error_messages={
#             "required": "E-poçt vacibdir.",
#             "blank": "E-poçt boş ola bilməz.",
#         },
#     )
#     username = serializers.CharField(
#         required=True,
#         error_messages={
#             "required": "İstifadəçi adı vacibdir.",
#             "blank": "İstifadəçi adı boş ola bilməz.",
#         },
#     )
#     password = serializers.CharField(
#         write_only=True, required=True, style={"input_type": "password"}
#     )
#     password2 = serializers.CharField(
#         write_only=True, required=True, style={"input_type": "password"}
#     )

#     class Meta:
#         model = User
#         fields = ["username", "email", "password", "password2"]

#     def validate(self, data):
#         if data["password"] != data["password2"]:
#             raise serializers.ValidationError({"password": "Şifrələr uyğun gəlmir."})

#         if User.objects.filter(email=data["email"]).exists():
#             raise ValidationError({"email": "Bu e-poçt artıq qeydiyyatdan keçib."})

#         if User.objects.filter(username=data["username"]).exists():
#             raise ValidationError(
#                 {"username": "Bu istifadəçi adı artıq qeydiyyatdan keçib."}
#             )

#         return data

#     def create(self, validated_data):
#         validated_data.pop("password2")
#         user = User.objects.create_user(**validated_data)
#         return user


# class CustomLoginSerializer(serializers.Serializer):
#     username = serializers.CharField(
#         required=True,
#         error_messages={
#             "required": "İstifadəçi adı vacibdir.",
#             "blank": "İstifadəçi adı boş ola bilməz.",
#         },
#     )
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         style={"input_type": "password"},
#         error_messages={
#             "required": "Şifrə vacibdir.",
#             "blank": "Şifrə boş ola bilməz.",
#         },
#     )

#     def validate(self, data):
#         username = data.get("username")
#         password = data.get("password")

#         user = authenticate(username=username, password=password)

#         if user is None:
#             raise serializers.ValidationError("İstifadəçi adı və ya şifrə yalnışdır.")

#         data["user"] = user
#         return data
