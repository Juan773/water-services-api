from django.contrib.auth.models import Permission, Group, ContentType


class Permissions():

    def accession(request, models):
        data = {}
        user = request.user
        user_id = user.id

        list_models = []
        for p in models:
            split = p.strip().split(".")

            if len(split) == 2:
                app_label = split[0]
                model = split[1]
                cont_type = ContentType.objects.filter(
                    app_label=app_label, model=model).values('id', 'app_label', 'model').first()
                if cont_type:
                    list_models.append(cont_type)

        is_superuser = user.is_superuser
        for p in list_models:

            if is_superuser:
                permissions_upxe = Permission.objects.filter(
                    content_type=p['id'],
                ).values('codename')
            else:
                permissions_upxe = Permission.objects.filter(
                    content_type=p['id'],
                    user__exact=user_id
                ).values('codename')

            for q in permissions_upxe:
                data[p['app_label'] + '.' + p['model'] + "." +
                     q['codename'].replace('_' + p['model'], '')] = True

        # models por grupos
        if is_superuser is False:
            for p in list_models:

                permissions_groups = Group.objects.filter(
                    user__exact=user_id,
                    permissions__content_type=p['id'],
                ).values('permissions__codename')

                for q in permissions_groups:
                    data[p['app_label'] + '.' + p['model'] + "." +
                         q['permissions__codename'].replace('_' + p['model'], '')] = True

        return data
