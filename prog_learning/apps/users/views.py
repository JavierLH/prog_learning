from datetime import datetime
from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from apps.users.api.serializer import UserTokenSerializer
from rest_framework.views import APIView
class Login (ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data,context={'request':request})
        if login_serializer.is_valid():
            user=login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({
                            'token':token.key,
                            'user':user_serializer.data,
                            'message':'Exito al iniciar sesión'
                            },status=status.HTTP_200_OK)
                else:
                    token.delete()
                    token = Token.objects.create(user =user)
                    return Response({
                            'token':token.key,
                            'user':user_serializer.data,
                            'message':'Exito al iniciar sesión'
                            },status=status.HTTP_200_OK)

            else:
                return Response({'error':'El usuario esta inactivo,fallo al iniciar sesión'},status=status.HTTP_401_UNAUTHORIZED)
        else:    
            return Response({'error':'Nombre o contraseña incorrectos'},status=status.HTTP_400_BAD_REQUEST)
    

class Logout(APIView):
    def get(self, request, *args, **kwargs):   
        token = request.GET.get('token')
        print(token)
        token =Token.objects.filter(key=token).first()
        if token:
            user = token.user
            all_sesion= Session.objects.filter(expire_date__gte=datetime.now())
            if all_sesion.exists():
                for session in all_sesion:
                    session_data = session.get_decoded()
                    if user.id == int (session_data.get('_auth_user_id')):
                        session.delete()
            token.delete()
            session_message = 'sesiones de usuario eliminadas'
            token_message = 'token eliminado'
            return Response({'token_message':token_message,'session_message':session_message},status=status.HTTP_200_OK)
        return Response({'error':'No se ha encontrado un usuario asociado con estas credenciales'},status=status.HTTP_400_BAD_REQUEST)
        






