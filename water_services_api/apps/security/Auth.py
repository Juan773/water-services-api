import datetime
from django.utils import timezone
from oauth2_provider.models import get_access_token_model, get_refresh_token_model
from django.contrib.auth.models import  User

AccessToken = get_access_token_model()
RefreshToken = get_refresh_token_model()
from uuid import uuid4


class Auth():

    def is_user(person_id):
        user = User.objects.filter(person_id=person_id).values('id').first()
        if user:
            return True
        else:
            return False

    def create_token(person_id):
        user = User.objects.filter(person_id=person_id).values('id').first()

        if user:
            user_id = user['id']
            token = str(uuid4()) + '-dinam-acces-webs-' + str(uuid4())
            application_id = 1

            horas = 24 * 7

            data_actok = dict(
                user_id=user_id,
                scope='read write groups',
                expires=timezone.now() + datetime.timedelta(hours=horas),
                application_id=application_id,
                token=token,
            )

            acc_token = AccessToken.objects.create(**data_actok)

            if acc_token:
                data_rtoken = dict(
                    user_id=user_id,
                    token=token,
                    application_id=application_id,
                    access_token_id=acc_token.id
                )
                reftoken = RefreshToken.objects.create(**data_rtoken)
                resul = dict(
                    token=token,
                    estado=True
                )
                return resul
        else:
            resul = dict(
                estado=False,
                mensaje='La persona no tiene usuario registrado'
            )
            return resul

    def get_persona(email, activar):
        resul = dict(estado=False)
        fil_email = dict(
            contact_type__code='COR',
            value__exact=email,
        )
        # corr = PersonContact.objects.filter(**fil_email).values('id', 'person_id', 'person__full_name').first()
        # if corr:
        #     resul = {**corr}
        #     resul['estado'] = True
        return resul

    def get_email(person_id):
        resul = ''
        fil_correo = dict(
            contact_type__code='COR',
            person_id=person_id
        )
        # corr = PersonContact.objects.filter(**fil_correo).values('value').first()
        # if corr:
        #     resul = corr['value']
        return resul
