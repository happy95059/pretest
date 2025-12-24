from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class APIKeyAuthentication(BaseAuthentication):
    """
    API Key 驗證
    Token 從環境變數讀取,不寫死在程式碼中
    """
    def authenticate(self, request):
        # 從 X-API-Key header 取得
        api_key = request.headers.get('X-API-Key')
        
        # 如果完全沒有提供 token
        if not api_key:
            raise AuthenticationFailed('API Key is required')
        
        # 驗證 token (從 settings 讀取)
        if api_key != settings.API_TOKEN:
            raise AuthenticationFailed('Invalid API Key')
        
        # 驗證成功: 回傳 (user, auth)
        return (None, api_key)
    
    def authenticate_header(self, request):
        return 'X-API-Key realm="API"'
