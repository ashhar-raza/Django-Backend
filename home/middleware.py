import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from home.models import User
from django.http import JsonResponse

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path

        # Only protect /api/notes
        if not path.startswith('/api/notes'):
            return  # Skip for other APIs

        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Unauthorized - Missing token'}, status=401)

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['id'])
            request.user = user  # Attach user to request
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return JsonResponse({'error': 'Unauthorized - Invalid token'}, status=401)
