import jwt
from django.http import JsonResponse
from django.contrib.auth.models import User

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before the view

        # print(request.headers.get)
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            print(jwt_token)
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                print('Token is invalid')
                return JsonResponse({'message': 'Token is invalid'}, status=400)

            request.user = User.objects.get(id=payload['user_id'])

        response = self.get_response(request)

        return response