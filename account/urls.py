from django.urls import path
from .views import RegisterViewSet, LoginViewSet, ProfileViewSet, ChangePasswordViewSet, LogoutViewSet

urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post': 'create'})),
    path('login/', LoginViewSet.as_view({'post': 'create'})),
    path('profile/', ProfileViewSet.as_view({'get': 'list', 'patch': 'partial_update'})),
    path('change-password/', ChangePasswordViewSet.as_view({'post': 'create'})),
    path('logout/', LogoutViewSet.as_view({'post': 'create'})),
]