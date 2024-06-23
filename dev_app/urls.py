
from django.urls import path ,include

from rest_framework_simplejwt.views import (TokenRefreshView)
from .views import (
    MyTokenObtainPairView, ChangePasswordView , RegisterUser, UserList, UserDetail)
from rest_framework import routers

from dev_app import views
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from .views import ChildViewSet, AdoptionRequestViewSet , AdoptionRequestListView
from .views import send_test_email

router = DefaultRouter()



router.register(r'children', ChildViewSet , basename='Child')
router.register(r'adoptions', AdoptionRequestViewSet , basename='AdoptionRequest')

schema_view = get_schema_view(
   openapi.Info(
      title="Adoption App API",
      default_version='v1',
      description="API documentation for the Adoption App",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="contact@yourapp.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('', include(router.urls)),
    path('authtoken/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('users/', UserList.as_view() , name='user_list_view'),
    path('users/<int:pk>', UserDetail.as_view()),
    path('changepassword/<int:pk>',
         ChangePasswordView.as_view(), name='change_password'),
    path('docs/', include_docs_urls(title='My API Docs')),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('adoptions/<int:pk>/approve/', AdoptionRequestViewSet.as_view({'post': 'approve'}), name='adoption-approve'),
    # path('adoptions/<int:pk>/reject/', AdoptionRequestViewSet.as_view({'post': 'reject'}), name='adoption-reject'),
     path('children/adopted/', ChildViewSet.as_view({'get': 'adopted'}), name='adopted-children'),
    path('children/unadopted/', ChildViewSet.as_view({'get': 'unadopted'}), name='unadopted-children'),
     path('send-test-email/', send_test_email),
      path('adoption-requests/', AdoptionRequestListView.as_view(), name='adoption_request_list'),

]