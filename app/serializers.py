from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    """
    Serializer do logowania użytkownika.

    Przyjmuje nazwę użytkownika i hasło, a następnie próbuje uwierzytelnić użytkownika.
    Jeżeli uwierzytelnienie jest udane, zwraca dane.
    Jeżeli uwierzytelnienie nie jest udane, zwraca błąd walidacji.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid username or password.')
            if not user.is_active:
                raise serializers.ValidationError('User is deactivated.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        return data
