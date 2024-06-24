from rest_framework import serializers
from ..models import *
from django.contrib.auth.password_validation import validate_password


class ChildSerializer(serializers.ModelSerializer):
    is_adopted = serializers.SerializerMethodField()
    img_url = serializers.SerializerMethodField()
    base_url = 'https://res.cloudinary.com/dx6s6ebfb/'

    class Meta:
        model = Child
        fields = '__all__'

    def get_is_adopted(self, obj):
        return obj.is_adopted
    def get_img_url(self,obj):
        return f"{self.base_url}{obj.photo}"
    

class ChildSerializer_2(serializers.ModelSerializer):
   
    class Meta:
        model = Child
        exclude = ('is_adopted',)
  
    


class AdoptionRequestSerializer(serializers.ModelSerializer):
    child = ChildSerializer_2
    class Meta:
        model = AdoptionRequest
        exclude = ('status' , 'approved_date' , 'rejected_date')

    def validate(self, data):
        child = data.get('child')
        if child.is_adopted:
            raise serializers.ValidationError('This child has already been adopted and cannot be adopted again.')
        if self.instance:
            if self.instance.status == 'approved' and data.get('status') == 'approved':
                raise serializers.ValidationError('This adoption request has already been approved.')
            if self.instance.status == 'rejected' and data.get('status') == 'rejected':
                raise serializers.ValidationError('This adoption request has already been rejected.')
        return data
class AdoptionRequestSerializer2(serializers.ModelSerializer):
    class Meta:
        model = AdoptionRequest
        exclude = ( 'approved_date' , 'rejected_date')

    def validate(self, data):
        child = data.get('child')
        if child.is_adopted:
            raise serializers.ValidationError('This child has already been adopted and cannot be adopted again.')
        if self.instance:
            if self.instance.status == 'approved' and data.get('status') == 'approved':
                raise serializers.ValidationError('This adoption request has already been approved.')
            if self.instance.status == 'rejected' and data.get('status') == 'rejected':
                raise serializers.ValidationError('This adoption request has already been rejected.')
        return data
    def to_representation(self, instance):
        rep = super(AdoptionRequestSerializer2, self).to_representation(instance)
        rep['child'] = instance.child.name
        return rep


class RegisterStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'email' , 'first_name' , 'last_name' , 'password' , 'password2']
    
    def validated_status(self, validated_data):
        if validated_data['Status'] == 'Admin':
            user = User.objects.create_superuser(validated_data['Status'],
                                                 validated_data['username'],  validated_data['email'],
                                                 validated_data['password'], validated_data['first_name'], validated_data['last_name'] )
        elif validated_data['Status'] == 'Staff':
            user = User.objects.create_staffuser(
                validated_data['Status'], validated_data['username'], validated_data[
                    'email'],
                validated_data['password'], validated_data['first_name'], validated_data['last_name'])
        return user
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs


    def create(self, validated_data):
        user = self.validated_status(validated_data)
        user.save()
        return user
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'Status',  'username',  'email', 'first_name', 'last_name']

