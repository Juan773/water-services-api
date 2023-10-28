from rest_framework.exceptions import APIException


class ExistDocumentException(APIException):
    status_code = 403
    default_detail = "No tiene permisos para realizar dicha accion"


class NumberDecimalFormatException(Exception):
    """The django.apps registry is not populated yet"""
    pass


class ErrorNumberConvertDecimal(APIException):
    status_code = 403
    default_detail = "Error al convertir de string a decimal"


class ErrorQuantityTotalDispatch(APIException):
    status_code = 403
    default_detail = "Las cantidades asignadas al personal supera lo indicado en el item"


class InternalOrderHasDispatched(APIException):
    status_code = 403
    default_detail = "El pedido interno ya ha sido despachado. No se puede hacer modificacion al despacho."


class SaleOrderHasDispatched(APIException):
    status_code = 403
    default_detail = "La venta interna ya ha sido despachado. No se puede hacer modificacion al despacho."


class InternalOrderNotMutable(APIException):
    status_code = 403
    default_detail = "El pedido interno ya ha sido aprobado o rechazado. No se puede modificar el registro."


class UserDoesNotStaff(APIException):
    status_code = 403
    default_detail = "El usuario que realiza esta operación no es personal. Asegúrese se configurarlo"
