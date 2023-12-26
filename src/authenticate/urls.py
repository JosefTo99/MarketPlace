from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, TestingAuthenticatedReq
# from . import views

urlpatterns=[
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestingAuthenticatedReq.as_view(), name='granted'),  # Authorization Bearer 'token'
    # path('login/', LoginUserView.as_view(), name='login'),
    # path('test-token/', views.test_token, name='test-token'),
]