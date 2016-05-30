# coding: utf-8

import logging

from django.forms import ModelForm, HiddenInput, TextInput, Textarea, DateInput, Select, RadioSelect, FileInput, ChoiceField, CheckboxInput, ValidationError, CharField, ChoiceField
from django.forms.models import modelformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from unidaddiagnosticomolecular.models import UDMUser, Paciente, Diagnostico, DiagnosticoExamen, DiagnosticoSintoma, DiagnosticoEstudio, DiagnosticoAntecedente, DiagnosticoTrasladoMuestra, Ciudad, Estado, Institucion, Unidad, EstadoCivil, NivelEstudio, TipoEnfermedad, TipoCancer, TipoAntecedente, TipoEstudio, TipoExamen
logger = logging.getLogger(__name__)

class UDMUserForm(ModelForm):
    class Meta(UserCreationForm.Meta):
        model = UDMUser
        fields = [ 'first_name', 'last_name', 'nombre_segundo', 'apellido_segundo', 'nacionalidad', 'cedula_pasaporte', 'edad', 'sexo', 'profesion', 'especializacion', 'especializacion_culminada', 'numero_mpps', 'numero_colegio', 'ubicacion_colegio', 'email', 'telefono', 'institucion', 'unidad', 'unidad_fecha_inicio', 'unidad_fecha_fin', 'unidad_director', 'unidad_director_telefono', 'unidad_director_email', 'ciudad' ]
        widgets = {
            'first_name': TextInput(attrs={ 'size': '40', 'disabled': 'true' }),
            'nombre_segundo': TextInput(attrs={ 'size': '40', 'disabled': 'true' }),
            'last_name': TextInput(attrs={ 'size': '40', 'disabled': 'true' }),
            'apellido_segundo': TextInput(attrs={ 'size': '40', 'disabled': 'true' }),
            'nacionalidad': Select(attrs={ 'disabled': 'true' }),
            'cedula_pasaporte': TextInput(attrs={ 'size': '40', 'disabled': 'true' }),
            'edad': TextInput(attrs={ 'size': '3', 'disabled': 'true' }),
            'sexo': Select(attrs={ 'disabled': 'true' }),
            'profesion': TextInput(attrs={ 'size': '40', 'disabled': 'true' }), 
            'especializacion': TextInput(attrs={ 'size': '40', 'disabled': 'true' }), 
            'especializacion_culminada': Select(attrs={ 'disabled': 'true' }), 
            'numero_mpps': TextInput(attrs={ 'size': '40', 'disabled': 'true' }), 
            'numero_colegio': TextInput(attrs={ 'size': '40', 'disabled': 'true' }), 
            'ubicacion_colegio': TextInput(attrs={ 'size': '40', 'disabled': 'true' }), 
            'email': TextInput(attrs={ 'size': '40', 'disabled': 'true' }), 
            'telefono': TextInput(attrs={ 'size': '40', 'disabled': 'true' }),
            'institucion': Select(attrs={ 'disabled': 'true' }),
            'unidad': Select(attrs={ 'disabled': 'true' }),
            'telefono': TextInput(attrs={ 'size': '40', 'disabled': 'true' }),
            'ciudad': Select(attrs={ 'disabled': 'true' }),
            'firma': FileInput(attrs={ 'size': '40', 'disabled': 'true', 'accept': 'image/gif,image/jpeg,image/pjpeg,image/png,image/tiff,image/x-tiff' }),
        }
        labels = {
            'first_name': 'Primer Nombre',
            'last_name': 'Primer Apellido',
            'email': 'Correo electrónico', 
        }

class UDMUserCreationForm(UserCreationForm):

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            UDMUser._default_manager.get(username=username)
        except UDMUser.DoesNotExist:
            return username
        raise ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = UDMUser
        widgets = {
            'first_name': TextInput(attrs={ 'size': '40' }),
            'segundo_nombre': TextInput(attrs={ 'size': '40' }),
            'last_name': TextInput(attrs={ 'size': '40' }),
            'segundo_apellido': TextInput(attrs={ 'size': '40' }),
            'nacionalidad': Select(attrs={ }),
            'cedula_pasaporte': TextInput(attrs={ 'size': '40' }),
            'edad': TextInput(attrs={ 'size': '3' }),
            'sexo': Select(attrs={ }),
            'profesion': TextInput(attrs={ 'size': '40' }), 
            'especializacion': TextInput(attrs={ 'size': '40' }), 
            'especializacion_culminada': Select(attrs={ }), 
            'numero_mpps': TextInput(attrs={ 'size': '40' }), 
            'numero_colegio': TextInput(attrs={ 'size': '40' }), 
            'ubicacion_colegio': TextInput(attrs={ 'size': '40' }), 
            'email': TextInput(attrs={ 'size': '40' }), 
            'telefono': TextInput(attrs={ 'size': '40' }),
            'institucion': Select(attrs={ }),
            'unidad': Select(attrs={ }),
            'telefono': TextInput(attrs={ 'size': '40' }),
            'ciudad': Select(attrs={ }),
            'firma': FileInput(attrs={ 'size': '40', 'accept': 'image/gif,image/jpeg,image/pjpeg,image/png,image/tiff,image/x-tiff' }),
        }
        labels = {
            'first_name': 'Primer Nombre',
            'last_name': 'Primer Apellido',
            'email': 'Correo electrónico', 
        }

class UDMUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UDMUser
        widgets = {
            'first_name': TextInput(attrs={ 'size': '40' }),
            'segundo_nombre': TextInput(attrs={ 'size': '40' }),
            'last_name': TextInput(attrs={ 'size': '40' }),
            'segundo_apellido': TextInput(attrs={ 'size': '40' }),
            'nacionalidad': Select(attrs={ }),
            'cedula_pasaporte': TextInput(attrs={ 'size': '40' }),
            'edad': TextInput(attrs={ 'size': '3' }),
            'sexo': Select(attrs={ }),
            'profesion': TextInput(attrs={ 'size': '40' }), 
            'especializacion': TextInput(attrs={ 'size': '40' }), 
            'especializacion_culminada': Select(attrs={ }), 
            'numero_mpps': TextInput(attrs={ 'size': '40' }), 
            'numero_colegio': TextInput(attrs={ 'size': '40' }), 
            'ubicacion_colegio': TextInput(attrs={ 'size': '40' }), 
            'email': TextInput(attrs={ 'size': '40' }), 
            'telefono': TextInput(attrs={ 'size': '40' }),
            'institucion': Select(attrs={ }),
            'unidad': Select(attrs={ }),
            'telefono': TextInput(attrs={ 'size': '40' }),
            'ciudad': Select(attrs={ }),
            'firma': FileInput(attrs={ 'size': '40', 'accept': 'image/gif,image/jpeg,image/pjpeg,image/png,image/tiff,image/x-tiff' }),
        }
        labels = {
            'first_name': 'Primer Nombre',
            'last_name': 'Primer Apellido',
            'email': 'Correo electrónico', 
        }

class EstadoForm(ModelForm):
    """
    Clase Forma de la clase modelo Estado.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma EstadoForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = Estado
        fields = [ 'nombre' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
        }

class CiudadForm(ModelForm):
    """
    Clase Forma de la clase modelo Ciudad.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma CiudadForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = Ciudad
        fields = [ 'nombre', 'estado' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
        }
		
class InstitucionForm(ModelForm):
    """
    Clase Forma de la clase modelo Institución.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma InstitucionForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = Institucion
        fields = [ 'nombre' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
        }

class UnidadForm(ModelForm):
    """
    Clase Forma de la clase modelo Unidad.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma UnidadForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = Unidad
        fields = [ 'nombre' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
        }

class EstadoCivilForm(ModelForm):
    """
    Clase Forma de la clase modelo Estado Civil.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma EstadoCivilForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = EstadoCivil
        fields = [ 'nombre' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
        }

class NivelEstudioForm(ModelForm):
    """
    Clase Forma de la clase modelo Nivel de Estudio.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma NivelEstudioForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = NivelEstudio
        fields = [ 'nombre' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
        }

class TipoEnfermedadForm(ModelForm):
    """
    Clase Forma de la clase modelo TipoEnfermedad.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma TipoEnfermedadForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = TipoEnfermedad
        fields = [ 'nombre', 'orden' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
            'oorden': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '12' }),
        }

class TipoCancerForm(ModelForm):
    """
    Clase Forma de la clase modelo TipoCancer.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma TipoCancerForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = TipoCancer
        fields = [ 'nombre', 'orden' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
            'oorden': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '12' }),
        }

class TipoAntecedenteForm(ModelForm):
    """
    Clase Forma de la clase modelo TipoAntecedente.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma TipoAntecedenteForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = TipoAntecedente
        fields = [ 'nombre', 'orden' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
            'oorden': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '12' }),
        }

class TipoEstudioForm(ModelForm):
    """
    Clase Forma de la clase modelo TipoEstudio.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma TipoEstudioForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = TipoEstudio
        fields = [ 'nombre', 'orden' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
            'oorden': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '12' }),
        }

class TipoExamenForm(ModelForm):
    """
    Clase Forma de la clase modelo TipoExamen.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma TipoExamenForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = TipoExamen
        fields = [ 'nombre', 'tipo', 'orden' ]
        widgets = {
		    'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
		    'tipo': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
            'oorden': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '12' }),
        }

class PacienteForm(ModelForm):
    """
    Clase Forma de la clase modelo Paciente.
    """

    class Meta(object):
        """
        Clase meta de la clase forma PacienteForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = Paciente
        fields = [ 'id', 'numero_historia', 'nombre_primero', 'nombre_segundo', 'apellido_primero', 'apellido_segundo', 'tipo_identificacion', 'identificacion', 'partida_nacimiento', 'fecha_nacimiento', 'edad_anios', 'edad_meses', 'sexo', 'nacionalidad', 'estado_civil', 'nivel_estudio', 'represent_nombre_primero', 'represent_nombre_segundo', 'represent_apellido_primero', 'represent_apellido_segundo', 'represent_tipo_identificacion', 'represent_identificacion', 'represent_numero_hijo', 'represent_fecha_nacimiento', 'represent_sexo', 'represent_nacionalidad', 'represent_estado_civil', 'represent_nivel_estudio', 'telefono_local', 'telefono_celular1', 'telefono_celular2', 'correo_electronico', 'calle_avenida', 'sector_barrio_urb', 'casa_edificio', 'familiares_observaciones' ]
        widgets = {
		    'id': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true' }),
            'numero_historia': TextInput(attrs={ 'class': 'campo', 'size': '40' }),
		    'nombre_primero': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
		    'nombre_segundo': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
            'apellido_primero': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
            'apellido_segundo': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
			'tipo_identificacion': Select(attrs={ 'class': 'campo', 'onchange': 'tieneTipoIdentificacion(this); validar(this)' }),
			'identificacion': TextInput(attrs={ 'class': 'campo', 'size': '17', 'onkeypress': 'return revisarLetrasNumeros(event)', 'onchange': 'tieneIdentificacion(this); validar(this)' }),
			'partida_nacimiento': TextInput(attrs={ 'class': 'campo', 'size': '17', 'disabled': 'true', 'onkeypress': 'return revisarLetrasNumeros(event)', 'onchange': 'validar(this)' }),
			'fecha_nacimiento': DateInput(attrs={ 'class': 'campo', 'size': '40', 'readonly': 'true', 'onchange': 'calcularEdad(this); validar(this)' }),
			'edad_anios': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '12', 'onkeypress': 'return revisarNumeros(event)', 'onchange': 'tieneEdadAnios(this); validar(this)' }),
			'edad_meses': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '12', 'onkeypress': 'return revisarNumeros(event)', 'onchange': 'tieneEdadMeses(this); validar(this)' }),
            'sexo': Select(attrs={ 'class': 'campo', 'onchange': 'validar(this)' }),
            'nacionalidad': Select(attrs={ 'class': 'campo', 'onchange': 'validar(this)' }),
            'estado_civil': Select(attrs={ 'class': 'campo', 'onchange': 'validar(this)' }),			
            'nivel_estudio': Select(attrs={ 'class': 'campo', 'onchange': 'validar(this)' }),			
		    'represent_nombre_primero': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true', 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
		    'represent_nombre_segundo': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true', 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
            'represent_apellido_primero': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true', 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
            'represent_apellido_segundo': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true', 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
			'represent_tipo_identificacion': Select(attrs={ 'class': 'campo', 'disabled': 'true', 'onchange': 'validar(this)' }),
			'represent_identificacion': TextInput(attrs={ 'class': 'campo', 'size': '27', 'disabled': 'true', 'onkeypress': 'return revisarLetrasNumeros(event)', 'onchange': 'validar(this)' }),
			'represent_numero_hijo': TextInput(attrs={ 'class': 'campo', 'size': '27', 'disabled': 'true', 'onkeypress': 'return revisarNumeros(event)', 'onchange': 'validar(this)' }),
            'represent_sexo': Select(attrs={ 'class': 'campo', 'disabled': 'true', 'onchange': 'validar(this)' }),
            'represent_nacionalidad': Select(attrs={ 'class': 'campo', 'disabled': 'true', 'onchange': 'validar(this)' }),
			'represent_fecha_nacimiento': DateInput(attrs={ 'class': 'campo', 'size': '40', 'readonly': 'true', 'disabled': 'true', 'onchange': 'validar(this)' }),
            'represent_estado_civil': Select(attrs={ 'class': 'campo', 'disabled': 'true', 'onchange': 'validar(this)' }),			
            'represent_nivel_estudio': Select(attrs={ 'class': 'campo', 'disabled': 'true', 'onchange': 'validar(this)' }),			
			'telefono_local': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onkeypress': 'return revisarTelefono(event)', 'onchange': 'validar(this)' }),
			'telefono_celular1': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onkeypress': 'return revisarTelefono(event)', 'onchange': 'validar(this)' }),
			'telefono_celular2': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onkeypress': 'return revisarTelefono(event)', 'onchange': 'validar(this)' }),
			'correo_electronico': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onchange': 'validar(this)' }),
			'calle_avenida': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onchange': 'validar(this)' }),
			'sector_barrio_urb': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onchange': 'validar(this)' }),
			'casa_edificio': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onchange': 'validar(this)' }),
			'familiares_observaciones': Textarea(attrs={ 'class': 'campo', 'cols': '142', 'rows': '3', 'onchange': 'validar(this)' }),
        }
		
class PacienteMostrarForm(ModelForm):
    """
    Clase Forma de la clase modelo Paciente.
    """

    class Meta(object):
        """
        Clase meta de la clase forma PacienteForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = Paciente
        fields = [ 'id', 'numero_historia', 'nombre_primero', 'nombre_segundo', 'apellido_primero', 'apellido_segundo', 'edad_anios', 'edad_meses' ]
        widgets = {
            'id': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true' }),
            'numero_historia': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true' }),
		    'nombre_primero': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true' }),
		    'nombre_segundo': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true' }),
            'apellido_primero': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true' }),
            'apellido_segundo': TextInput(attrs={ 'class': 'campo', 'size': '40', 'disabled': 'true' }),
			'edad_anios': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '12', 'disabled': 'true' }),
			'edad_meses': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '12', 'disabled': 'true' }),
        }

class DiagnosticoMedicoForm(ModelForm):
    """
    Clase Forma de la clase modelo Diagnostico.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma DiagnosticoForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = Diagnostico
        fields = [ 'id', 'medico_tipo_diagnostico', 'medico_observaciones', 'medico_fecha_ini_signos', 'medico_fecha_fin_signos', 'medico_fecha_ini_sintomas', 'medico_fecha_fin_sintomas', 'medico_signos', 'medico_sintomas', 'medico_presencia_tumor', 'medico_ubicacion_tumor', 'medico_presencia_metastasis', 'medico_ubicacion_metastasis', 'medico_otros_estudios', 'medico_diagnostico_presuntivo', 'medico_familiar_antecedente', 'medico_familiar_nexo', 'medico_familiar_tipo_enfermedad', 'medico_familiar_tipo_cancer', 'medico_familiar_enfermedad_otra', 'medico_paciente_cumplio_condiciones', 'medico_paciente_cumplio_ayuno_3', 'medico_paciente_cumplio_ayuno_12', 'medico_paciente_cumplio_observaciones', 'medico_ubicacion_institucion', 'medico_ubicacion_telefono', 'medico_ubicacion_piso', 'medico_ubicacion_habitacion', 'udm_tipo_muestra', 'udm_tipo_muestra_otro' ]
        widgets = {
                'id': TextInput(attrs={ 'class': 'campo', 'readonly': 'true', 'size': '40' }),
                'medico_tipo_diagnostico': RadioSelect(attrs={ 'class': 'campo', 'onchange': 'cambiarTipoDiagnostico(this); validar(this)' }),
                'medico_familiar_antecedente': RadioSelect(choices=(( True, 'Si' ), ( False, 'No' )), attrs={ 'class': 'campo', 'style': 'visibility: hidden', 'onchange': 'cambiarFamiliarAntecedente(this); validar(this)' }),
                'medico_familiar_nexo': TextInput(attrs={ 'class': 'campo', 'size': '40', 'style': 'visibility: hidden', 'onchange': 'validar(this)' }),
                'medico_familiar_tipo_enfermedad': Select(attrs={ 'class': 'campo', 'visibility': 'hidden', 'onchange': 'cambiarFamiliarEnfermedad(); validar(this)' }),
                'medico_familiar_tipo_cancer': Select(attrs={ 'class': 'campo', 'onchange': 'cambiarFamiliarCancer(); validar(this)' }),
	            'medico_familiar_enfermedad_otra': TextInput(attrs={ 'class': 'campo', 'size': '40', 'style': 'visibility: hidden', 'onchange': 'validar(this)' }),
                'medico_observaciones': Textarea(attrs={ 'class': 'campo', 'cols': '142', 'rows': '3', 'onchange': 'validar(this)' }),
                'medico_fecha_ini_signos': DateInput(attrs={ 'class': 'campo', 'readonly': 'true', 'onchange': 'validar(this)' }),
                'medico_fecha_fin_signos': DateInput(attrs={ 'class': 'campo', 'readonly': 'true', 'onchange': 'validar(this)' }),
                'medico_fecha_ini_sintomas': DateInput(attrs={ 'class': 'campo', 'readonly': 'true', 'onchange': 'validar(this)' }),
                'medico_fecha_fin_sintomas': DateInput(attrs={ 'class': 'campo', 'readonly': 'true', 'onchange': 'validar(this)' }),
                'medico_signos': Textarea(attrs={ 'class': 'campo', 'cols': '95', 'rows': '3', 'onchange': 'validar(this)' }),
                'medico_sintomas': Textarea(attrs={ 'class': 'campo', 'cols': '95', 'rows': '3', 'onchange': 'validar(this)' }),
                'medico_diagnostico_presuntivo': Textarea(attrs={ 'class': 'campo', 'cols': '95', 'rows': '3', 'onchange': 'validar(this)' }),
                'medico_presencia_tumor': RadioSelect(choices=(( 'S', 'Si' ), ( 'N', 'No' ), ( 'D', 'No determinado' )), attrs={ 'class': 'campo', 'onchange': 'cambiarPresenciaTumor(); validar(this)' }),
                'medico_ubicacion_tumor': Textarea(attrs={ 'class': 'campo', 'cols': '42', 'rows': '3', 'style': 'visibility: hidden', 'onchange': 'validar(this)' }),
                'medico_presencia_metastasis': RadioSelect(choices=(( 'S', 'Si' ), ( 'N', 'No' ), ( 'D', 'No determinado' )), attrs={ 'class': 'campo', 'onchange': 'cambiarPresenciaMetastasis(); validar(this)' }),
                'medico_ubicacion_metastasis': Textarea(attrs={ 'class': 'campo', 'cols': '42', 'rows': '3', 'style': 'visibility: hidden', 'onchange': 'validar(this)' }),
                'medico_otros_estudios': Textarea(attrs={ 'class': 'campo', 'cols': '142', 'rows': '3', 'onchange': 'validar(this)' }),
                'medico_ubicacion_instituto': Select(attrs={ 'class': 'campo' }),
	            'medico_ubicacion_telefono': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onkeypress': 'return revisarTelefono(event)', 'onchange': 'validar(this)' }),
	            'medico_ubicacion_piso': TextInput(attrs={ 'class': 'campo', 'size': '5', 'onkeypress': 'return revisarNumeros(event)', 'onchange': 'validar(this)' }),
	            'medico_ubicacion_habitacion': TextInput(attrs={ 'class': 'campo', 'size': '5', 'onkeypress': 'return revisarLetrasNumeros(event)', 'onchange': 'validar(this)' }),
                'medico_paciente_cumplio_condiciones': RadioSelect(choices=(( 'S', 'Si' ), ( 'N', 'No' )), attrs={ 'class': 'campo', 'onchange': 'cambiarCumplioCondiciones(); validar(this)' }),
                'medico_paciente_cumplio_ayuno_12': CheckboxInput(attrs={ 'class': 'campo', 'onchange': 'validar(this)' }),
                'medico_paciente_cumplio_ayuno_3': CheckboxInput(attrs={ 'class': 'campo', 'onchange': 'validar(this)' }),
                'medico_paciente_cumplio_observaciones': Textarea(attrs={ 'class': 'campo', 'cols': '120', 'rows': '3', 'onchange': 'validar(this)' }),
                'udm_tipo_muestra': Select(attrs={ 'class': 'campo', 'onchange': 'cambiarTipoMuestra(); validar(this)' }),
                'udm_tipo_muestra_otro': TextInput(attrs={ 'class': 'campo', 'size': '40', 'style': 'visibility: hidden', 'onchange': 'validar(this)' }),
        }
		
class DiagnosticoPatologoForm(ModelForm):
    """
    Clase Forma de la clase modelo Diagnostico.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma DiagnosticoForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = Diagnostico
        fields = [ 'id', 'patologo_tipo_muestra', 'patologo_resultado', 'patologo_marcadores', 'patologo_observaciones' ]
        widgets = {
                'id': TextInput(attrs={ 'class': 'campo', 'readonly': 'true', 'size': '40' }),
                'patologo_tipo_muestra': Textarea(attrs={ 'class': 'campo', 'cols': '142', 'rows': '3', 'onchange': 'validar(this)' }),
                'patologo_resultado': Textarea(attrs={ 'class': 'campo', 'cols': '142', 'rows': '3', 'onchange': 'validar(this)' }),
                'patologo_marcadores': Textarea(attrs={ 'class': 'campo', 'cols': '142', 'rows': '3', 'onchange': 'validar(this)' }),
                'patologo_observaciones': Textarea(attrs={ 'class': 'campo', 'cols': '142', 'rows': '3', 'onchange': 'validar(this)' }),
        }

class DiagnosticoUDMForm(ModelForm):
    """
    Clase Forma de la clase modelo Diagnostico.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma DiagnosticoForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = Diagnostico
        fields = [ 'id', 'udm_observaciones', 'udm_tipo_muestra', 'udm_tipo_muestra_otro', 'udm_tecnica_deteccion' ]
        widgets = {
                'id': TextInput(attrs={ 'class': 'campo', 'readonly': 'true', 'size': '40' }),
                'udm_observaciones': Textarea(attrs={ 'class': 'campo', 'cols': '142', 'rows': '3', 'onchange': 'validar(this)' }),
                'udm_tipo_muestra': Select(attrs={ 'class': 'campo', 'onchange': 'cambiarTipoMuestra(); validar(this)' }),
                'udm_tipo_muestra_otro': TextInput(attrs={ 'class': 'campo', 'size': '40', 'style': 'visibility: hidden', 'onchange': 'validar(this)' }),
                'udm_tecnica_deteccion': Select(attrs={ 'class': 'campo', 'onchange': 'validar(this)' }),
        }
		
class DiagnosticoEstudioForm(ModelForm):
    """
    Clase Forma de la clase modelo DiagnosticoEstudio.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma DiagnosticoEstudioForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = DiagnosticoEstudio
		
        fields = [ 'id', 'nombre', 'link', 'ruta', 'tipo_estudio' ]
        widgets = {
		    'id': HiddenInput(attrs={ 'class': 'campo' }),
			'nombre': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onchange': 'validar(this)' }),
			'link': TextInput(attrs={ 'class': 'campo', 'size': '40', 'onchange': 'validar(this)' }),
			'ruta': FileInput(attrs={ 'class': 'campo', 'size': '40', 'accept': 'image/gif,image/jpeg,image/pjpeg,image/png,image/tiff,image/x-tiff,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation', 'onchange': 'validar(this)' }),
            'orden': HiddenInput(attrs={ 'class': 'campo' }),
			'tipo_estudio': HiddenInput(attrs={ 'class': 'campo', 'size': '40', 'onchange': 'validar(this)' }),
        }
		
class DiagnosticoExamenForm(ModelForm):
    """
    Clase Forma de la clase modelo DiagnosticoExamen.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma DiagnosticoExamenForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = DiagnosticoExamen
        fields = [ 'id', 'nombre', 'presente', 'resultado', 'tipo', 'orden', 'tipo_examen' ]
        widgets = {
		    'id': HiddenInput(attrs={ 'class': 'campo' }),
		    'nombre': HiddenInput(attrs={ 'class': 'campo', 'size': '40' }),
            'presente': CheckboxInput(attrs={ 'class': 'campo', 'onclick': 'validar(this)' }),
			'resultado': RadioSelect(choices=(( True, 'Si' ), ( False, 'No' )), attrs={ 'class': 'campo', 'onclick': 'cambiarResultadoPresente(this); validar(this)' }),
			'tipo': HiddenInput(attrs={ 'class': 'campo' }),
            'orden': HiddenInput(attrs={ 'class': 'campo' }),
            'tipo_examen': HiddenInput(attrs={ 'class': 'campo' }),
        }
		
class DiagnosticoSintomaForm(ModelForm):
    """
    Clase Forma de la clase modelo DiagnosticoSintoma.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma DiagnosticoSintomaForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = DiagnosticoSintoma
        fields = [ 'id', 'nombre', 'presente', 'cuantos', 'personas', 'tipos', 'orden' ]
        widgets = {
		    'id': HiddenInput(attrs={ 'class': 'campo' }),
            'nombre': HiddenInput(attrs={ 'class': 'campo' }),
            'presente': CheckboxInput(attrs={ 'class': 'campo', 'onchange': 'cambiarSintomaPresente(); validar(this)' }),
			'cuantos': TextInput(attrs={ 'class': 'campo', 'style': 'text-align: right;', 'size': '20', 'disabled': 'disabled', 'onkeypress': 'return revisarNumeros(event)', 'onchange': 'validar(this)' }),
			'personas': TextInput(attrs={ 'class': 'campo', 'size': '20', 'disabled': 'disabled', 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
			'tipos': TextInput(attrs={ 'class': 'campo', 'size': '20', 'disabled': 'disabled', 'onchange': 'validar(this)' }),
            'orden': HiddenInput(attrs={ 'class': 'campo' }),
        }

class DiagnosticoAntecedenteForm(ModelForm):
    """
    Clase Forma de la clase modelo DiagnosticoAntecedente.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma DiagnosticoAntecedenteForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = DiagnosticoAntecedente
        fields = [ 'id', 'antecedente', 'nexo_familiar', 'otro', 'presente', 'orden', 'tipo_antecedente' ]
        widgets = {
		    'id': HiddenInput(attrs={ 'class': 'campo' }),
			'antecedente': TextInput(attrs={ 'class': 'campo', 'size': '20', 'onchange': 'validar(this)' }),
			'nexo_familiar': TextInput(attrs={ 'class': 'campo', 'disabled': 'disabled', 'size': '20', 'onchange': 'validar(this)' }),
			'otro': HiddenInput(attrs={ 'class': 'campo' }),
            'presente': RadioSelect(choices=(( True, 'Si' ), ( False, 'No' )), attrs={ 'class': 'campo', 'onclick': 'cambiarAntecedentesPresente(this); validar(this)' }),
			'tipo_antecedente': HiddenInput(attrs={ 'class': 'campo', 'size': '20', 'onchange': 'validar(this)' }),
            'orden': HiddenInput(attrs={ 'class': 'campo' }),
        }

class DiagnosticoTrasladoMuestraForm(ModelForm):
    """
    Clase Forma de la clase modelo DiagnosticoTrasladoMuestra.
    """
    
    class Meta(object):
        """
        Clase meta de la clase forma DiagnosticoTrasladoMuestraForm.
        
        model: La clase modelo.
        fields: Los campos a mostrar.
        widgets: Los tipos de componentes visuales.
        """
        
        model = DiagnosticoTrasladoMuestra
        fields = [ 'id', 'ruta', 'orden' ]
        widgets = {
		    'id': HiddenInput(attrs={ 'class': 'campo' }),
			'ruta': FileInput(attrs={ 'class': 'campo', 'size': '40', 'accept': 'image/gif,image/jpeg,image/pjpeg,image/png,image/tiff,image/x-tiff,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation', 'onchange': 'validar(this)' }),
            'orden': HiddenInput(attrs={ 'class': 'campo' }),
        }

class UDMRegistroUserForm(ModelForm): #modelFomr
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            UDMUser._default_manager.get(username=username)
        except UDMUser.DoesNotExist:
            return username
        raise ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = UDMUser
        fields = [ 'first_name', 'last_name', 'nombre_segundo', 'apellido_segundo', 'nacionalidad', 'cedula_pasaporte', 'edad', 'fecha_nacimiento','sexo','email','profesion', 'especializacion', 'especializacion_culminada' , 'numero_mpps', 'numero_colegio', 'email', 'telefono', 'unidad_fecha_inicio', 'unidad_fecha_fin', 'unidad_director', 'unidad_director_telefono', 'unidad_director_email']
        # , 'ubicacion_colegio',  'institucion', 'unidad', 'ciudad' ]
        widgets = {
            'first_name': TextInput(attrs={ 'size': '35', 'enable': 'true' ,'onkeypress': 'return revisarLetras(event)','onchange': 'validar(this)' }),
            'nombre_segundo': TextInput(attrs={ 'size': '35', 'enable': 'true' , 'onkeypress': 'return revisarLetras(event)','onchange': 'validar(this)' }),
            'last_name': TextInput(attrs={ 'size': '35', 'enable': 'true', 'onkeypress': 'return revisarLetras(event)','onchange': 'validar(this)'  }),
            'apellido_segundo': TextInput(attrs={ 'size': '35', 'enable': 'true', 'onkeypress': 'return revisarLetras(event)','onchange': 'validar(this)'  }),
            'cedula_pasaporte': TextInput(attrs={ 'size': '35', 'enable': 'true','onkeypress': 'return revisarLetrasNumeros(event)', 'onchange': 'validar(this)' }),
            'fecha_nacimiento': DateInput(attrs={ 'class': 'campo', 'size': '32', 'readonly': 'true', 'onchange': 'calcularEdad(this); validar(this)' }),
            'edad': TextInput(attrs={'class': 'campo', 'size': '12', 'enable': 'true', 'onkeypress': 'return revisarNumeros(event)', 'onchance':'tieneEdadAnios(this);'}),
            'sexo': Select(attrs={ 'class': 'campo', 'onchange': 'validar(this)' }),
            'nacionalidad': Select(attrs={'class': 'campo', 'onchange': 'validar(this)'}),
            'profesion': Select(attrs={'enable': 'true' , 'onchange':  'validar(this)'}),
            'especializacion': TextInput(attrs={ 'size': '35', 'enable': 'true','onkeypress': 'return revisarLetras(event)', 'onchange':  'validar(this)' }),
            'especializacion_culminada': Select(attrs={ 'enable': 'true', 'onchange':  'validar(this)' }),
            'numero_mpps': TextInput(attrs={ 'size': '35', 'enable': 'true', 'onkeypress': 'return revisarNumeros(event)', 'onchange':  'validar(this)' }),
            'numero_colegio': TextInput(attrs={ 'size': '35', 'enable': 'true', 'onkeypress': 'return revisarNumeros(event)', 'onchange':  'validar(this)' }),
            #'ubicacion_colegio': Select(attrs={ 'enable': 'true' }),
            'email': TextInput(attrs={ 'size': '35', 'enable': 'true', 'onchange':  'validar(this)' }),
            'telefono': TextInput(attrs={ 'size': '35', 'enable': 'true', 'onkeypress': 'return revisarTelefono(event)', 'onchange':  'validar(this)' }),
            'unidad_fecha_inicio':  DateInput(attrs={ 'class': 'campo', 'size': '25', 'readonly': 'true', 'onchange':  'validar(this)' }),
            'unidad_fecha_fin': DateInput(attrs={ 'class': 'campo', 'size': '25', 'readonly': 'true' }),
            'unidad_director': TextInput(attrs={ 'size': '35', 'enable': 'true' , 'onkeypress': 'return revisarLetras(event)', 'onchange': 'validar(this)' }),
            'unidad_director_telefono': TextInput(attrs={ 'size': '35', 'enable': 'true',  'onkeypress': 'return revisarTelefono(event)','onchange': 'validar(this)' }),
            'unidad_director_email': TextInput(attrs={ 'size': '35', 'enable': 'true','onchange': 'validar(this)' }),
            #'institucion': Select(attrs={ 'disabled': 'true' }),
            #'unidad': Select(attrs={ 'disabled': 'true' }),
            #'ciudad': Select(attrs={ 'disabled': 'true' }),
            #'firma': FileInput(attrs={ 'size': '40', 'disabled': 'true', 'accept': 'image/gif,image/jpeg,image/pjpeg,image/png,image/tiff,image/x-tiff' }),
        }
        labels = {
            'first_name': 'Primer Nombre',
            'last_name': 'Primer Apellido',
            'email': 'Correo electrónico',
        }


DiagnosticoEstudioFormSet = modelformset_factory(DiagnosticoEstudio, form=DiagnosticoEstudioForm, extra=0, can_delete=True)
DiagnosticoExamenFormSet = modelformset_factory(DiagnosticoExamen, form=DiagnosticoExamenForm, extra=0)
DiagnosticoSintomaFormSet = modelformset_factory(DiagnosticoSintoma, form=DiagnosticoSintomaForm, extra=0)
DiagnosticoAntecedenteFormSet = modelformset_factory(DiagnosticoAntecedente, form=DiagnosticoAntecedenteForm, extra=0)
DiagnosticoTrasladoMuestraFormSet = modelformset_factory(DiagnosticoTrasladoMuestra, form=DiagnosticoTrasladoMuestraForm, extra=3, can_delete=True)