from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.db import models
from apps.account.models import UserSession
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

class SessionMiddleware(SessionMiddleware):
    def __init__(self, *args, **kwargs):
        super(SessionMiddleware, self).__init__(*args, **kwargs)
    
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(
            session_key=session_key,
            ip=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

class SessionStore(DBStore):
    """Custom user session storage with user_id, ip, user_agent"""

    def __init__(self, session_key=None, user_agent=None, ip=None):
        super(SessionStore, self).__init__(session_key)
        self.user_agent= user_agent
        self.ip = ip

    @classmethod
    def get_model_class(cls):
        return UserSession

    def create_model_instance(self, data):
        obj = super().create_model_instance(data)
        try:
            user_id = int(data.get('_auth_user_id'))
        except (ValueError, TypeError):
            user_id = None

        obj.user_id = user_id
        obj.ip = self.ip
        obj.user_agent = self.user_agent
    
        return obj