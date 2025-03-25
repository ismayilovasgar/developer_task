from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, CustomLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "İstifadəçi uğurla yaradıldı."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomLoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = CustomLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data["user"]

#             refresh = RefreshToken.for_user(user)
#             access_token = refresh.access_token

#             # Token'ları döndür
#             return Response({"refresh": str(refresh), "access": str(access_token)})

#         return Response(serializer.errors, status=400)

class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({
                "access": response.data["access"],
                "refresh": response.data["refresh"],
                "redirect": "/home"
            }, status=status.HTTP_200_OK)
        return response




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Yalnız daxil olmuş istifadəçilər çıxış edə bilər

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token tələb olunur!"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Token-i qara siyahıya əlavə et

            return Response({"message": "Çıxış uğurla tamamlandı."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Etibarsız token!"}, status=status.HTTP_400_BAD_REQUEST)
