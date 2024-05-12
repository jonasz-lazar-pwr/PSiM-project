# Autorzy: Jonasz Lazar, Kacper Malinowski

import qrcode
from io import BytesIO
import base64

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User, Dwarf, UserDwarf, Comment, UserAchievement, Achievement
from .serializers import (
    UserSerializer,
    DwarfSerializer,
    RegisterSerializer,
    DwarfDetailSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    UserAchievementSerializer,
    AchievementSerializer
)
from .utils import (
    check_and_assign_dwarf_achievements,
    check_and_assign_comment_achievements,
    check_and_remove_comment_achievements
)


class HomePageView(APIView):

    def get(self, request):
        routes = [
            '/admin/',
            '/token/',
            '/token/refresh/',
            '/swagger/',
            '/redoc/',
            '/home/',
            '/user/',
            '/register/',
            '/logout/',
            '/dwarfs/',
            '/dwarfs/<int:pk>/',
            '/dwarfs/<int:pk>/qr_code/',
            '/dwarfs/<int:pk>/comments/',
            '/comments/<int:pk>/',
            '/verify_qr_code/',
            '/users_ranking/',
            '/user_comments/',
            '/user_achievements/',
            '/achievements_to_gain/',
        ]
        return Response(routes)


class LogoutView(APIView):
    """
    Widok wylogowania użytkownika.

    Ten widok obsługuje żądanie POST do wylogowania użytkownika.
    Wymaga uwierzytelnienia.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Wylogowanie użytkownika.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            }
        ),
        responses={
            205: 'Wylogowanie udane.',
            400: 'Błąd wylogowania.'
        },
    )
    def post(self, request):
        """
        Metoda obsługująca żądanie POST.

        Próbuje wylogować użytkownika za pomocą przesłanego w żądaniu refresh tokena.
        Jeżeli operacja jest udana, zwraca status 205 (Reset Content).
        Jeżeli operacja nie jest udana, zwraca status 400 (Bad Request).
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    """
    Widok rejestracji użytkownika.

    Jeżeli metoda żądania to 'POST', próbuje zarejestrować użytkownika za pomocą danych przesłanych w żądaniu.
    Jeżeli rejestracja jest udana, loguje użytkownika i zwraca odpowiedź z danymi użytkownika.
    Jeżeli rejestracja nie jest udana, zwraca błąd z informacją o błędach walidacji.
    Jeżeli metoda żądania to 'GET', renderuje formularz rejestracji.
    """

    @swagger_auto_schema(
        operation_description="Rejestracja nowego użytkownika.",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(description="Rejestracja udana.", schema=RegisterSerializer),
            400: "Błąd walidacji."
        },
    )
    def post(self, request):
        """
        Metoda obsługująca żądanie POST.

        Próbuje zarejestrować użytkownika za pomocą danych przesłanych w żądaniu.
        Używa serializera RegisterSerializer do walidacji danych.
        Jeżeli dane są prawidłowe, tworzy nowego użytkownika, loguje go, a następnie zwraca odpowiedź z danymi użytkownika.
        Jeżeli dane są nieprawidłowe, zwraca błąd z informacją o błędach walidacji.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.RetrieveAPIView):
    """
    Widok szczegółów użytkownika.

    Ten widok zwraca szczegółowe informacje o zalogowanym użytkowniku.
    Wymaga uwierzytelnienia.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Pobranie szczegółów zalogowanego użytkownika.",
        responses={
            200: openapi.Response(description="Szczegóły zalogowanego użytkownika.", schema=UserSerializer),
            401: "Nieautoryzowany."
        },
    )
    def get_object(self):
        """
        Metoda zwracająca zalogowanego użytkownika.

        Ta metoda jest wywoływana, gdy do serwera wysłane jest żądanie GET.
        Zwraca obiekt zalogowanego użytkownika.
        """
        return self.request.user


class DwarfListView(APIView):
    """
    Widok listy krasnoludków.

    GET:
    Zwraca listę krasnoludków, które pasują do zapytania wyszukiwania przesłanego w żądaniu.
    Jeżeli zapytanie wyszukiwania jest puste, zwraca wszystkie krasnoludki.
    Zwraca listę krasnoludków, liczbę wszystkich krasnoludków oraz liczbę krasnoludków odwiedzonych przez zalogowanego użytkownika.
    Nie wymaga uwierzytelnienia.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Pobranie listy krasnoludków.",
        responses={
            200: openapi.Response(
                description="Lista krasnoludków, liczba wszystkich krasnoludków oraz liczba krasnoludków odwiedzonych "
                            "przez zalogowanego użytkownika.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_dwarfs': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of dwarfs'),
                        'user_dwarfs_count': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                            description='Number of dwarfs visited by the user'),
                        'dwarfs': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                 items=openapi.Schema(type=openapi.TYPE_OBJECT),
                                                 description='List of dwarfs')
                    }
                )
            )
        },
    )
    def get(self, request):
        """
        Metoda obsługująca żądanie GET.

        Próbuje pobrać listę krasnoludków, które pasują do zapytania wyszukiwania przesłanego w żądaniu.
        Jeżeli zapytanie wyszukiwania jest puste, zwraca wszystkie krasnoludki.
        Zwraca listę krasnoludków, liczbę wszystkich krasnoludków oraz liczbę krasnoludków odwiedzonych przez zalogowanego użytkownika.
        """
        query = request.query_params.get('q', '')
        dwarfs = Dwarf.objects.filter(name__icontains=query).order_by('name')
        serializer = DwarfSerializer(dwarfs, many=True, context={'request': request})

        total_dwarfs = Dwarf.objects.count()
        user_dwarfs_count = 0
        if request.user.is_authenticated:
            user_dwarfs_count = UserDwarf.objects.filter(user=request.user).count()

        return Response({
            'total_dwarfs': total_dwarfs,
            'user_dwarfs_count': user_dwarfs_count,
            'dwarfs': serializer.data
        })


class DwarfDetailView(generics.RetrieveAPIView):
    """
    Widok szczegółów krasnoludka.

    GET:
    Zwraca szczegółowe informacje o krasnoludku.
    Nie wymaga uwierzytelnienia.
    """

    queryset = Dwarf.objects.all()
    serializer_class = DwarfDetailSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Pobranie szczegółów krasnoludka.",
        responses={
            200: openapi.Response(description="Szczegóły krasnoludka.", schema=DwarfDetailSerializer),
            404: "Nie znaleziono krasnoludka."
        },
    )
    def get_serializer_context(self):
        """
        Metoda zwracająca kontekst serializera.

        Ta metoda jest wywoływana, gdy do serwera wysłane jest żądanie GET.
        Zwraca kontekst serializera, który jest używany do serializacji danych.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class CommentDeleteView(generics.DestroyAPIView):
    """
    Widok usuwania komentarza.

    DELETE:
    Usuwa komentarz.
    Wymaga uwierzytelnienia i tego, że zalogowany użytkownik jest autorem komentarza.
    """

    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Usuwanie komentarza.",
        responses={
            204: 'No Content',
            403: 'Forbidden',
            404: 'Nie znaleziono komentarza.'
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Metoda obsługująca żądanie DELETE.

        Próbuje usunąć komentarz. Jeżeli zalogowany użytkownik jest autorem komentarza, usuwa komentarz i zwraca
        status 204 (No Content). Jeżeli zalogowany użytkownik nie jest autorem komentarza, zwraca status 403 (
        Forbidden).
        """
        comment = self.get_object()
        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        response = super().delete(request, *args, **kwargs)
        check_and_remove_comment_achievements(request.user)
        return response


class CommentCreateView(APIView):
    """
    Widok tworzenia komentarza.

    POST:
    Tworzy komentarz.
    Wymaga uwierzytelnienia i tego, że zalogowany użytkownik zdobył krasnoludka, do którego chce dodać komentarz.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Tworzenie komentarza.",
        request_body=CommentCreateSerializer,
        responses={
            201: openapi.Response(description="Utworzenie komentarza udane.", schema=CommentCreateSerializer),
            400: "Błąd walidacji.",
            401: "Nieautoryzowany.",
            403: "Zabronione."
        },
    )
    def post(self, request, pk):
        """
        Metoda obsługująca żądanie POST.

        Próbuje utworzyć komentarz za pomocą danych przesłanych w żądaniu.
        Sprawdza, czy użytkownik jest zalogowany, czy zdobył krasnoludka, do którego chce dodać komentarz, oraz czy nie dodał jeszcze komentarza do danego krasnoludka.
        Jeżeli wszystkie warunki są spełnione, tworzy komentarz, a następnie zwraca odpowiedź z danymi komentarza.
        Jeżeli któreś z warunków nie jest spełnione, zwraca odpowiedni kod błędu.
        """
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        dwarf = Dwarf.objects.get(pk=pk)
        if not UserDwarf.objects.filter(user=request.user, dwarf=dwarf).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        if Comment.objects.filter(user=request.user, dwarf=dwarf).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            Comment.objects.create(user=request.user, dwarf=dwarf,
                                   comment_text=serializer.validated_data['comment_text'])
            check_and_assign_comment_achievements(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateQRCodeView(APIView):
    """
    Widok generowania kodu QR.

    GET:
    Generuje kod QR, który prowadzi do szczegółów krasnoludka o podanym ID.
    Wymaga uwierzytelnienia i uprawnień administratora.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_description="Generowanie kodu QR dla krasnoludka.",
        responses={
            200: openapi.Response(description="Kod QR dla krasnoludka.", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'qr_code': openapi.Schema(type=openapi.TYPE_STRING,
                                              description='Kod QR jako string w formacie base64')
                }
            )),
            401: "Nieautoryzowany.",
            403: "Zabronione.",
            404: "Nie znaleziono krasnoludka."
        },
    )
    def get(self, request, pk):
        """
        Metoda obsługująca żądanie GET.

        Próbuje pobrać krasnoludka o podanym ID. Jeżeli krasnoludek istnieje, generuje kod QR, który prowadzi do szczegółów tego krasnoludka.
        Kod QR jest zapisywany jako obraz PNG, a następnie konwertowany na string w formacie base64.
        Zwraca odpowiedź z kodem QR jako stringiem w formacie base64.
        Jeżeli krasnoludek nie istnieje, zwraca status 404 (Not Found).
        """
        dwarf = get_object_or_404(Dwarf, pk=pk)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        url = request.build_absolute_uri(reverse('dwarf_detail', kwargs={'pk': dwarf.pk}))
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        response = BytesIO()
        img.save(response, "PNG")
        response.seek(0)
        img_base64 = base64.b64encode(response.read()).decode('utf-8')
        return Response({'qr_code': img_base64})


class VerifyQRCodeView(APIView):
    """
    Widok weryfikacji kodu QR.

    POST:
    Weryfikuje kod QR przesłany w żądaniu.
    Wymaga uwierzytelnienia.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Weryfikacja kodu QR.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'qr_code': openapi.Schema(type=openapi.TYPE_STRING, description='Kod QR')
            }
        ),
        responses={
            200: openapi.Response(description="Weryfikacja udana.", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Czy weryfikacja była udana'),
                    'url': openapi.Schema(type=openapi.TYPE_STRING, description='URL do szczegółów krasnoludka'),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Komunikat')
                }
            )),
            400: "Nieprawidłowy kod QR.",
            401: "Nieautoryzowany."
        },
    )
    def post(self, request):
        """
        Metoda obsługująca żądanie POST.

        Próbuje zweryfikować kod QR przesłany w żądaniu.
        Jeżeli kod QR jest prawidłowy i prowadzi do krasnoludka, który nie został jeszcze odblokowany przez zalogowanego użytkownika, odblokowuje krasnoludka i zwraca odpowiedź z informacją o sukcesie oraz URL do szczegółów krasnoludka.
        Jeżeli kod QR jest prawidłowy, ale prowadzi do krasnoludka, który został już odblokowany przez zalogowanego użytkownika, zwraca odpowiedź z informacją o niepowodzeniu oraz URL do szczegółów krasnoludka.
        Jeżeli kod QR jest nieprawidłowy, zwraca odpowiedź z informacją o niepowodzeniu.
        """
        data = request.data
        qr_code = data.get('qr_code')
        try:
            dwarf = Dwarf.objects.get(pk=qr_code.split('/')[-2])
            user_dwarf, created = UserDwarf.objects.get_or_create(user=request.user, dwarf=dwarf)
            if created:
                check_and_assign_dwarf_achievements(request.user)
                return Response({'success': True, 'url': reverse('dwarf_detail', args=[dwarf.id])},
                                status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'message': 'Ten krasnal został już odblokowany.',
                                 'url': reverse('dwarf_detail', args=[dwarf.id])}, status=status.HTTP_200_OK)
        except Dwarf.DoesNotExist:
            return Response({'success': False, 'message': 'Nieprawidłowy kod QR.'}, status=status.HTTP_400_BAD_REQUEST)


class UserRankingView(generics.ListAPIView):
    """
    Widok rankingu użytkowników.

    GET:
    Zwraca listę użytkowników posortowaną według podanego kryterium sortowania.
    Domyślnym kryterium sortowania jest liczba zdobytych krasnoludków.
    Możliwe kryteria sortowania to: 'num_dwarfs' (liczba zdobytych krasnoludków) i 'num_comments' (liczba dodanych komentarzy).
    """

    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Pobranie rankingu użytkowników.",
        responses={
            200: openapi.Response(description="Ranking użytkowników.", schema=UserSerializer(many=True)),
        },
    )
    def get_queryset(self):
        """
        Metoda zwracająca listę użytkowników do wyświetlenia.

        Ta metoda jest wywoływana, gdy do serwera wysłane jest żądanie GET.
        Zwraca listę użytkowników posortowaną według podanego kryterium sortowania.
        Domyślnym kryterium sortowania jest liczba zdobytych krasnoludków.
        Możliwe kryteria sortowania to: 'num_dwarfs' (liczba zdobytych krasnoludków) i 'num_comments' (liczba dodanych komentarzy).
        """
        sort_by = self.request.query_params.get('sort_by', 'num_dwarfs')
        if sort_by == 'num_dwarfs':
            return User.objects.annotate(num_dwarfs=Count('userdwarf')).order_by('-num_dwarfs')
        elif sort_by == 'num_comments':
            return User.objects.annotate(num_comments=Count('comment')).order_by('-num_comments')
        else:
            return User.objects.all()


class UserCommentsView(generics.ListAPIView):
    """
    Widok listy komentarzy użytkownika.

    GET:
    Zwraca listę komentarzy dodanych przez zalogowanego użytkownika.
    Wymaga uwierzytelnienia.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Pobranie listy komentarzy zalogowanego użytkownika.",
        responses={
            200: openapi.Response(description="Lista komentarzy użytkownika.", schema=CommentSerializer(many=True)),
            401: "Nieautoryzowany."
        },
    )
    def get_queryset(self):
        """
        Metoda zwracająca listę komentarzy do wyświetlenia.

        Ta metoda jest wywoływana, gdy do serwera wysłane jest żądanie GET.
        Zwraca listę komentarzy dodanych przez zalogowanego użytkownika.
        """
        return Comment.objects.filter(user=self.request.user)


class UserAchievementsView(generics.ListAPIView):
    """
    Widok listy osiągnięć użytkownika.

    GET:
    Zwraca listę osiągnięć zdobytych przez zalogowanego użytkownika.
    Wymaga uwierzytelnienia.
    """

    serializer_class = UserAchievementSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Pobranie listy osiągnięć zalogowanego użytkownika.",
        responses={
            200: openapi.Response(description="Lista osiągnięć użytkownika.", schema=UserAchievementSerializer(many=True)),
            401: "Nieautoryzowany."
        },
    )
    def get_queryset(self):
        """
        Metoda zwracająca listę osiągnięć do wyświetlenia.

        Ta metoda jest wywoływana, gdy do serwera wysłane jest żądanie GET.
        Zwraca listę osiągnięć zdobytych przez zalogowanego użytkownika.
        """
        return UserAchievement.objects.filter(user=self.request.user)


class AchievementsToGainView(generics.ListAPIView):
    """
    Widok listy osiągnięć do zdobycia przez użytkownika.

    GET:
    Zwraca listę osiągnięć, które zalogowany użytkownik może jeszcze zdobyć.
    Wymaga uwierzytelnienia.
    """

    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Pobranie listy osiągnięć do zdobycia przez zalogowanego użytkownika.",
        responses={
            200: openapi.Response(description="Lista osiągnięć do zdobycia.", schema=AchievementSerializer(many=True)),
            401: "Nieautoryzowany."
        },
    )
    def get_queryset(self):
        """
        Metoda zwracająca listę osiągnięć do wyświetlenia.

        Ta metoda jest wywoływana, gdy do serwera wysłane jest żądanie GET.
        Zwraca listę osiągnięć, które zalogowany użytkownik może jeszcze zdobyć.
        """
        user_achievements = UserAchievement.objects.filter(user=self.request.user)
        return Achievement.objects.exclude(id__in=user_achievements.values_list('achievement_id', flat=True))
