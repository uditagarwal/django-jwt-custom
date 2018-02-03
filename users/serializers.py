from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate



class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # TODO: Add minimum password requirements
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

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


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

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # Calling save on the model because it generates a new refresh token
        # throws an error if the user is already logged in
        if not user.refresh_token:
            user.refresh_token = user._generate_refresh_token()
            user.save()

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

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is that
        # we don't need to specify anything else about the field. The
        # password field needed the `min_length` and 
        # `max_length` properties, but that isn't the case for the token
        # field.
        read_only_fields = ('token',)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)

    def validate(self, data):
        refresh_token = data.get('refresh_token', None)

        if refresh_token is None:
            raise serializers.ValidationError(
                'A Refresh Token is required in this Request'
            )

        # get user by the refresh token
        try:
            user = User.objects.get(refresh_token=refresh_token)
            user.refresh_token = None
            user.save()
        except:
            raise serializers.ValidationError(
                'The Entered Refresh Token is Incorrect'
            )

        return {}
