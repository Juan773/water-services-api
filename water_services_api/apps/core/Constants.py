from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

SI_NO = (
    ('SI', capfirst(_('SI'))),
    ('NO', capfirst(_('NO'))),
)

TYPE_ENTRY = (
    ('I', 'Ingreso'),
    ('S', 'Salida'),
    ('T', 'Traspaso'),
)

STATUS_INTERNAL_ORDER = (
    ('P', 'Registrado'),
    ('A', 'Aprobado'),
    ('O', 'Observado'),
    ('R', 'Rechazado'),
)

TYPE_ORIGIN = (
    ('S', 'Venta'),
    ('P', 'Compra'),
    ('W', 'Almacen'),
    ('SO', 'Pedido de venta'),
    ('IO', 'Pedido interno'),
    ('RIO', 'Devolución de pedido interno'),
    ('CN', 'Nota Crédito'),
)

UNIT_DEFAULT = 1
