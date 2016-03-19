# coding: utf-8

from django.contrib.sessions.models import Session
from django.core.mail import EmailMultiAlternatives
from django.utils.module_loading import import_by_path

def load_backend(path):
    """
	Importar la ruta.
	
	Args:
	    path: La ruta.
		
	Returns:
	    La ruta importada.
	"""
    return import_by_path(path)()

def validar_session(request):
    """
	Define si tiene una session creada en el sistema. para filtar el usuario.
    Verifica si hay una session abierta para recuperar el usuario.
	
	Args:
	    request: La petición HTTP.
		
	Returns:
	    El usuario.
	"""
	
    try:        
        s = Session.objects.get(pk=request.COOKIES['sessionid'])
        user_id = s.get_decoded().get('_auth_user_id')        
        backend = load_backend(s.get_decoded().get('_auth_user_backend'))
        user = backend.get_user(user_id)
        usuario = [user_id, user.username, user.id_fisc, user.nom_ger]
    except Exception:            
        usuario = [0,None,-1,0]
    #retorna una tupla usuario_id, usuario, colaborador_id, coordinacion_id     
    return usuario


def enviar_correo(correo, cuerpo_mensaje, ruta_archivo_adjunto, subject, from_email, attach_file):
    """
	Define el envio de correo electronico.
	
	Args:
	    correo: El correo electrónico destino.
		cuerpo_mensaje: El cuerpo del correo.
		ruta_archivo_adjunto: La ruta de un archivo a adjuntar.
		subject: El título del correo.
		from_email: El correo electrónico que envía.
		attach_file: El archivo a adjuntar.
        
    Returns:
        La excepción en caso de que se genere.
	"""
	
    valor = 0
    to = correo    
    text_content = 'This is an important message.'            
    html_content = '<br>%s' % (cuerpo_mensaje)    
    
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        
        if attach_file:            
            msg.attach_file(ruta_archivo_adjunto)
            
        msg.send()
    except Exception, e:
        valor = e

    return valor