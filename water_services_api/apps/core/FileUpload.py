from django.conf import settings
import os

from uuid import uuid4
from PIL import Image
import time

from water_services_api.apps.configuration.models import Person

folder_storage = "storage"


def get_or_create_folder(ruta):
    ruta = "%s/%s" % (settings.BASE_DIR, ruta)
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    return ruta


def save_file(ruta, nombre_file, up_file):
    url = "%s%s" % (ruta, nombre_file)
    destination = open(url, 'wb+')
    if up_file.multiple_chunks:
        for c in up_file.chunks():
            destination.write(c)
    else:
        destination.write(up_file.read())
    destination.close()
    return nombre_file


def recortar_img(up_file, size_x, size_y):
    image_obj = Image.open(up_file)
    rec_image = image_obj.resize((size_x, size_y), Image.ANTIALIAS)
    return rec_image


def save_recortado(rec_image, ruta, nombre_file):
    url = "%s%s" % (ruta, nombre_file)
    destination = open(url, 'wb+')
    rec_image.save(destination)
    return nombre_file


def save_file_txt(ruta, nombre_file, up_file):
    url = "%s%s" % (ruta, nombre_file)
    destination = open(url, 'wb+')
    if up_file.multiple_chunks:
        for c in up_file.chunks():
            destination.write(c)
    else:
        destination.write(up_file.read())
    destination.close()
    return nombre_file


def util_save_img(column, up_file, dir_storage):
    name_uui = str(uuid4()).replace('-', '')
    dir_complete = "%s/%s" % (folder_storage, dir_storage)
    ruta = get_or_create_folder(dir_complete)
    nombre_file = name_uui + os.path.splitext(up_file.name)[1]
    if column == 'logo':
        return "%s%s" % (dir_storage, save_file(ruta, nombre_file, up_file))

    if column == 'thumbnail':
        rec_image = recortar_img(up_file, 150, 150)
        return "%s%s" % (dir_storage, save_recortado(rec_image, ruta, nombre_file))


def get_info(file, extension):
    resul = dict(
        name=file.name,
        content_type=file.content_type,
        size=file.size,
        size_mb=round(int(file.size) / 1048576, 2),
        exten='',
        extension_id=None
    )

    split_name = file.name.split('.')
    if len(split_name) > 1:
        resul['exten'] = "%s%s" % (".", split_name[len(split_name) - 1])

    # if extension:
    #     from apps.files.models.Extension import Extension
    #     if resul['exten']:
    #         exis_ext = Extension.objects.filter(
    #             extension=resul['exten']
    #         ).values('id').first()
    #         if exis_ext:
    #             resul['extension_id'] = exis_ext['id']

    return resul


class FileUpload():

    def configuration_person(column, up_file):
        dir_storage = "%s%s" % (Person.dir_storage, '/')
        return util_save_img(column, up_file, dir_storage)

    def valida_extension(extensiones, up_file):
        extension = os.path.splitext(up_file.name)[1].replace('.', '').lower()
        if extension in extensiones:
            return True
        else:
            raise Exception('La extension %s no esta permitida' % (extension))

    def delete_file(ruta_file):
        ruta = "%s/%s/%s" % (settings.BASE_DIR, folder_storage, ruta_file)
        if os.path.exists(ruta):
            os.remove(ruta)
            return ""

    def files_recurso(up_file, nombre, folder):
        fecha_hora = str(time.strftime("%Y%m%d-")) + str(time.strftime("%H%M%S"))
        name_uui = "%s-%s" % (nombre, fecha_hora)
        if folder:
            folder += '/'
        ruta_file = ''  # Recurso.dir_storage_local + "/" + folder
        dir_complete = "%s/%s" % (folder_storage, ruta_file)
        ruta = get_or_create_folder(dir_complete)
        nombre_file = "%s%s" % (name_uui, os.path.splitext(up_file.name)[1])
        return "%s%s" % (ruta_file, save_file(ruta, nombre_file, up_file))


class Conversiones():
    """docstring for Conversiones"""

    def to_base64(url_file):
        import base64
        url = url = "%s/%s/%s" % (settings.BASE_DIR, folder_storage, url_file)

        split_url = url_file.split('.')

        with open(url, "rb") as img:
            thumb_string = base64.b64encode(img.read())

        if len(split_url) > 0 and split_url[len(split_url) - 1] == 'png':
            base64out = "%s%s" % ("data:image/png;base64,", str(thumb_string)[2:-1])
        # return(base64out)

        if len(split_url) > 0 and split_url[len(split_url) - 1] == 'jpg':
            base64out = "%s%s" % ("data:image/jpg;base64,", str(thumb_string)[2:-1])

        return base64out
