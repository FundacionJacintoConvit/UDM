# coding: utf-8

import inspect
import time
from requests.models import Response

from django.conf import settings
from django.http import HttpRequest
from rest_framework.request import Request

from commons.convit.logs import ConvitLevel, obj_a_params
from commons.convit.exceptions import SeguridadException, manejar_excepcion
from commons.convit.views import custom_web_exception_handler, custom_rest_exception_handler

class ConvitLoggerExceptionDecorator(object):
    """
    Clase decoradora de Arquitectura Convit que maneja las excepciones y las trazas.
    """
    
    def __init__(self, origen=None, destino=None, tipo_transaccion=None, transaccion_id=None, metodo=None, login_requerido=False, permisos=None, logger=None):
        """
        Constructor de decorador que maneja las trazas y genera las excepciones.
        
        Args:
            origen: El origen.
            destino: El destino.
            tipo_transaccion: El tipo de transacción.
            transaccion_id: El identificador de transacciones.
            metodo: El método.
            login_requerido: Si el método se ejecuta sólo si el usuario está requerido, sino dispara una excepción SeguridadException.
            permisos: Si el método se ejecuta sólo si el usuario tiene los permisos, sino dispara una excepción SeguridadException.
            logger: El objeto logger.
        """
        
        self.origen = origen
        self.destino = destino
        self.tipo_transaccion = tipo_transaccion
        self.transaccion_id = transaccion_id
        self.metodo = metodo
        self.login_requerido = login_requerido
        self.permisos = permisos
        self.logger = logger
        
    def __call__(self, funcion):
        """
        La invocación a la función.
        
        Args:
            funcion: La función.
            
        Returns:
            La función wrapper que agrega funcionalidad a la función original.
            
        Raises:
            SeguridadException: La excepción de seguridad si no se cumple que el usuario sea requerido o tenga los permisos.
        """
        
        args_spec = inspect.getargspec(funcion)
        
        def wrapper(*args, **kwargs):
            """
            La función wrapper que agrega funcionalidad a la función original.
            
            Returns:
                El resultado de la función original.
                
            Raises:
                MantenimientoException: La excepción de mantenimiento.
            """
            
            try:
                request = None
                procesado = False
                clase = None
                kwargs_extra = dict(kwargs)
                
                if args_spec.defaults:
                    params = dict(zip(args_spec.args, args + args_spec.defaults[len(args):]))
                else:
                    params = dict(zip(args_spec.args, args))
                    
                if params.has_key('self'):
                    if self.metodo:
                        kwargs_extra['metodo'] = self.metodo
                    else:
                        clase = args[0].__class__.__name__
                        kwargs_extra['metodo'] = args[0].__class__.__module__ + '.' + clase + '.' + funcion.__name__
                    
                    del params['self']
                else:
                    if self.metodo:
                        kwargs_extra['metodo'] = self.metodo
                    else:
                        kwargs_extra['metodo'] = funcion.__module__ + '.' + funcion.__name__
                
                if params.has_key('request') and isinstance(params['request'], (HttpRequest, Request)):
                    request = params['request']
                    if 'transaccionId' in request.GET:
                        kwargs_extra['transaccionId'] = request.GET.get('transaccionId')
                    if 'origen' in request.GET:
                        kwargs_extra['origen'] = request.GET.get('origen')
                    
                    params.update(dict(request.GET))
                    
                    del params['request']
                
                params.update(kwargs_extra)
                for param in [ 'request_id', 'usuario', 'transaccionId', 'origen', 'destino', 'tipo_transaccion', 'aplicacion', 'metodo', 'codigo', 'param_entrada', 'mensaje', 'plataforma', 'tiempo', 'ex', 'GET', 'POST', 'COOKIES', 'META' ]:
                    if param in params:
                        del params[param]
                        
                kwargs_extra['aplicacion'] = settings.APLICACION
                kwargs_extra['param_entrada'] = obj_a_params(params)
                if self.tipo_transaccion:
                    kwargs_extra['tipo_transaccion'] = self.tipo_transaccion
                if self.origen:
                    kwargs_extra['origen'] = self.origen
                if self.destino:
                    kwargs_extra['destino'] = self.destino
                if self.transaccion_id:
                    kwargs_extra['transaccionId'] = self.transaccion_id
                    
                if request:
                    if self.permisos and not isinstance(self.permisos, (list, tuple)):
                        self.permisos = ( self.permisos, )
                    
                    if self.login_requerido and not request.user.is_authenticated():
                        kwargs_extra['codigo'] = 'SEG-001'
                        kwargs_extra['mensaje'] = 'Se requiere un usuario autenticado para acceder al recurso ' + request.path
                        raise SeguridadException(**kwargs_extra)
                    if self.permisos and not request.user.has_perms(self.permisos):
                        kwargs_extra['codigo'] = 'SEG-002'
                        kwargs_extra['mensaje'] = 'El usuario ' + request.user.username + ' no tiene los permisos ' + str(self.permisos) + ' para acceder al recurso ' + request.path
                        raise SeguridadException(**kwargs_extra)
                        
                tiempo = time.clock()
                
                if clase and (clase.endswith('View') or clase.endswith('Service') or clase.endswith('Manage')):
                    resultado = funcion(*args, **kwargs_extra)
                else:
                    resultado = funcion(*args, **kwargs)
                    
                if isinstance(resultado, Response) and resultado.status_code != 200:
                    ex = manejar_excepcion(resultado, self.logger, **kwargs_extra)
                    procesado = True
                    raise ex
                    
                kwargs_extra['tiempo'] = time.clock() - tiempo
                if self.logger:
                    self.logger.log(ConvitLevel.INFO, '', extra=kwargs_extra)
                
                return resultado
            except Exception as ex:
                if not procesado:
                    ex = manejar_excepcion(ex, self.logger, **kwargs_extra)

                if request:
                    if isinstance(request, Request):
                        return custom_rest_exception_handler(ex)
                    elif isinstance(request, HttpRequest):
                        return custom_web_exception_handler(ex)
                else:
                    raise ex

        return wrapper