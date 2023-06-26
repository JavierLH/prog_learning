from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    #envia la contraseña encriptada al crear un nuevo usuario
    def create(self, validated_data):
        create_user = User(**validated_data)
        create_user.set_password(validated_data['password'])
        create_user.save()
        return create_user
    
    #envia la contraseña encriptada al actualizar un nuevo usuario
    def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user
    
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('username','email','name','last_name')
