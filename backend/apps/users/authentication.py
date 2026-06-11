import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions

User = get_user_model()

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
            
        token = parts[1]
        
        # Verify token by sending it to Supabase Auth API
        supabase_url = getattr(settings, 'SUPABASE_URL', None)
        supabase_key = getattr(settings, 'SUPABASE_KEY', None)
        
        if not supabase_url or not supabase_key:
            raise exceptions.AuthenticationFailed('Supabase configuration is missing in settings')
            
        headers = {
            'Authorization': f'Bearer {token}',
            'apikey': supabase_key
        }
        
        try:
            response = requests.get(f"{supabase_url}/auth/v1/user", headers=headers, timeout=5)
            if response.status_code != 200:
                raise exceptions.AuthenticationFailed('Invalid token')
                
            user_data = response.json()
            user_id = user_data['id']
            email = user_data['email']
            is_admin = user_data.get('user_metadata', {}).get('is_admin', False)
            
            # Get or create the user in Django db matching this ID and email
            user, created = User.objects.get_or_create(
                id=user_id,
                defaults={
                    'email': email,
                    'name': user_data.get('user_metadata', {}).get('name', email),
                    'is_email_verified': user_data.get('email_confirmed_at') is not None,
                    'is_admin': is_admin,
                    'is_staff': is_admin
                }
            )
            
            # If user already exists, update their details
            if not created:
                user.email = email
                user.is_admin = is_admin
                user.is_staff = is_admin
                name = user_data.get('user_metadata', {}).get('name')
                if name:
                    user.name = name
                user.save()
                
            return (user, token)
            
        except requests.RequestException:
            raise exceptions.AuthenticationFailed('Supabase service unavailable')
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))
