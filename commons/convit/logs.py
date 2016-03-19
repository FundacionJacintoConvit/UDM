# coding: utf-8

import logging
from decimal import Decimal
from datetime import date, time, datetime

from commons import local
from commons.convit import constants

from django.conf import settings

PARAM_LONGITUD = 100

class ConvitFilter(logging.Filter):
    """
    Filtro de logs de Convit, agrega origen, destino aplicación y request_id de estar disponibles en el local.
    """

    def filter(self, record):
        """
        Metodo que filtra los logs.

        Args:
            record: El registro que se pasara al log.
            
        Returns:
            True.
        """
            
        record.request_id = getattr(local, 'request_id', "NO_REQUEST_ID")
        record.usuario = getattr(local, 'usuario', "NO_USUARIO")
        if not hasattr(record, 'origen'):
            record.origen = getattr(local, 'origen', "NO_ORIGEN")
        if not hasattr(record, 'destino'):
            record.destino = getattr(local, 'destino', "NO_DESTINO")
        if not hasattr(record, 'aplicacion'):
            record.aplicacion = settings.APLICACION
        if not hasattr(record, 'tipo_transaccion'):
            record.tipo_transaccion = constants.TIPO_TRANSACCION_DB
        if not hasattr(record, 'transaccionId'):
            setattr(record, 'transaccionId', '')
        if not hasattr(record, 'codigo'):
            record.codigo = ''
        if not hasattr(record, 'mensaje'):
            record.mensaje = ''
        if not hasattr(record, 'tiempo'):
            record.tiempo = ''
        if not hasattr(record, 'metodo'):
            record.metodo = ''
        if not hasattr(record, 'param_entrada'):
            record.param_entrada = ''
        if not hasattr(record, 'ex'):
            record.ex = ''
            
        return True
		
class ConvitLevel(object):
    """
	Clase de Nivel de Trazas para manejar los niveles particulares de Convit.
    
    PERF_INT: Número del nivel PERF.
    STATS_INT: Número del nivel STATS.
    ALARM_INT: Número del nivel ALARM.
    
    PERF_STRING: Nombre del nivel PERF.
    STATS_STRING: Nombre del nivel STAT.
    ALARM_STRING: Nombre del nivel ALARM.
    WARN_STRING: Nombre del nivel WARN.
    INFO_STRING: Nombre del nivel INFO.
    DEBUG_STRING: Nombre del nivel DEBUG.
    
    CRITICAL: Objeto nivel CRITICAL.
    ERROR: Objeto nivel ERROR.
    WARN: Objeto nivel WARN.
    INFO: Objeto nivel INFO.
    DEBUG: Objeto nivel DEBUG.
    NOTSET: Objeto nivel NOTSET.
    PERF: Objeto nivel PERF.
    STATS: Objeto nivel STATS.
    ALARM: Objeto nivel ALARM.
	"""
    
    PERF_INT = logging.DEBUG + 11
    STATS_INT = logging.WARN - 1
    ALARM_INT = logging.ERROR - 1    
    
    PERF_STRING = 'PERF'
    STATS_STRING = 'STATS'
    ALARM_STRING = 'ALARM'
    WARN_STRING = 'WARN'
    INFO_STRING = 'INFO'
    DEBUG_STRING = 'DEBUG'
    
    logging.addLevelName(PERF_INT, PERF_STRING)
    logging.addLevelName(STATS_INT, STATS_STRING)
    logging.addLevelName(ALARM_INT, ALARM_STRING)
    
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET
    
    PERF = logging.getLevelName(PERF_STRING)
    STATS = logging.getLevelName(STATS_STRING)
    ALARM = logging.getLevelName(ALARM_STRING)
    
def obj_a_params(obj, prefijo=None, profundidad=0):
    """
    Convierte un obj en un string con el formato 'k1=v1,k2=v2'
    
    Args:
        obj: El diccionario que se convertirá al string de parámetros.
        prefijo: El prefijo a agregarle a la clave.
        profundidad: La profundidad que se va a generar los parámetros.
        
    Returns:
        El string de parámetros.
    """

    result = []
    
    try:
        if isinstance(obj, dict):
            diccionario = obj
        elif obj.__dict__:
            diccionario = obj.__dict__
        else:
            diccionario = None

        if diccionario and profundidad < 2:
            for k,v in diccionario.iteritems():
                if not v or isinstance(v, ( bool, int, long, float, complex, Decimal, str, unicode, list, tuple, dict, date, time, datetime )):
                    if prefijo:
                        result.append(prefijo + '.' + str(k) + '=' + str(v))
                    else:
                        result.append(str(k) + '=' + str(v))
                else:
                    if prefijo:
                        result += obj_a_params(v, prefijo + '.' + str(k), profundidad + 1)
                    else:
                        result += obj_a_params(v, str(k), profundidad + 1)
    except Exception as ex:
        pass

    if profundidad == 0:
        return ','.join(result)[:PARAM_LONGITUD]
    else:
        return result