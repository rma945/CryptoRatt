from django.urls import include, path
from apps.help.views import *

app_name = 'help'

urlpatterns = [
    # include(help.views),
    path('', home),
    path('<slug:page>/', markdown),
]
