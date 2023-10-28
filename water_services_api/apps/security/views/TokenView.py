from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status

from water_services_api.apps.security.Auth import Auth


class TokenViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[],
            url_path='access', url_name='access')
    def access(self, request, format=None):
        data = request.data
        autenticado = False
        user_id = None
        idform = None
        message = ''
        user = User.objects.filter(email=data['username']).values('id').first()
        if user:
            user_id = user['id']
        else:
            user = User.objects.filter(username=data['username']).values('id').first()
            if user:
                user_id = user['id']
            else:
                idform = 'username'
                message = 'Usuario o correo electrónico inválido'

        if user_id:
            us = User.objects.get(pk=user_id)
            is_correct = us.check_password(data['password'])
            if is_correct:
                autenticado = True
                token = Auth.create_token(us.person_id)['token']
                resul = dict(
                    id='correcto',
                    estado=True,
                    message='Autenticado correctamente, bienvenido',
                    access_token=token
                )

                return Response(resul)
            else:
                idform = 'password'
                message = 'Contraseña inválida'

        if autenticado is False:
            resul = dict(
                error='invalid_grant',
                error_description=message,
                idform=idform
            )
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
