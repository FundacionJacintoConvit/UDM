# coding: utf-8

from django.http import HttpResponseRedirect
from to.MenuModel import MenuTo

def my_login_required(f):
    """
	Define si tiene acceso controlando solamente el login.
	
	Args:
	    f: La función.
        
	Returns:
	    La función decorada.
    """
	
    def wrap(request, *args, **kwargs):		
        """
    	Revisa si el usuario tiene acceso al recurso.
    	
    	Args:
    	    request: La petición HTTP.

        Returns:
		    Lo que devuelva la función original.
		"""

        if 'usuario' not in request.session:
            return HttpResponseRedirect('/acceso_denegado/')

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
	
    return wrap

def my_access_required(f):
    """
	Define si tiene acceso controlando login y acceso por menu.

    Args:
        f: La función.
        
    Returns:
        La función decorada.
    """
	
    def wrap(request, *args, **kwargs):		
        """
        Revisa si el usuario tiene acceso al recurso.
		
        Args:
            request: La petición HTTP.

        Returns:
            Lo que devuelva la función original.
        """

        # Para tener acceso por menu siempre hay que estar logueado
        if 'usuario' not in request.session:
            return HttpResponseRedirect('/acceso_denegado/')

        # Esta logueado, controla acceso por menu
        tipo_usuario = request.session['usuario_id']
        accion = f.__name__

        try:
            menu = MenuTo.objects.get(action = accion)
            menu.tipousuarios.get(id = tipo_usuario)			
        except Exception:
            return HttpResponseRedirect('/acceso_denegado/')

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap
