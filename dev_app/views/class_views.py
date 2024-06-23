from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from dev_app.models import User
from dev_app.serializers import ChangePasswordSerializer, RegisterStaffSerializer, UserSerializer, ChildSerializer, AdoptionRequestSerializer ,AdoptionRequestSerializer2
from rest_framework import generics , viewsets , status , filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from dev_app.models import Child, AdoptionRequest
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from dev_app.filters import AdoptionRequestFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['status'] = user.Status
        token['username'] = user.username
        token['email'] = user.email
        token['first_name']= user.first_name
        token["last_name"]= user.last_name
        

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Takes the username an password an returns access an refresh tokens
    These can be used for user authentication 
    """
    serializer_class = MyTokenObtainPairSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    Used for users to change passwords based on their old password
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated)
    serializer_class = ChangePasswordSerializer


class UserList(generics.ListAPIView):
    """List all users this is only available for an admin user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    
class RegisterUser(generics.CreateAPIView):
    """This can be used to register new users on the app"""
    queryset = User.objects.all()
    serializer_class = RegisterStaffSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """ View , update and delete a specific user's detail"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]





class ChildViewSet(viewsets.ModelViewSet):
    
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['get'])
    def adopted(self, request):
        adopted_children = Child.objects.filter(adoptionrequest__status='approved').distinct()
        serializer = self.get_serializer(adopted_children, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unadopted(self, request):
        unadopted_children = Child.objects.exclude(adoptionrequest__status='approved').distinct()
        serializer = self.get_serializer(unadopted_children, many=True)
        return Response(serializer.data)
    


class AdoptionRequestViewSet(viewsets.ModelViewSet):
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptionRequestSerializer
    permission_classes = [IsAuthenticated,]
    # filter_backends = (DjangoFilterBackend)
    # filter_class = AdoptionRequestFilter
    # ordering_fields = ['status', 'created_at']
    # ordering = ['status']
    http_method_names = ['post', 'head', 'put']

    def update(self, request, *args, **kwargs):
        adoption_request = self.get_object()
        status = request.data.get('status')

        if status == 'approved':
            adoption_request.status = 'approved'
            adoption_request.approved_date = timezone.now()
        elif status == 'rejected':
            adoption_request.status = 'rejected'
            adoption_request.rejected_date = timezone.now()

        adoption_request.save()

        return Response({'status': f'Adoption request {status}'}, status=status.HTTP_200_OK)
   
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def request_adoption(self, request, pk=None):
        user = request.user
        child = Child.objects.get(pk=pk)

        # Check if the child is already adopted
        if child.is_adopted:
            return Response({'status': 'child is already adopted'}, status=status.HTTP_400_BAD_REQUEST)

        if AdoptionRequest.objects.filter(user=user, child=child).exists():
            return Response({'status': 'adoption request already exists'}, status=status.HTTP_400_BAD_REQUEST)

        adoption_request = AdoptionRequest.objects.create(user=user, child=child, status='pending')
        serializer = AdoptionRequestSerializer(adoption_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        adoption_request = self.get_object()
        if adoption_request.status == 'approved':
            return Response({'status': 'adoption request already approved'}, status=status.HTTP_400_BAD_REQUEST)

        adoption_request.status = 'approved'
        adoption_request.save()
        return Response({'status': 'adoption request approved'}, status=status.HTTP_200_OK)
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        adoption_request = self.get_object()
        if adoption_request.status != 'pending':
            return Response({'status': 'adoption request is not pending and cannot be rejected again'}, status=status.HTTP_400_BAD_REQUEST)

        if adoption_request.status == 'rejected':
            return Response({'status': 'adoption request already rejected'}, status=status.HTTP_400_BAD_REQUEST)

        adoption_request.status = 'rejected'
        adoption_request.save()
        return Response({'status': 'adoption request rejected'}, status=status.HTTP_200_OK)
    
class AdoptionRequestListView(generics.ListAPIView):
    """
    Lists Adoption Requests for users
    And view all Adoption Requests for admin users
    """
    serializer_class = AdoptionRequestSerializer2
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdoptionRequestFilter
    ordering_fields = ['status', 'created_at']
    ordering = ['status']
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return AdoptionRequest.objects.all()  # Admin can see all requests
        return AdoptionRequest.objects.filter(user=user)  # Normal users see only their own requests