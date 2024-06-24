from django.urls import path
from .views import RegisterUser, UserLogin, UserLogout, UserDetail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('user/<str:username>/', UserDetail.as_view(), name='user-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)