# coding: utf-8

import sys
import json

from rest_framework.parsers import JSONParser

from commons.convit.logs import ConvitLevel

class ConvitException(Exception):
    """
    Clase padre de todas las excepciones de Convit.
    """

    def __init__(self, **kwargs):
        """
        Es el constructor de la clase.
        """
        
        super(ConvitException, self).__init__()
        for k in [ 'request_id', 'usuario', 'transaccionId', 'origen', 'destino', 'tipo_transaccion', 'aplicacion', 'metodo', 'codigo', 'param_entrada', 'mensaje', 'plataforma', 'tiempo', 'ex' ]:
            setattr(self, k, kwargs.get(k, ''))
            
    def __str__(self):
        """
        Obtener un string de la excepción.
        
        Returns:
            El string de la excepción.
        """
        
        return self.mensaje
        
    def __repr__(self):
        """
        Obtener una representación de la excepción.
        
        Returns:
            La representación de la excepción.
        """
        
        return self.mensaje

class ErrorOperacionalException(ConvitException):
    """
    Es la clase que representa la excepción generada cuando ocurre un error que no permite que la aplicación continúe su ejecución. Ejemplos: Se llenó el disco, no hay memoria suficiente, etc.
    """
    pass

class PlataformaNoDisponibleException(ErrorOperacionalException):
    """
    Es la clase que representa la excepción generada cuando un recurso, del cual depende la aplicación, no se encuentra disponible. Ejemplo la base de datos está abajo, el web service está abajo.
    """
    pass

class AdvertenciaFuncionalException(ConvitException):
    """
    Clase que representa la excepción generada cuando no se cumple el flujo natural de la aplicación (Ej: Usuario y Password no válido, Serial inválido, El cliente ya existe).
    """
    pass

class MantenimientoException(AdvertenciaFuncionalException):
    """
    Es la clase que representa la excepción generada cuando una entidad accede a la aplicación y está se encuentra en modo de mantenimiento.
    """
    pass

class SeguridadException(AdvertenciaFuncionalException):
    """
    Es la clase que representa la excepción generada cuando una entidad trata de accede un recurso al cual no tiene permisos de acceder.
    """
    pass
        
def obtener_ultimo_tb(tb):
    """
    Obtener el último traceback que es el que tiene el origen de la excepción.
    
    Args:
        tb: Traceback.
        
    Returns:
        El traceback que contiene el origen de la excepción.
    """
    
    while tb.tb_next:
        tb = tb.tb_next
        
    return tb
    
def manejar_excepcion(ex, logger=None, **kwargs):
    """
    Convertir una excepción a una excepción de la jerarquía Convit.
    
    Args:
        ex: La excepción original.
        logger: El objeto logger para generar las trazas.
    
    Returns:
        La excepción de la jerarquía Convit.
    """
    
    if isinstance(ex, ConvitException):
        for arg in [ 'request_id', 'usuario', 'transaccionId', 'origen', 'destino', 'tipo_transaccion', 'aplicacion', 'metodo', 'codigo', 'param_entrada', 'mensaje', 'plataforma', 'tiempo' ]:
            if not hasattr(ex, arg) or not getattr(ex, arg):
                setattr(ex, arg, kwargs.get(arg, ''))        
    elif hasattr(ex, '__module__'):
        kwargs['ex'] = ex

        nombre = ex.__module__ + '.' + ex.__class__.__name__
        
        if nombre in [ 'django.db.utils.DatabaseError', 'django.db.utils.DataError', 'django.db.utils.IntegrityError', 'django.db.utils.InterfaceError', 'django.db.utils.InternalError', 'django.db.utils.NotSupportedError', 'django.db.utils.OperationalError', 'django.db.utils.ProgrammingError' ]:
            ex = ex.__cause__
            nombre = ex.__module__ + '.' + ex.__class__.__name__

        if nombre in [ 'psycopg2.DatabaseError', 'psycopg2.DataError', 'psycopg2.IntegrityError', 'psycopg2.InterfaceError', 'psycopg2.InternalError', 'psycopg2.NotSupportedError', 'psycopg2.OperationalError', 'psycopg2.ProgrammingError' ]:
            codigo = ex.pgcode
            mensaje = str(ex)
            kwargs['codigo'] = codigo
            kwargs['mensaje'] = mensaje
            if mensaje.startswith('could not connect to server') or mensaje.startswith('connection already closed'):
                ex = PlataformaNoDisponibleException(**kwargs)
            else:
                ex = ErrorOperacionalException(**kwargs)
        elif nombre in [ 'cx_Oracle.DatabaseError', 'cx_Oracle.DataError', 'cx_Oracle.IntegrityError', 'cx_Oracle.InterfaceError', 'cx_Oracle.InternalError', 'cx_Oracle.NotSupportedError', 'cx_Oracle.OperationalError', 'cx_Oracle.ProgrammingError' ]:
            mensaje = str(ex)
            if mensaje.find('ORA-') >= 0:
                mensaje = mensaje.split(':', 1)
                codigo = mensaje[0].strip()
                mensaje = mensaje[1].strip()
                kwargs['codigo'] = codigo
                kwargs['mensaje'] = mensaje
                if codigo.split('-')[1] in [ '1033', '1089', '12505', '12514', '12518', '12519', '12528', '12541', '17002' ]:
                    ex = PlataformaNoDisponibleException(**kwargs)
                else:
                    ex = ErrorOperacionalException(**kwargs)
            else:
                kwargs['codigo'] = ''
                kwargs['mensaje'] = mensaje[0].strip()
                ex = ErrorOperacionalException(**kwargs)
        elif nombre == 'urllib2.URLError':
            mensaje = str(ex).split('[', 1)[1]
            if len(mensaje) > 1:
                mensaje = mensaje.split(']', 1)
                codigo = mensaje[0].split(' ', 1)[1].strip()
                mensaje = mensaje[1].strip()
                kwargs['codigo'] = codigo
                kwargs['mensaje'] = mensaje
                if codigo == '10061':
                    ex = PlataformaNoDisponibleException(**kwargs)
                else:
                    ex = ErrorOperacionalException(**kwargs)
            else:
                kwargs['codigo'] = ''
                kwargs['mensaje'] = mensaje[0]
                ex = ErrorOperacionalException(**kwargs)
        elif nombre == 'urllib2.HTTPError':
            try:
                data = JSONParser().parse(ex)
                data = json.loads(data)
                kwargs.update(data)
                if ex.getcode() == 400:
                    ex = AdvertenciaFuncionalException(**kwargs)
                elif ex.getcode() == 403:
                    ex = SeguridadException(**kwargs)
                elif ex.getcode() == 423:
                    ex = MantenimientoException(**kwargs)
                elif ex.getcode() == 503:
                    ex = PlataformaNoDisponibleException(**kwargs)
                else:
                    ex = ErrorOperacionalException(**kwargs)
            except Exception as ex:
                codigo = 'MOV-0003'
                mensaje = 'Error Operacional'
                kwargs['codigo'] = codigo
                kwargs['mensaje'] = mensaje
                
                ex = ErrorOperacionalException(**kwargs)
        elif nombre == 'requests.models.Response':
            data = ex.json()
            data = json.loads(data)
            kwargs.update(data)
            if ex.status_code == 400:
                ex = AdvertenciaFuncionalException(**kwargs)
            elif ex.status_code == 503:
                ex = PlataformaNoDisponibleException(**kwargs)
            elif ex.status_code == 423:
                ex = MantenimientoException(**kwargs)
            elif ex.status_code == 403:
                ex = SeguridadException(**kwargs)
            else:
                ex = ErrorOperacionalException(**kwargs)
        else:
            exc_type, exc_obj, exc_tb = sys.exc_info()

            codigo = 'MOV-0003'
            mensaje = str(ex)
            if not mensaje:
                mensaje = nombre
            
            tb = obtener_ultimo_tb(exc_tb)
            mensaje += ' at ' + tb.tb_frame.f_code.co_filename + ':' + str(tb.tb_lineno)
            
            kwargs['codigo'] = codigo
            kwargs['mensaje'] = mensaje
            
            ex = ErrorOperacionalException(**kwargs)
    else:
        exc_type, exc_obj, exc_tb = sys.exc_info()

        codigo = 'MOV-0003'
        mensaje = str(ex)
        if not mensaje:
            mensaje = ex.__class__.__name__

        tb = obtener_ultimo_tb(exc_tb)
        mensaje += ' at ' + tb.tb_frame.f_code.co_filename + ':' + str(tb.tb_lineno)

        kwargs['codigo'] = codigo
        kwargs['mensaje'] = mensaje
        
        ex = ErrorOperacionalException(**kwargs)
    
    if logger:
        extra = ex.__dict__
        extra['ex'] = str(extra['ex']).replace('\n', ' ').replace('\r', ' ')
        extra['mensaje'] = str(extra['mensaje']).replace('\n', ' ').replace('\r', ' ')
        
        if isinstance(ex, AdvertenciaFuncionalException):
            logger.log(ConvitLevel.WARN, ex.mensaje.replace('\n', ' ').replace('\r', ' '), extra=extra)
        elif isinstance(ex, ErrorOperacionalException):
            logger.log(ConvitLevel.ALARM_INT, ex.mensaje.replace('\n', ' ').replace('\r', ' '), extra=extra)

    return ex