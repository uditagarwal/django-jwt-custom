from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
import django.contrib.auth.password_validation as validators
from django.core import exceptions


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 16
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=16,
        min_length=8,
        write_only=True
    )
    email = serializers.CharField(
        write_only=True
    )
    name = serializers.CharField(
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    jwt = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'password', 'name', 'jwt', 'refresh_token']

    def validate_password(self, password):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return password

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    jwt = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)
        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(email=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
                'refresh_token': user.refresh_token,
                'jwt': user.jwt
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    class Meta:
        model = User
        fields = ('email', 'name', "avatar")
        read_only_fields = ('token',)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)

    def validate(self, data):
        refresh_token = data.get('refresh_token', None)

        if refresh_token is None:
            raise serializers.ValidationError(
                'A Refresh Token is required in this Request'
            )

        # get user by the refresh token and save him again so
        # the refresh token gets regenerated, that way
        # all the prior Auth Tokens arent valid until
        # the user logs back in again
        try:
            user = User.objects.get(refresh_token=refresh_token)
            user.save()
        except:
            raise serializers.ValidationError(
                'The Entered Refresh Token is Incorrect'
            )

        return {}


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255, write_only=True)
    jwt = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        refresh_token = data.get('refresh_token', None)

        if refresh_token is None:
            raise serializers.ValidationError(
                'A Refresh Token is required in this Request'
            )

        # get user by the refresh token
        try:
            user = User.objects.get(refresh_token=refresh_token)
            user.save()
        except:
            raise serializers.ValidationError(
                'The Entered Refresh Token is Incorrect'
            )

        return {
            'jwt': user.jwt
        }

