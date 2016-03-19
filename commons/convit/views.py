# coding: utf-8

from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from commons.convit.exceptions import AdvertenciaFuncionalException, MantenimientoException, PlataformaNoDisponibleException, SeguridadException

def custom_web_exception_handler(ex):
    """
    Manejador de excepciones para aplicaciones web.
    
    Args:
        ex: La excepción.
        
    Returns:
        El objeto HTTP Response.
    """

    if isinstance(ex, SeguridadException):
        return HttpResponseRedirect(settings.URL_PREFIX + '/logout')
    elif not settings.DEBUG:
        if isinstance(ex, PlataformaNoDisponibleException):
            return HttpResponseRedirect(settings.URL_PREFIX + '/plataforma_no_disponible')
        elif isinstance(ex, MantenimientoException):
            return HttpResponseRedirect(settings.URL_PREFIX + '/mantenimiento')
        else:
            return HttpResponseRedirect(settings.URL_PREFIX + '/error_operacional')

        return response
    else:
        raise ex
    
def custom_rest_exception_handler(ex):
    """
    Manejador de excepciones para servicios REST.
    
    Args:
        ex: La excepción.
        
    Returns:
        El objeto HTTP Response.
    """

    data = JSONRenderer().render(ex.__dict__)
    if isinstance(ex, PlataformaNoDisponibleException):
        response = Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    elif isinstance(ex, MantenimientoException):
        response = Response(data, status=423)
    elif isinstance(ex, SeguridadException):
        response = Response(data, status=status.HTTP_403_FORBIDDEN)
    elif isinstance(ex, AdvertenciaFuncionalException):
        response = Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response