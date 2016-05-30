# coding: utf-8

from datetime import date, datetime
import os
import logging
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, Spacer
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django_tables2 import Table, LinkColumn, RequestConfig
from django_tables2.columns import TemplateColumn
from django_tables2.utils import A
from django.db.models import Q
from django.conf import settings
from django.forms.models import modelformset_factory

from commons.convit import constants
from commons.convit.decorators import ConvitLoggerExceptionDecorator
from unidaddiagnosticomolecular.models import Paciente, Diagnostico, DiagnosticoExamen, DiagnosticoSintoma, DiagnosticoEstudio, DiagnosticoAntecedente, DiagnosticoTrasladoMuestra, Ciudad, Estado, TipoAntecedente, TipoEstudio, TipoExamen, HistoricoCambio, Parroquia, Municipio, EstadoCivil, NivelEstudio, UDMUser, Institucion, Unidad
from unidaddiagnosticomolecular.forms import PacienteForm, PacienteMostrarForm, DiagnosticoMedicoForm, DiagnosticoPatologoForm, DiagnosticoUDMForm, DiagnosticoExamenForm, DiagnosticoSintomaForm, DiagnosticoEstudioForm, DiagnosticoExamenForm, DiagnosticoAntecedenteForm, DiagnosticoTrasladoMuestraForm, UDMUserForm, DiagnosticoExamenFormSet, DiagnosticoSintomaFormSet, DiagnosticoEstudioFormSet, DiagnosticoExamenFormSet, DiagnosticoAntecedenteFormSet, DiagnosticoTrasladoMuestraFormSet, UDMRegistroUserForm


logger = logging.getLogger(__name__)

class LinkDateTimeColumn(LinkColumn):
    def __init__(self, viewname, format, *args, **extra):
        super(LinkDateTimeColumn, self).__init__(viewname, *args, **extra)
        self.format = format

    def render(self, value, record, bound_column):  
        if value != None:
            value = value.strftime(self.format)

        return super(LinkDateTimeColumn, self).render(value, record, bound_column)

class HistoricoCambiosTable(Table):
    """
        Clase que representa una tabla HTML que lista los pacientes.

    	Fecha: La columna de la fecha de la modificacion.
    	Campo_Modificado: La columna del campo modificado.
        Valor_Anterior: La columna del valor anterior.
        Valor_Actual: La columna del valor actual.
    	Medico: La columna del nombre del medico.
        """

    Fecha = TemplateColumn(template_code='<label class="tdCustom">{{record.fecha }} </label>')
    Campo_Modificado = TemplateColumn(template_code='<label class="tdCustom">{{record.campo_modificado }} </label>')
    Valor_Anterior = TemplateColumn(template_code='<label class="tdCustom">{{record.valor_anterior }} </label>')
    Valor_Actual = TemplateColumn(template_code='<label class="tdCustom">{{record.valor_actual }} </label>')
    Medico = TemplateColumn(template_code='<label class="tdCustom">{{record.medico }} </label>')

    class Meta(object):
        """
        Clase meta de la clase DiagnosticoMedicoTable.

        model: La clase modelo.
        attrs: Los atributos específicos de la tabla.
        fields: Los campos a mostrar.
        """

        attrs = {'class': 'paleblue', 'width': '100%'}

class PacientesTable(Table):
    """
    Clase que representa una tabla HTML que lista los pacientes.

	numero_historia: La columna número de historia.
	partida_nacimiento: LA columna partida de nacimiento
	identificacion: La columna cedula.
    nombre: La columna nombre.
    apellido: La columna apellido.
	ciudad: La columna ciudad.
	estado: La columna estado.
    """

    seleccionar = TemplateColumn(template_code='<input name="id" type="radio" value="{{ record.paciente_id }}" />')
    Numero_de_Historia = TemplateColumn(template_code='<label class="tdCustom">{{record.paciente_id }} </label>')
    Partida_de_Nacimiento = TemplateColumn(template_code='<label class="tdCustom">{{record.partida_nacimiento }} </label>')
    identificacion = TemplateColumn(template_code='<label class="tdCustom">{{record.identificacion }} </label>')
    Nombre = TemplateColumn(template_code='<label class="tdCustom">{{record.nombre }} </label>')
    Apellido = TemplateColumn(template_code='<label class="tdCustom">{{record.apellido }} </label>')
    Ciudad = TemplateColumn(template_code='<label class="tdCustom">{{record.ciudad }} </label>')
    Estado = TemplateColumn(template_code='<label class="tdCustom">{{record.estado }} </label>')

    class Meta(object):
        """
        Clase meta de la clase DiagnosticoMedicoTable.

        model: La clase modelo.
        attrs: Los atributos específicos de la tabla.
        fields: Los campos a mostrar.
        """

        attrs = { 'class': 'paleblue', 'width': '100%' }

class DiagnosticoMedicoTable(Table):
    """
    Clase que representa una tabla HTML que lista los diagnósticos.
    
	numero_historia: La columna número de historia.
	identificacion: La columna cedula.
    nombre: La columna nombre.
    apellido: La columna apellido.
	ciudad: La columna ciudad.
	estado: La columna estado.
    """

    seleccionar = TemplateColumn(template_code='<input name="id" type="radio" value="{{ record.id }}" />')
    id = LinkColumn('salvar_diagnostico_medico', verbose_name='N de solicitud de exámen', args=[A('id')])
    creacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Solicitud de Exámen', args=[A('id')])
    paciente_id = LinkColumn('salvar_diagnostico_medico', verbose_name='Número de Historia', args=[A('id')])
    identificacion = LinkColumn('salvar_diagnostico_medico', verbose_name='C.I. / Pasaporte', args=[A('id')])
    nombre = LinkColumn('salvar_diagnostico_medico', verbose_name='Nombre', args=[A('id')])
    apellido = LinkColumn('salvar_diagnostico_medico', verbose_name='Apellido', args=[A('id')])
    ciudad = LinkColumn('salvar_diagnostico_medico', verbose_name='Ciudad', args=[A('id')])
    estado = LinkColumn('salvar_diagnostico_medico', verbose_name='Estado', args=[A('id')])
    medico_modificacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Modificación Médico', args=[A('id')])
    patologo_modificacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Modificación Patólogo', args=[A('id')])
    udm_modificacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Modificación UDM', args=[A('id')])
    
    class Meta(object):
        """
        Clase meta de la clase DiagnosticoMedicoTable.
        
        model: La clase modelo.
        attrs: Los atributos específicos de la tabla.
        fields: Los campos a mostrar.
        """

        attrs = { 'class': 'paleblue', 'width': '100%' }

class DiagnosticoPatologoTable(Table):
    """
    Clase que representa una tabla HTML que lista los diagnósticos.
    
	numero_historia: La columna número de historia.
	identificacion: La columna cedula.
    nombre: La columna nombre.
    apellido: La columna apellido.
	ciudad: La columna ciudad.
	estado: La columna estado.
    """

    seleccionar = TemplateColumn(template_code='<input name="id" type="radio" value="{{ record.id }}" />')
    id = LinkColumn('salvar_diagnostico_patologo', verbose_name='N de solicitud de exámen', args=[A('id')])
    creacion_fecha = LinkDateTimeColumn('salvar_diagnostico_patologo', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Solicitud de Exámen', args=[A('id')])
    paciente_id = LinkColumn('salvar_diagnostico_patologo', verbose_name='Número de Historia', args=[A('id')])
    identificacion = LinkColumn('salvar_diagnostico_patologo', verbose_name='C.I. / Pasaporte', args=[A('id')])
    nombre = LinkColumn('salvar_diagnostico_patologo', verbose_name='Nombre', args=[A('id')])
    apellido = LinkColumn('salvar_diagnostico_patologo', verbose_name='Apellido', args=[A('id')])
    ciudad = LinkColumn('salvar_diagnostico_patologo', verbose_name='Ciudad', args=[A('id')])
    estado = LinkColumn('salvar_diagnostico_patologo', verbose_name='Estado', args=[A('id')])
    medico_modificacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Modificación Médico', args=[A('id')])
    patologo_modificacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Modificación Patólogo', args=[A('id')])
    udm_modificacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Modificación UDM', args=[A('id')])
    
    class Meta(object):
        """
        Clase meta de la clase DiagnosticoPatologoTable.
        
        model: La clase modelo.
        attrs: Los atributos específicos de la tabla.
        fields: Los campos a mostrar.
        """

        attrs = { 'class': 'paleblue', 'width': '100%' }
		
class DiagnosticoUdmTable(Table):
    """
    Clase que representa una tabla HTML que lista los diagnósticos.
    
	numero_historia: La columna número de historia.
	identificacion: La columna cedula.
    nombre: La columna nombre.
    apellido: La columna apellido.
	ciudad: La columna ciudad.
	estado: La columna estado.
    """

    seleccionar = TemplateColumn(template_code='<input name="id" type="radio" value="{{ record.id }}" />')
    id = LinkColumn('salvar_diagnostico_udm', verbose_name='N de solicitud de exámen', args=[A('id')])
    creacion_fecha = LinkDateTimeColumn('salvar_diagnostico_udm', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Solicitud de Exámen', args=[A('id')])
    paciente_id = LinkColumn('salvar_diagnostico_udm', verbose_name='Número de Historia', args=[A('id')])
    identificacion = LinkColumn('salvar_diagnostico_udm', verbose_name='C.I. / Pasaporte', args=[A('id')])
    nombre = LinkColumn('salvar_diagnostico_udm', verbose_name='Nombre', args=[A('id')])
    apellido = LinkColumn('salvar_diagnostico_udm', verbose_name='Apellido', args=[A('id')])
    ciudad = LinkColumn('salvar_diagnostico_udm', verbose_name='Ciudad', args=[A('id')])
    estado = LinkColumn('salvar_diagnostico_udm', verbose_name='Estado', args=[A('id')])
    medico_modificacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Modificación Médico', args=[A('id')])
    patologo_modificacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Modificación Patólogo', args=[A('id')])
    udm_modificacion_fecha = LinkDateTimeColumn('salvar_diagnostico_medico', '%d/%m/%y %H:%M:%S', verbose_name='Fecha de Modificación UDM', args=[A('id')])
    
    class Meta(object):
        """
        Clase meta de la clase DiagnosticoUdmTable.
        
        model: La clase modelo.
        attrs: Los atributos específicos de la tabla.
        fields: Los campos a mostrar.
        """

        attrs = { 'class': 'paleblue', 'width': '100%' }

class IndiceView(View):
    """
    Clase Vista que representa el índice.
    """

    @ConvitLoggerExceptionDecorator(logger=logger)
    def get(self, request, *args, **kwargs):
        """
        Método get que representa el índice. 
        
        Args:
            request: El objeto HTTP Request.
            
        Returns:
            El objeto HTTP Response.
        """


        if request.user.fecha_ult_reest_clave == None: # Si el usuario no tiene una fecha de ultima actualización de clave
            request.user.fecha_ult_reest_clave = date.today().strftime('%Y-%m-%d') # se le asigna la fecha del día en el que está ingresando

        if request.user.is_clave_caducable == None:
            request.user.is_clave_caducable = True

        formato_fecha = '%Y-%m-%d'

        fecha_actual = date.today().strftime(formato_fecha) #fecha actual
        fecha_usuario = request.user.fecha_ult_reest_clave.strftime(formato_fecha) #fecha de la último cambio de contraseña
        fecha_fin_convenio = request.user.unidad_fecha_fin.strftime(formato_fecha)

        # se necesitan estas conversiones para realizar operaciones con fecha
        fecha_actual = datetime.strptime(fecha_actual, formato_fecha)
        fecha_usuario = datetime.strptime(fecha_usuario, formato_fecha)
        fecha_fin_convenio = datetime.strptime( fecha_fin_convenio, formato_fecha)
        diferencia_dias = int((fecha_actual - fecha_usuario).days)

        if (diferencia_dias >= 90 and request.user.is_clave_caducable == True or  fecha_fin_convenio > fecha_actual ): #Se verifica que el usuario no tenga la clave vencida
            return HttpResponseRedirect(
                settings.URL_PREFIX + '/reestablecer_clave?mensaje= Clave Vencida, debe reestablecer su contraseña. Para reestablecerla ingrese su usuario')
        else:
            if request.user.has_perms(( 'unidaddiagnosticomolecular.diagnostico_medico', )):
            	return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda')
        	elif request.user.has_perms(( 'unidaddiagnosticomolecular.diagnostico_patologo', )):
            	return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda')
        	elif request.user.has_perms(( 'unidaddiagnosticomolecular.diagnostico_udm', )):
            	return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda')
            else:
                return HttpResponseRedirect(settings.URL_PREFIX + '/login')




class BusquedaDiagnosticoMedicoView(View):
    """
    Clase Vista que permite consultar diagnósticos de pacientes.
    
    template_name: Nombre de la plantilla.
    """
    
    template_name = 'busqueda_diagnostico_medico.html'

    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_medico', logger=logger)
    def get(self, request, *args, **kwargs):
        """
        Método get que consultar diagnósticos de clientes. 
        
        Args:
            request: El objeto HTTP Request.
            
        Returns:
            El objeto HTTP Response.
        """
        
        busqueda = request.GET.get('busqueda', '')
        if busqueda == '':
            diagnosticos = Diagnostico.objects.all()
        else:
            diagnosticos = Diagnostico.objects.filter(Q(paciente__identificacion__contains=busqueda) | Q(paciente__nombre_primero__contains=busqueda) | Q(paciente__nombre_segundo__contains=busqueda) | Q(paciente__apellido_primero__contains=busqueda) | Q(paciente__apellido_segundo__contains=busqueda))
        data = []
        for diagnostico in diagnosticos:
            data.append({ 'id': diagnostico.id, 'paciente_id': diagnostico.paciente.id, 'identificacion': diagnostico.paciente.tipo_identificacion + diagnostico.paciente.identificacion if diagnostico.paciente.tipo_identificacion else '', 'nombre': (diagnostico.paciente.nombre_primero if diagnostico.paciente.nombre_primero else '') + u' ' + (diagnostico.paciente.nombre_segundo if diagnostico.paciente.nombre_segundo else ''), 'apellido': (diagnostico.paciente.apellido_primero if diagnostico.paciente.apellido_primero else '') + u' ' + (diagnostico.paciente.apellido_segundo if diagnostico.paciente.apellido_segundo else ''), 'ciudad': diagnostico.paciente.ciudad.nombre, 'estado': diagnostico.paciente.ciudad.estado.nombre, 'creacion_fecha': diagnostico.creacion_fecha, 'medico_modificacion_fecha': diagnostico.medico_modificacion_fecha, 'patologo_modificacion_fecha': diagnostico.patologo_modificacion_fecha, 'udm_modificacion_fecha': diagnostico.udm_modificacion_fecha })
        tabla = DiagnosticoMedicoTable(data)
        RequestConfig(request, paginate={ 'per_page': 5 }).configure(tabla)
        
        return render(request, self.template_name, { 'tabla': tabla })
		
class BusquedaDiagnosticoPatologoView(View):
    """
    Clase Vista que permite consultar diagnósticos de pacientes.
    
    template_name: Nombre de la plantilla.
    """
    
    template_name = 'busqueda_diagnostico_patologo.html'

    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_patologo', logger=logger)
    def get(self, request, *args, **kwargs):
        """
        Método get que consultar diagnósticos de clientes. 
        
        Args:
            request: El objeto HTTP Request.
            
        Returns:
            El objeto HTTP Response.
        """
        
        busqueda = request.GET.get('busqueda', '')
        if busqueda == '':
            diagnosticos = Diagnostico.objects.all()
        else:
            diagnosticos = Diagnostico.objects.filter(Q(paciente__identificacion__contains=busqueda) | Q(paciente__nombre__contains=busqueda) | Q(paciente__apellido__contains=busqueda))
        data = []
        for diagnostico in diagnosticos:
            data.append({ 'id': diagnostico.id, 'paciente_id': diagnostico.paciente.id, 'identificacion': diagnostico.paciente.tipo_identificacion + diagnostico.paciente.identificacion if diagnostico.paciente.tipo_identificacion else '', 'nombre': (diagnostico.paciente.nombre_primero if diagnostico.paciente.nombre_primero else '') + u' ' + (diagnostico.paciente.nombre_segundo if diagnostico.paciente.nombre_segundo else ''), 'apellido': (diagnostico.paciente.apellido_primero if diagnostico.paciente.apellido_primero else '') + u' ' + (diagnostico.paciente.apellido_segundo if diagnostico.paciente.apellido_segundo else ''), 'ciudad': diagnostico.paciente.ciudad.nombre, 'estado': diagnostico.paciente.ciudad.estado.nombre, 'creacion_fecha': diagnostico.creacion_fecha, 'medico_modificacion_fecha': diagnostico.medico_modificacion_fecha, 'patologo_modificacion_fecha': diagnostico.patologo_modificacion_fecha, 'udm_modificacion_fecha': diagnostico.udm_modificacion_fecha })
        tabla = DiagnosticoPatologoTable(data)
        RequestConfig(request, paginate={ 'per_page': 5 }).configure(tabla)
        
        return render(request, self.template_name, { 'tabla': tabla })
       
class BusquedaDiagnosticoUdmView(View):
    """
    Clase Vista que permite consultar diagnósticos de pacientes.
    
    template_name: Nombre de la plantilla.
    """
    
    template_name = 'busqueda_diagnostico_udm.html'

    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_udm', logger=logger)
    def get(self, request, *args, **kwargs):
        """
        Método get que consultar diagnósticos de clientes. 
        
        Args:
            request: El objeto HTTP Request.
            
        Returns:
            El objeto HTTP Response.
        """
        
        busqueda = request.GET.get('busqueda', '')
        if busqueda == '':
            diagnosticos = Diagnostico.objects.all()
        else:
            diagnosticos = Diagnostico.objects.filter(Q(paciente__identificacion__contains=busqueda) | Q(paciente__nombre_primero__contains=busqueda) | Q(paciente__nombre_segundo__contains=busqueda) | Q(paciente__apellido_primero__contains=busqueda) | Q(paciente__apellido_segundo__contains=busqueda))
        data = []
        for diagnostico in diagnosticos:
            data.append({ 'id': diagnostico.id, 'paciente_id': diagnostico.paciente.id, 'identificacion': diagnostico.paciente.tipo_identificacion + diagnostico.paciente.identificacion if diagnostico.paciente.tipo_identificacion else '', 'nombre': (diagnostico.paciente.nombre_primero if diagnostico.paciente.nombre_primero else '') + u' ' + (diagnostico.paciente.nombre_segundo if diagnostico.paciente.nombre_segundo else ''), 'apellido': (diagnostico.paciente.apellido_primero if diagnostico.paciente.apellido_primero else '') + u' ' + (diagnostico.paciente.apellido_segundo if diagnostico.paciente.apellido_segundo else ''), 'ciudad': diagnostico.paciente.ciudad.nombre, 'estado': diagnostico.paciente.ciudad.estado.nombre, 'creacion_fecha': diagnostico.creacion_fecha, 'medico_modificacion_fecha': diagnostico.medico_modificacion_fecha, 'patologo_modificacion_fecha': diagnostico.patologo_modificacion_fecha, 'udm_modificacion_fecha': diagnostico.udm_modificacion_fecha })
        tabla = DiagnosticoUdmTable(data)
        RequestConfig(request, paginate={ 'per_page': 5 }).configure(tabla)
        
        return render(request, self.template_name, { 'tabla': tabla })
		
class SalvarDiagnoticoMedicoView(View):
    """
    Clase Vista que salva un diagnóstico.
    
    template_name: Nombre de la plantilla.
    """

    template_name = 'salvar_diagnostico_medico.html'

#    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_medico', logger=logger)
    def get(self, request, pk, *args, **kwargs):
        """
        Método get que crea o consulta un diagnóstico.
        
        Args:
            request: El objeto HTTP Request.
            pk: El identificador.
            
        Returns:
            El objeto HTTP Response.
        """

        if len(request.GET.items()) > 0:
            diagnostico_forma = DiagnosticoMedicoForm(request.GET)
            examenes_forma_set = DiagnosticoExamenFormSet(request.GET, prefix='examenes')
            estudios_forma_set = DiagnosticoEstudioFormSet(request.GET, prefix='estudios')			
            antecedentes_forma_set = DiagnosticoAntecedenteFormSet(request.GET, prefix='antecedentes')
            traslados_muestras_forma_set = DiagnosticoTrasladoMuestraFormSet(request.GET, prefix='traslados_muestras')
            if request.GET.get('boton_buscar') == 'Buscar paciente registrado':
                try:
                    paciente = Paciente.objects.get(tipo_identificacion=request.GET.get('tipo_identificacion'), identificacion=request.GET.get('identificacion'))
                    paciente_forma = PacienteForm(instance=paciente)
                    id_estado = paciente.ciudad.estado.id
                    id_ciudad = paciente.ciudad.id
                except Paciente.DoesNotExist:
                    paciente = Paciente()
                    paciente_forma = PacienteForm(request.GET)
                    paciente_forma.add_error(None, 'No se consigue el paciente')
                    id_estado = int(request.GET.get('id_estado', '0'))
                    id_ciudad = int(request.GET.get('id_ciudad', '0'))
            else:
                paciente = Paciente()
                paciente_forma = PacienteForm(request.GET)
                id_estado = int(request.GET.get('id_estado', '0'))
                id_ciudad = int(request.GET.get('id_ciudad', '0'))
        elif not pk:
            paciente = Paciente()
            diagnostico_forma = DiagnosticoMedicoForm()
            paciente_forma = PacienteForm()
            examenes = []
            orden = 0
            for tipo_examen in TipoExamen.objects.all():
                examenes.append({ 'tipo_examen': tipo_examen, 'nombre': tipo_examen.nombre, 'tipo': tipo_examen.tipo, 'orden': orden })				
                orden = orden + 1
            examenes_forma_set = modelformset_factory(DiagnosticoExamen, form=DiagnosticoExamenForm, extra=len(examenes))(prefix='examenes', queryset=DiagnosticoExamen.objects.none(), initial=examenes)
            estudios = []
            orden = 0
            for tipo_estudio in TipoEstudio.objects.all():
                estudios.append({ 'tipo_estudio': tipo_estudio, 'nombre': tipo_estudio.nombre, 'orden': orden })				
                orden = orden + 1
            estudios_forma_set = modelformset_factory(DiagnosticoEstudio, form=DiagnosticoEstudioForm, extra=len(estudios))(prefix='estudios', queryset=DiagnosticoEstudio.objects.none(), initial=estudios)
            antecedentes = []
            orden = 0
            for tipo_antecedente in TipoAntecedente.objects.all():
                antecedentes.append({ 'presente': None, 'otro': False, 'tipo_antecedente': tipo_antecedente, 'antecedente': tipo_antecedente.nombre, 'orden': orden })				
                orden = orden + 1
            antecedentes.append({ 'presente': None, 'otro': True, 'orden': orden })				
            antecedentes_forma_set = modelformset_factory(DiagnosticoAntecedente, form=DiagnosticoAntecedenteForm, extra=len(antecedentes))(prefix='antecedentes', queryset=DiagnosticoAntecedente.objects.none(), initial=antecedentes)
            traslados_muestras_forma_set = DiagnosticoTrasladoMuestraFormSet(prefix='traslados_muestras', queryset=DiagnosticoTrasladoMuestra.objects.none())
            id_estado = 0
            id_ciudad = 0
        else:
            diagnostico = Diagnostico.objects.get(id=pk)
            paciente = diagnostico.paciente
            id_estado = paciente.ciudad.estado.id
            id_ciudad = paciente.ciudad.id
            diagnostico_forma = DiagnosticoMedicoForm(instance=diagnostico)
            paciente_forma = PacienteForm(instance=paciente)
            examenes_forma_set = DiagnosticoExamenFormSet(prefix='examenes', queryset=DiagnosticoExamen.objects.filter(diagnostico__id=pk).order_by('orden'))
            estudios_forma_set = DiagnosticoEstudioFormSet(prefix='estudios', queryset=DiagnosticoEstudio.objects.filter(diagnostico__id=pk).order_by('orden'))
            antecedentes_forma_set = DiagnosticoAntecedenteFormSet(prefix='antecedentes', queryset=DiagnosticoAntecedente.objects.filter(diagnostico__id=pk).order_by('orden'))
            traslados_muestras_forma_set = DiagnosticoTrasladoMuestraFormSet(prefix='traslados_muestras', queryset=DiagnosticoTrasladoMuestra.objects.filter(diagnostico__id=pk).order_by('orden'))

        return render(request, self.template_name, { 'diagnostico_forma': diagnostico_forma, 'paciente_forma': paciente_forma, 'examenes_forma_set': examenes_forma_set, 'estudios_forma_set': estudios_forma_set, 'antecedentes_forma_set': antecedentes_forma_set, 'traslados_muestras_forma_set': traslados_muestras_forma_set, 'medico_user_forma': UDMUserForm(instance=request.user, prefix='medico'), 'estados': Estado.objects.all().order_by('nombre'), 'ciudades': Ciudad.objects.filter(estado_id=id_estado).order_by('nombre'), 'id_estado': id_estado, 'id_ciudad': id_ciudad, 'pk': pk, 'paciente_pk': (paciente.id if paciente.id else '') })

#    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_medico', logger=logger)
    def post(self, request, pk, *args, **kwargs):
        """
        Método post que salva un diagnóstico.
        
        Args:
            request: El objeto HTTP Request.
            pk: El identificador.
            
        Returns:
            El objeto HTTP Response.
        """

        id_estado = int(request.POST.get('id_estado', '0'))
        id_ciudad = int(request.POST.get('id_ciudad', '0'))	
        ciudad = Ciudad.objects.get(id=id_ciudad)

        try:
            paciente = Paciente.objects.get(tipo_identificacion=request.POST.get('tipo_identificacion'), identificacion=request.POST.get('identificacion'))
        except Paciente.DoesNotExist:
            paciente = Paciente()
        paciente.ciudad = ciudad
        paciente_forma = PacienteForm(request.POST, instance=paciente)
        diagnostico_forma = DiagnosticoMedicoForm(request.POST)
        examenes_forma_set = DiagnosticoExamenFormSet(request.POST, prefix='examenes')
        estudios_forma_set = DiagnosticoEstudioFormSet(request.POST, request.FILES, prefix='estudios')
        antecedentes_forma_set = DiagnosticoAntecedenteFormSet(request.POST, prefix='antecedentes')
        traslados_muestras_forma_set = DiagnosticoTrasladoMuestraFormSet(request.POST, request.FILES, prefix='traslados_muestras')


        if paciente_forma.is_valid() and diagnostico_forma.is_valid() and examenes_forma_set.is_valid() and antecedentes_forma_set.is_valid() and estudios_forma_set.is_valid() and traslados_muestras_forma_set.is_valid():
            paciente = paciente_forma.save()

            fecha = datetime.now()

            if pk:
                diagnostico = Diagnostico.objects.get(id=pk)
                diagnostico.medico_modificacion_fecha = fecha
                diagnostico.medico_modificacion_usuario = request.user
            else:
                diagnostico = Diagnostico()
                diagnostico.creacion_fecha = fecha
                diagnostico.creacion_usuario = request.user
                diagnostico.medico_modificacion_fecha = fecha
                diagnostico.medico_modificacion_usuario = request.user
            diagnostico.paciente = paciente
            diagnostico_forma = DiagnosticoMedicoForm(request.POST, instance=diagnostico)

            diagnostico = diagnostico_forma.save()
			
            examenes = examenes_forma_set.save()
            if pk:
                indice = DiagnosticoExamen.objects.filter(diagnostico__id=pk).count() + 1
            else:
                indice = 1
            for examen in examenes:
                examen.diagnostico = diagnostico
                if not examen.orden:
                    examen.orden = indice
                    indice = indice + 1
                examen.save()

            estudios = estudios_forma_set.save()
            if pk:
                indice = DiagnosticoEstudio.objects.filter(diagnostico__id=pk).count() + 1
            else:
                indice = 1
            for estudio in estudios:
                estudio.diagnostico = diagnostico
                if not estudio.orden:
                    estudio.orden = indice
                    indice = indice + 1
                estudio.save()
            for estudio in estudios_forma_set.deleted_objects:
                ruta = str(estudio.ruta)
                if ruta:
                    os.remove(os.path.join(settings.MEDIA_ROOT, ruta))

            antecedentes = antecedentes_forma_set.save()
            for antecedente in antecedentes:
                antecedente.diagnostico = diagnostico
                antecedente.save()

            traslados_muestras = traslados_muestras_forma_set.save()
            if pk:
                indice = DiagnosticoTrasladoMuestra.objects.filter(diagnostico__id=pk).count() + 1
            else:
                indice = 1
            for traslado_muestra in traslados_muestras:
                traslado_muestra.diagnostico = diagnostico
                if not traslado_muestra.orden:
                    traslado_muestra.orden = indice
                    indice = indice + 1
                traslado_muestra.save()
            for traslado_muestra in traslados_muestras_forma_set.deleted_objects:
                ruta = str(traslado_muestra.ruta)
                if ruta:
                    os.remove(os.path.join(settings.MEDIA_ROOT, ruta))
				
            self.enviar_correo(diagnostico)
			
            if not pk:
                return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda_diagnostico_medico?mensaje=Se creó un nuevo diagnóstico con número de historia ' + str(paciente.id))
            else:
                return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda_diagnostico_medico')
        else:
            diagnostico_forma = DiagnosticoMedicoForm(request.POST)
			
        return render(request, self.template_name, { 'diagnostico_forma': diagnostico_forma, 'paciente_forma': paciente_forma, 'examenes_forma_set': examenes_forma_set, 'estudios_forma_set': estudios_forma_set, 'antecedentes_forma_set': antecedentes_forma_set, 'traslados_muestras_forma_set': traslados_muestras_forma_set, 'medico_user_forma': UDMUserForm(instance=request.user, prefix='medico'), 'estados': Estado.objects.all().order_by('nombre'), 'ciudades': Ciudad.objects.filter(estado_id=id_estado).order_by('nombre'), 'id_estado': id_estado, 'id_ciudad': id_ciudad, 'pk': pk, 'paciente_pk': (paciente.id if paciente.id else '') })
		
    def enviar_correo(self, diagnostico):
        contenido  = u'<html><body><table border="0" width="100%"><tr><td align="left"><img src="http://nestorjb.ddns.net/static/img/logo-j.png" width="79" height="60"/></td><td align="right"><img src="http://nestorjb.ddns.net/static/img/logo-j.jpg" width="60" height="60"/></td></tr></table><p align="center"><b>SOLICITUD DE SERVICIO A LA UNIDAD DE DIAGNÓSTICO MOLECULAR</b></p><p>&nbsp;</p><p>Paciente (a) '
        contenido += diagnostico.paciente.nombre_primero if diagnostico.paciente.nombre_primero else '' + u' ' + diagnostico.paciente.nombre_segundo if diagnostico.paciente.nombre_segundo else ''
        contenido += u' '
        contenido += diagnostico.paciente.apellido_primero if diagnostico.paciente.apellido_primero else '' + u' ' + diagnostico.paciente.apellido_segundo if diagnostico.paciente.apellido_segundo else ''    
        contenido += u', C.I. '
        contenido += diagnostico.paciente.tipo_identificacion + diagnostico.paciente.identificacion if diagnostico.paciente.identificacion else u''
        contenido += u' EDAD '
        contenido += unicode(diagnostico.paciente.edad_anios)
        contenido += u' años '
        contenido += unicode(diagnostico.paciente.edad_meses)
        contenido += u' meses</p><p>Fecha de nacimiento '
        contenido += diagnostico.paciente.fecha_nacimiento.strftime('%d/%m/%Y') if diagnostico.paciente.fecha_nacimiento else ''
        contenido += u'. Número de Historia externa '
        contenido += diagnostico.paciente.numero_historia if diagnostico.paciente.numero_historia else ''
        contenido += u'</p><p>Nombre del representante: '
        contenido += diagnostico.paciente.represent_nombre_primero if diagnostico.paciente.represent_nombre_primero else '' + u' ' + diagnostico.paciente.represent_nombre_segundo if diagnostico.paciente.represent_nombre_segundo else ''
        contenido += u' '
        contenido += diagnostico.paciente.represent_apellido_primero if diagnostico.paciente.represent_apellido_primero else '' + u' ' + diagnostico.paciente.represent_apellido_segundo if diagnostico.paciente.represent_apellido_segundo else ''       
        contenido += u', C.I. '
        contenido += diagnostico.paciente.represent_tipo_identificacion + diagnostico.paciente.represent_identificacion if diagnostico.paciente.represent_identificacion else u''
        contenido += u'</p><p>Fecha: '
        contenido += date.today().strftime('%d/%m/%Y')
        contenido += u'</p><p>FAVOR REALIZAR LOS SIGUIENTES SERVICIOS:</p><table border="0" width="100%"><tr><td valign="top"><table border="0" width="100%"><tr><td colspan="2">TIPO DE MUESTRA:</td></tr><tr><td colspan="2">Seleccione el tipo de muestra que requiere ser analizada.</td></tr><tr><td colspan="2">&nbsp;</td></tr>'
        for tipo_muestra in ( u'Sangre', u'Tejido Fresco', u'Tejido en Parafina', u'Tejido en Formaldehido', u'Esputo', u'Lavado Gástrico', u'Heces', u'Orina', u'Líquido Cefalorraquídeo', u'Hisopados Faringeos', u'Mucosas', u'Otros' ):
            contenido += u'<tr><td><input type="checkbox" readonly="readonly" '
            if diagnostico.udm_tipo_muestra == tipo_muestra:
                contenido += u' checked="checked"'
            contenido += u'/></td><td>'
            contenido += tipo_muestra
            if tipo_muestra in ( u'Tejido Fresco', u'Tejido en Parafina', u'Tejido en Formaldehido' ):
                contenido += u' Tipo: '
                if diagnostico.udm_tipo_muestra == tipo_muestra:
                    contenido += diagnostico.udm_tipo_muestra_otro
            contenido += u'</td></tr>'
			
        contenido += u'</table></td><td valign="top"><table border="0"><tr><td colspan="2">EXÁMEN A REALIZAR:</td></tr><tr><td colspan="2">Seleccione el exámen a realizar.</td></tr><tr><td colspan="2">&nbsp;</td></tr>'
		
        examenes = DiagnosticoExamen.objects.filter(diagnostico__id=diagnostico.id)
        for examen in examenes:
            contenido += u'<tr><td><input type="checkbox" readonly="readonly" '
            if examen.presente:
                contenido += u' checked="checked"'
            contenido += u'/></td><td>'
            contenido += examen.nombre
            contenido += u'</td></tr>'
			
        contenido += u'</table></td></tr></table><p>Autorizado por: '
        contenido += diagnostico.medico_modificacion_usuario.first_name + ' ' + diagnostico.medico_modificacion_usuario.last_name
        contenido += u'</p><p>Firma y Sello: </p><p>Recibido por UDM:</p><p>Fecha y Hora:</p></body></html>'
		
        mensaje = MIMEMultipart('alternative')
        mensaje.set_charset('utf8')
        mensaje['From'] = settings.EMAIL_SERVER_USERNAME
        mensaje['To'] = 'udm@jacintoconvit.org'
        if diagnostico.medico_modificacion_fecha == diagnostico.creacion_fecha:
            mensaje['Subject'] = u'Diagnóstico nuevo para paciente ' + diagnostico.paciente.nombre_primero if diagnostico.paciente.nombre_primero else '' + u' ' + diagnostico.paciente.nombre_segundo if diagnostico.paciente.nombre_segundo else '' + u' ' + diagnostico.paciente.apellido_primero if diagnostico.paciente.apellido_primero else '' + u' ' + diagnostico.paciente.apellido_segundo if diagnostico.paciente.apellido_segundo else ''
        else:
            mensaje['Subject'] = u'Diagnóstico modificado para paciente ' + diagnostico.paciente.nombre_primero if diagnostico.paciente.nombre_primero else '' + u' ' + diagnostico.paciente.nombre_segundo if diagnostico.paciente.nombre_segundo else '' + u' ' + diagnostico.paciente.apellido_primero if diagnostico.paciente.apellido_primero else '' + u' ' + diagnostico.paciente.apellido_segundo if diagnostico.paciente.apellido_segundo else ''
        mensaje.attach(MIMEText(contenido, 'html', 'utf8'))

        server = smtplib.SMTP(settings.EMAIL_SERVER_URL)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_SERVER_USERNAME, settings.EMAIL_SERVER_PASSWORD)
        server.sendmail(settings.EMAIL_SERVER_USERNAME, 'udm@jacintoconvit.org', mensaje.as_string())
        server.quit()
		
class SalvarDiagnoticoPatologoView(View):
    """
    Clase Vista que salva un diagnóstico.
    
    template_name: Nombre de la plantilla.
    """

    template_name = 'salvar_diagnostico_patologo.html'

    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_patologo', logger=logger)
    def get(self, request, pk, *args, **kwargs):
        """
        Método get que crea o consulta un diagnóstico.
        
        Args:
            request: El objeto HTTP Request.
            pk: El identificador.
            
        Returns:
            El objeto HTTP Response.
        """

        diagnostico = Diagnostico.objects.get(id=pk)
        paciente = diagnostico.paciente
        diagnostico_forma = DiagnosticoPatologoForm(instance=diagnostico)
        paciente_forma = PacienteMostrarForm(instance=paciente)
        estudios_forma_set = DiagnosticoEstudioFormSet(queryset=DiagnosticoEstudio.objects.filter(diagnostico__id=pk).order_by('orden'))
			
        return render(request, self.template_name, { 'diagnostico_forma': diagnostico_forma, 'paciente_forma': paciente_forma, 'estudios_forma_set': estudios_forma_set, 'medico_user_forma': UDMUserForm(instance=diagnostico.creacion_usuario, prefix='medico'), 'patologo_user_forma': UDMUserForm(instance=request.user, prefix='patologo'), 'pk': pk, 'paciente_pk': paciente.id })

    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_patologo', logger=logger)
    def post(self, request, pk, *args, **kwargs):
        """
        Método post que salva un diagnóstico.
        
        Args:
            request: El objeto HTTP Request.
            pk: El identificador.
            
        Returns:
            El objeto HTTP Response.
        """

        diagnostico = Diagnostico.objects.get(id=pk)
        paciente = diagnostico.paciente
        diagnostico.patologo_modificacion_fecha = datetime.now()
        diagnostico.patologo_modificacion_usuario = request.user
        diagnostico_forma = DiagnosticoPatologoForm(request.POST, instance=diagnostico)
        paciente_forma = PacienteMostrarForm(request.POST, instance=paciente)
        estudios_forma_set = DiagnosticoEstudioFormSet(request.POST, request.FILES, queryset=DiagnosticoEstudio.objects.filter(diagnostico__id=pk).order_by('orden'))
			
        if diagnostico_forma.is_valid() and estudios_forma_set.is_valid():
            diagnostico = diagnostico_forma.save()
			
            indice = DiagnosticoEstudio.objects.filter(diagnostico__id=pk).count() + 1
            estudios = estudios_forma_set.save()
            for estudio in estudios:
                estudio.diagnostico = diagnostico
                if not estudio.orden:
                    estudio.orden = indice
                    indice = indice + 1
                estudio.save()
            for estudio in estudios_forma_set.deleted_objects:
                ruta = str(estudio.ruta)
                if ruta:
                    os.remove(os.path.join(settings.MEDIA_ROOT, ruta))
            return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda_diagnostico_patologo')

        return render(request, self.template_name, { 'diagnostico_forma': diagnostico_forma, 'paciente_forma': paciente_forma, 'estudios_forma_set': estudios_forma_set, 'medico_user_forma': UDMUserForm(instance=diagnostico.creacion_usuario, prefix='medico'), 'patologo_user_forma': UDMUserForm(instance=request.user, prefix='patologo'), 'pk': pk, 'paciente_pk': paciente.id })
		
class SalvarDiagnoticoUdmView(View):
    """
    Clase Vista que salva un diagnóstico.
    
    template_name: Nombre de la plantilla.
    """

    template_name = 'salvar_diagnostico_udm.html'

    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_udm', logger=logger)
    def get(self, request, pk, *args, **kwargs):
        """
        Método get que crea o consulta un diagnóstico.
        
        Args:
            request: El objeto HTTP Request.
            pk: El identificador.
            
        Returns:
            El objeto HTTP Response.
        """

        diagnostico = Diagnostico.objects.get(id=pk)
        paciente = diagnostico.paciente
        diagnostico_forma = DiagnosticoUDMForm(instance=diagnostico)
        paciente_forma = PacienteMostrarForm(instance=paciente)
        examenes_forma_set = DiagnosticoExamenFormSet(prefix='examenes', queryset=DiagnosticoExamen.objects.filter(Q(diagnostico__id=pk) & Q(presente=True)).order_by('orden'))
			
        return render(request, self.template_name, { 'diagnostico_forma': diagnostico_forma, 'paciente_forma': paciente_forma, 'examenes_forma_set': examenes_forma_set, 'medico_user_forma': UDMUserForm(instance=diagnostico.creacion_usuario, prefix='medico'), 'udm_user_forma': UDMUserForm(instance=request.user, prefix='udm'), 'pk': pk, 'paciente_pk': paciente.id })

    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_udm', logger=logger)
    def post(self, request, pk, *args, **kwargs):
        """
        Método post que salva un diagnóstico.
        
        Args:
            request: El objeto HTTP Request.
            pk: El identificador.
            
        Returns:
            El objeto HTTP Response.
        """

        diagnostico = Diagnostico.objects.get(id=pk)
        diagnostico.udm_modificacion_fecha = datetime.now()
        diagnostico.udm_modificacion_usuario = request.user
        paciente = diagnostico.paciente
        diagnostico_forma = DiagnosticoUDMForm(request.POST, instance=diagnostico)
        paciente_forma = PacienteMostrarForm(instance=paciente)
        examenes_forma_set = DiagnosticoExamenFormSet(request.POST, prefix='examenes')

        if diagnostico_forma.is_valid() and examenes_forma_set.is_valid():
            diagnostico = diagnostico_forma.save()
            for examen_forma in examenes_forma_set:
                examen_forma.save()
            return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda_diagnostico_udm')

        return render(request, self.template_name, { 'diagnostico_forma': diagnostico_forma, 'paciente_forma': paciente_forma, 'examenes_forma_set': examenes_forma_set, 'medico_user_forma': UDMUserForm(instance=diagnostico.creacion_usuario, prefix='medico'), 'udm_user_forma': UDMUserForm(instance=request.user, prefix='udm'), 'pk': pk, 'paciente_pk': paciente.id })

class EliminarDiagnosticoView(View):
    """
    Clase Vista que elimina un diagnóstico.
    
    template_name: Nombre de la plantilla.
    """

    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_medico', logger=logger)
    def get(self, request, pk, *args, **kwargs):
        """
        Método post que salva un diagnóstico.
        
        Args:
            request: El objeto HTTP Request.
            pk: El identificador.
            
        Returns:
            El objeto HTTP Response.
        """

        DiagnosticoSintoma.objects.filter(diagnostico__id=pk).delete()
        DiagnosticoExamen.objects.filter(diagnostico__id=pk).delete()
        Diagnostico.objects.get(id=pk).delete()

        return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda_diagnostico_medico')

class GenerarReporteView(View):
    """
    Clase Vista que genera el reporte.
    """

    @ConvitLoggerExceptionDecorator(logger=logger)
    def get(self, request, pk, *args, **kwargs):
        """
        Método get que crea o consulta un diagnóstico.
        
        Args:
            request: El objeto HTTP Request.
            pk: El identificador.
            
        Returns:
            El objeto HTTP Response.
        """

        diagnostico = Diagnostico.objects.get(id=pk)
        examenes = DiagnosticoExamen.objects.filter(diagnostico__id=pk).order_by('orden')
        examenes_texto = ''
        indice = 0
        for examen in examenes:
            if examen.presente:
                if indice > 0:
                    examenes_texto += ', '
                examenes_texto += examen.nombre + (('(' + examen.tipo + ')') if examen.tipo else '')
                indice = indice + 1
		
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Reporte de Diagnóstico ' + str(diagnostico.id) + '.pdf"'

        style1 = ParagraphStyle(name='style1', alignment=TA_CENTER, fontName='Helvetica-BoldOblique', fontSize=11)
        style2 = ParagraphStyle(name='style2', alignment=TA_JUSTIFY, fontName='Helvetica', fontSize=11)
        style3 = ParagraphStyle(name='style3', alignment=TA_CENTER, fontName='Helvetica', fontSize=11)
        style4 = ParagraphStyle(name='style4', alignment=TA_RIGHT, fontName='Helvetica', fontSize=11)
        style5 = ParagraphStyle(name='style5', alignment=TA_CENTER, fontName='Helvetica', fontSize=8)

        inicioLinea = 700
        espacioLinea = 15
		
        c = canvas.Canvas(response, pagesize=letter)
        c.drawImage(settings.STATICFILES_DIRS[0] + 'img/logo-j.png', 60, 710, width=79, height=60)
        c.drawImage(settings.STATICFILES_DIRS[0] + 'img/logo-j.jpg', 500, 710, width=60, height=60)
        c.drawImage(settings.STATICFILES_DIRS[0] + 'img/sello.jpg', 450, 60, width=105, height=31)
		
        p = Paragraph(u'Resultado Unidad de Diagnóstico Molecular', style1)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - p.height)

        p = Paragraph(str(diagnostico.paciente.id), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 2 * espacioLinea - p.height)

        p = Paragraph(str(diagnostico.paciente.numero_historia if diagnostico.paciente.numero_historia else ''), style4)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 2 * espacioLinea - p.height)

        p = Paragraph(u'Fecha de Emisión de Resultados: ' + date.today().strftime('%d/%m/%Y'), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 3 * espacioLinea - p.height)
		
        p = Paragraph(u'Nombres y Apellidos (Paciente): ' + (diagnostico.paciente.nombre_primero if diagnostico.paciente.nombre_primero else '') + u' ' + (diagnostico.paciente.nombre_segundo if diagnostico.paciente.nombre_segundo else '') + u' ' + (diagnostico.paciente.apellido_primero if diagnostico.paciente.apellido_primero else '') + u' ' + (diagnostico.paciente.apellido_segundo if diagnostico.paciente.apellido_segundo else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 4 * espacioLinea - p.height)

        p = Paragraph(u'CI / Pasaporte No: ' + (diagnostico.paciente.tipo_identificacion + diagnostico.paciente.identificacion if diagnostico.paciente.tipo_identificacion else '') + u' &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Edad: ' + (unicode(diagnostico.paciente.edad_anios) + u' años ' + unicode(diagnostico.paciente.edad_meses) + u' meses' if diagnostico.paciente.edad_anios else '') + u' &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sexo: ' + (diagnostico.paciente.sexo if diagnostico.paciente.sexo else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 5 * espacioLinea - p.height)

        p = Paragraph(u'Nombres y Apellidos (Representante Legal): ' + diagnostico.paciente.represent_nombre + ' ' + diagnostico.paciente.represent_apellido, style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 6 * espacioLinea - p.height)
		
        p = Paragraph(u'CI / Pasaporte No: ' + (diagnostico.paciente.represent_tipo_identificacion + diagnostico.paciente.represent_identificacion if diagnostico.paciente.represent_tipo_identificacion else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 7 * espacioLinea - p.height)
		
        p = Paragraph(u'Tipo de Muestra: ' + (diagnostico.udm_tipo_muestra if diagnostico.udm_tipo_muestra else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 9 * espacioLinea - p.height)

        p = Paragraph(u'Técnica Empleada en el Análisis: ' + (diagnostico.udm_tecnica_deteccion if diagnostico.udm_tecnica_deteccion else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 10 * espacioLinea - p.height)
		
        p = Paragraph(u'Resultado: ' + examenes_texto, style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 11 * espacioLinea - p.height)

        p = Paragraph(u'Observaciones: ' + (diagnostico.udm_observaciones if diagnostico.udm_observaciones else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 15 * espacioLinea - p.height)

        p = Paragraph(u'Médico Tratante: ' + ((diagnostico.creacion_usuario.first_name + ' ' + diagnostico.creacion_usuario.last_name) if diagnostico.creacion_usuario.first_name else '') + ' ' + (diagnostico.creacion_usuario.institucion.nombre if diagnostico.creacion_usuario.institucion else '') + ' ' + (diagnostico.creacion_usuario.unidad if diagnostico.creacion_usuario.unidad else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 17 * espacioLinea - p.height)

        p = Paragraph(u'Nombre del Representante de la Unidad: ' + (diagnostico.udm_modificacion_usuario.first_name + ' ' + diagnostico.udm_modificacion_usuario.last_name if diagnostico.udm_modificacion_usuario else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 18 * espacioLinea - p.height)

        p = Paragraph(u'Firma:', style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 19 * espacioLinea - p.height)

        if diagnostico.udm_modificacion_usuario != None and diagnostico.udm_modificacion_usuario.firma != None:
            c.drawImage(settings.STATICFILES_DIRS[0] + unicode(diagnostico.udm_modificacion_usuario.firma), 100, inicioLinea - 19 * espacioLinea - p.height - 24, width=51, height=38)
		
        p = Paragraph(u'Fundación Jacinto Convit | Rif. J-40111708-2 | www.jacintoconvit.org | <a href="mail:info@jacintoconvit.org">info@jacintoconvit.org</a>', style5)
        p.wrap(500, 15)
        p.drawOn(c, 60, 50 - p.height)

        c.showPage()
		
        inicioLinea = 715
		
        c.drawImage(settings.STATICFILES_DIRS[0] + 'img/logo-j.png', 60, 710, width=79, height=60)
        c.drawImage(settings.STATICFILES_DIRS[0] + 'img/logo-j.jpg', 500, 710, width=60, height=60)
        c.drawImage(settings.STATICFILES_DIRS[0] + 'img/sello.jpg', 450, 430, width=105, height=31)
		
        p = Paragraph(u'Resultado Unidad de Diagnóstico Molecular', style1)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - p.height)

        p = Paragraph(str(diagnostico.paciente.id), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - espacioLinea - p.height)

        p = Paragraph(str(diagnostico.paciente.numero_historia if diagnostico.paciente.numero_historia else ''), style4)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - espacioLinea - p.height)

        p = Paragraph(u'Fecha de Emisión de Resultados: ' + date.today().strftime('%d/%m/%Y'), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 2 * espacioLinea - p.height)
		
        p = Paragraph(u'Nombres y Apellidos (Paciente): ' + (diagnostico.paciente.nombre_primero if diagnostico.paciente.nombre_primero else '') + u' ' + (diagnostico.paciente.nombre_segundo if diagnostico.paciente.nombre_segundo else '') + u' ' + (diagnostico.paciente.apellido_primero if diagnostico.paciente.apellido_primero else '') + u' ' + (diagnostico.paciente.apellido_segundo if diagnostico.paciente.apellido_segundo else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 3 * espacioLinea - p.height)

        p = Paragraph(u'CI / Pasaporte No: ' + (diagnostico.paciente.tipo_identificacion + diagnostico.paciente.identificacion if diagnostico.paciente.tipo_identificacion else '') + u' &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Edad: ' + (unicode(diagnostico.paciente.edad_anios) + u' años ' + unicode(diagnostico.paciente.edad_meses) + u' meses' if diagnostico.paciente.edad_anios else '') + u' &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sexo: ' + (diagnostico.paciente.sexo if diagnostico.paciente.sexo else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 4 * espacioLinea - p.height)

        p = Paragraph(u'Nombres y Apellidos (Representante Legal): ' + diagnostico.paciente.represent_nombre + ' ' + diagnostico.paciente.represent_apellido, style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 5 * espacioLinea - p.height)
		
        p = Paragraph(u'CI / Pasaporte No: ' + (diagnostico.paciente.represent_tipo_identificacion + diagnostico.paciente.represent_identificacion if diagnostico.paciente.represent_tipo_identificacion else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 6 * espacioLinea - p.height)
		
        p = Paragraph(u'Tipo de Muestra: ' + (diagnostico.udm_tipo_muestra if diagnostico.udm_tipo_muestra else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 8 * espacioLinea - p.height)

        p = Paragraph(u'Técnica Empleada en el Análisis: ' + (diagnostico.udm_tecnica_deteccion if diagnostico.udm_tecnica_deteccion else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 9 * espacioLinea - p.height)
		
        p = Paragraph(u'Resultado: ' + examenes_texto, style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 10 * espacioLinea - p.height)

        p = Paragraph(u'Observaciones: ' + (diagnostico.udm_observaciones if diagnostico.udm_observaciones else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 13 * espacioLinea - p.height)

        p = Paragraph(u'Médico Tratante: ' + ((diagnostico.creacion_usuario.first_name + ' ' + diagnostico.creacion_usuario.last_name) if diagnostico.creacion_usuario.first_name else '') + ' ' + (diagnostico.creacion_usuario.institucion.nombre if diagnostico.creacion_usuario.institucion else '') + ' ' + (diagnostico.creacion_usuario.unidad if diagnostico.creacion_usuario.unidad else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 15 * espacioLinea - p.height)

        p = Paragraph(u'Nombre del Representante de la Unidad: ' + (diagnostico.udm_modificacion_usuario.first_name + ' ' + diagnostico.udm_modificacion_usuario.last_name if diagnostico.udm_modificacion_usuario else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 16 * espacioLinea - p.height)

        p = Paragraph(u'Firma:', style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 17 * espacioLinea - p.height)

        if diagnostico.udm_modificacion_usuario != None and diagnostico.udm_modificacion_usuario.firma != None:
            c.drawImage(settings.STATICFILES_DIRS[0] + unicode(diagnostico.udm_modificacion_usuario.firma), 100, inicioLinea - 17 * espacioLinea - p.height - 24, width=51, height=38)
		
        p = Paragraph(u'Fundación Jacinto Convit | Rif. J-40111708-2 | www.jacintoconvit.org | <a href="mail:info@jacintoconvit.org">info@jacintoconvit.org</a>', style5)
        p.wrap(500, 15)
        p.drawOn(c, 60, 420 - p.height)

        c.line(60, 407, 560, 407)
		
        c.drawImage(settings.STATICFILES_DIRS[0] + 'img/logo-j.png', 60, 340, width=79, height=60)
        c.drawImage(settings.STATICFILES_DIRS[0] + 'img/logo-j.jpg', 500, 340, width=60, height=60)
        c.drawImage(settings.STATICFILES_DIRS[0] + 'img/sello.jpg', 450, 60, width=105, height=31)
		
        p = Paragraph(u'Resultado Unidad de Diagnóstico Molecular', style1)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 25 * espacioLinea - p.height)

        p = Paragraph(str(diagnostico.paciente.id), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 26 * espacioLinea - p.height)

        p = Paragraph(str(diagnostico.paciente.numero_historia if diagnostico.paciente.numero_historia else ''), style4)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 26 * espacioLinea - p.height)

        p = Paragraph(u'Fecha de Emisión de Resultados: ' + date.today().strftime('%d/%m/%Y'), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 27 * espacioLinea - p.height)
		
        p = Paragraph(u'Nombres y Apellidos (Paciente): ' + (diagnostico.paciente.nombre_primero if diagnostico.paciente.nombre_primero else '') + u' ' + (diagnostico.paciente.nombre_segundo if diagnostico.paciente.nombre_segundo else '') + u' ' + (diagnostico.paciente.apellido_primero if diagnostico.paciente.apellido_primero else '') + u' ' + (diagnostico.paciente.apellido_segundo if diagnostico.paciente.apellido_segundo else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 28 * espacioLinea - p.height)

        p = Paragraph(u'CI / Pasaporte No: ' + (diagnostico.paciente.tipo_identificacion + diagnostico.paciente.identificacion if diagnostico.paciente.tipo_identificacion else '') + u' &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Edad: ' + (unicode(diagnostico.paciente.edad_anios) + u' años ' + unicode(diagnostico.paciente.edad_meses) + u' meses' if diagnostico.paciente.edad_anios else '') + u' &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sexo: ' + (diagnostico.paciente.sexo if diagnostico.paciente.sexo else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 29 * espacioLinea - p.height)

        p = Paragraph(u'Nombres y Apellidos (Representante Legal): ' + diagnostico.paciente.represent_nombre + ' ' + diagnostico.paciente.represent_apellido, style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 30 * espacioLinea - p.height)
		
        p = Paragraph(u'CI / Pasaporte No: ' + (diagnostico.paciente.represent_tipo_identificacion + diagnostico.paciente.represent_identificacion if diagnostico.paciente.represent_tipo_identificacion else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 31 * espacioLinea - p.height)
		
        p = Paragraph(u'Tipo de Muestra: ' + (diagnostico.udm_tipo_muestra if diagnostico.udm_tipo_muestra else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 33 * espacioLinea - p.height)

        p = Paragraph(u'Técnica Empleada en el Análisis: ' + (diagnostico.udm_tecnica_deteccion if diagnostico.udm_tecnica_deteccion else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 34 * espacioLinea - p.height)
		
        p = Paragraph(u'Resultado: ' + examenes_texto, style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 35 * espacioLinea - p.height)

        p = Paragraph(u'Observaciones: ' + (diagnostico.udm_observaciones if diagnostico.udm_observaciones else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 38 * espacioLinea - p.height)

        p = Paragraph(u'Médico Tratante: ' + ((diagnostico.creacion_usuario.first_name + ' ' + diagnostico.creacion_usuario.last_name) if diagnostico.creacion_usuario.first_name else '') + ' ' + (diagnostico.creacion_usuario.institucion.nombre if diagnostico.creacion_usuario.institucion else '') + ' ' + (diagnostico.creacion_usuario.unidad if diagnostico.creacion_usuario.unidad else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 40 * espacioLinea - p.height)

        p = Paragraph(u'Nombre del Representante de la Unidad: ' + (diagnostico.udm_modificacion_usuario.first_name + ' ' + diagnostico.udm_modificacion_usuario.last_name if diagnostico.udm_modificacion_usuario else ''), style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 41 * espacioLinea - p.height)

        p = Paragraph(u'Firma:', style2)
        p.wrap(500, 15)
        p.drawOn(c, 60, inicioLinea - 42 * espacioLinea - p.height)

        if diagnostico.udm_modificacion_usuario != None and diagnostico.udm_modificacion_usuario.firma != None:
            c.drawImage(settings.STATICFILES_DIRS[0] + unicode(diagnostico.udm_modificacion_usuario.firma), 100, inicioLinea - 42 * espacioLinea - p.height - 24, width=51, height=38)

        p = Paragraph(u'Fundación Jacinto Convit | Rif. J-40111708-2 | www.jacintoconvit.org | <a href="mail:info@jacintoconvit.org">info@jacintoconvit.org</a>', style5)
        p.wrap(500, 15)
        p.drawOn(c, 60, 50 - p.height)

        c.save()
			
        return response


class ventanaPacienteView(View):
    """
    Clase Vista que salva un paciente.


    template_name: Nombre de la plantilla.
    """

    template_name = 'ventana_paciente.html'

#    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_medico', logger=logger)
    def get(self, request, pk, *args, **kwargs):
        """
        Método get que crea o consulta un diagnóstico.

        Args:
            request: El objeto HTTP Request.
            pk: El identificador.

        Returns:
            El objeto HTTP Response.
        """

        if len(request.GET.items()) > 0:
            antecedentes_forma_set = DiagnosticoAntecedenteFormSet(request.GET, prefix='antecedentes')
            paciente = Paciente()
            paciente_forma = PacienteForm(request.GET)
            id_estado = int(request.GET.get('id_estado', '0'))
            id_ciudad = int(request.GET.get('id_ciudad', '0'))
            id_parroquia = int(request.GET.get('id_parroquia', '0'))
            id_municipio = int(request.GET.get('id_municipio', '0'))
        elif not pk:
            paciente = Paciente()
            paciente_forma = PacienteForm()
            antecedentes = []
            orden = 0
            for tipo_antecedente in TipoAntecedente.objects.all():
                antecedentes.append({ 'presente': None, 'otro': False, 'tipo_antecedente': tipo_antecedente, 'antecedente': tipo_antecedente.nombre, 'orden': orden })
                orden = orden + 1
            antecedentes.append({ 'presente': None, 'otro': True, 'orden': orden })
            antecedentes_forma_set = modelformset_factory(DiagnosticoAntecedente, form=DiagnosticoAntecedenteForm, extra=len(antecedentes))(prefix='antecedentes', queryset=DiagnosticoAntecedente.objects.none(), initial=antecedentes)
            id_estado = 0
            id_ciudad = 0
            id_parroquia = 0
            id_municipio = 0
        else:
            paciente = Paciente.objects.get(id=pk)
            id_estado = paciente.ciudad.estado.id
            id_ciudad = paciente.ciudad.id
            id_parroquia = paciente.parroquia.id
            id_municipio = paciente.parroquia.municipio.id
            paciente_forma = PacienteForm(instance=paciente)
            antecedentes_forma_set = DiagnosticoAntecedenteFormSet(prefix='antecedentes',
                                                                   queryset=DiagnosticoAntecedente.objects.filter(
                                                                       paciente__id=pk).order_by('orden'))

        return render(request, self.template_name,
                          {'paciente_forma': paciente_forma, 'antecedentes_forma_set': antecedentes_forma_set,
                           'medico_user_forma': UDMUserForm(instance=request.user, prefix='medico'),
                           'estados': Estado.objects.all().order_by('nombre'),
                           'ciudades': Ciudad.objects.filter(estado_id=id_estado).order_by('nombre'),
                           'municipios': Municipio.objects.filter(estado_id=id_estado).order_by('nombre'),
                           'parroquias': Parroquia.objects.filter(municipio_id=id_municipio).order_by('nombre'),
                           'id_estado': id_estado, 'id_ciudad': id_ciudad, 'id_municipio': id_municipio,
                           'id_parroquia': id_parroquia, 'pk': pk, 'paciente_pk': (paciente.id if paciente.id else '')})

#    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_medico', logger=logger)
    def post(self, request, pk, *args, **kwargs):
        """
        Método post que salva un paciente

        Args:
            request: El objeto HTTP Request.
            pk: El identificador.

        Returns:
            El objeto HTTP Response.
        """

        id_estado = int(request.POST.get('id_estado', '0'))
        id_ciudad = int(request.POST.get('id_ciudad', '0'))
        id_municipio = int(request.POST.get('id_municipio', '0'))
        id_parroquia = int(request.POST.get('id_parroquia', '0'))
        ciudad = Ciudad.objects.get(id=id_ciudad)
        parroquia = Parroquia.objects.get(id=id_parroquia)

        try:
            if (pk != ''):
                paciente = Paciente.objects.get(id=pk)
            else:
                paciente_pk = int(request.POST.get(pk, '0'))
                paciente = Paciente.objects.get(id=paciente_pk)
        except Paciente.DoesNotExist:
            paciente = Paciente()
        paciente.ciudad = ciudad
        paciente.parroquia = parroquia

        paciente_forma = PacienteForm(request.POST, instance=paciente)
        antecedentes_forma_set = DiagnosticoAntecedenteFormSet(request.POST, prefix='antecedentes')

        if paciente_forma.is_valid() and antecedentes_forma_set.is_valid():

            if pk:
                self.guardar_cambios(pk, request)
                paciente = Paciente.objects.get(id=pk)
            else:
                paciente = Paciente()

            paciente.ciudad = ciudad
            paciente.parroquia = parroquia
            paciente_forma = PacienteForm(request.POST, instance=paciente)
            paciente = paciente_forma.save()

            antecedentes = antecedentes_forma_set.save()
            for antecedente in antecedentes:
                antecedente.paciente = paciente
                antecedente.save()

            if not pk:
                return HttpResponseRedirect(
                    settings.URL_PREFIX + '/busqueda?mensaje=Se creó un nuevo diagnóstico con número de historia ' + str(
                        paciente.id))
            else:
                return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda')
        else:
            paciente_forma = PacienteForm(request.POST)

        return render(request, self.template_name, {'paciente_forma': paciente_forma, 'antecedentes_forma_set': antecedentes_forma_set,
                                                    'medico_user_forma': UDMUserForm(instance=request.user, prefix='medico'),
                                                    'estados': Estado.objects.all().order_by('nombre'),
                                                    'ciudades': Ciudad.objects.filter(estado_id=id_estado).order_by('nombre'),
                                                    'municipios': Municipio.objects.filter(estado_id=id_estado).order_by('nombre'),
                                                    'parroquias': Parroquia.objects.filter(municipio_id=id_municipio).order_by('nombre'),
                                                    'id_estado': id_estado, 'id_ciudad': id_ciudad, 'id_municipio': id_municipio,
                                                    'id_parroquia': id_parroquia, 'pk': pk, 'paciente_pk': (paciente.id if paciente.id else '')})

    def guardar_cambios(self, id_paciente_old,request):

        paciente_old = Paciente.objects.get(id=id_paciente_old)
        fecha = datetime.now()

        id_estado_civil = int(request.POST.get('estado_civil', '0'))
        estado_civil_new = EstadoCivil.objects.get(id=id_estado_civil)
        id_nivel_estudio = int(request.POST.get('nivel_estudio', '0'))
        nivel_estudio_new = NivelEstudio.objects.get(id=id_nivel_estudio)

        id_represent_estado_civil = int(request.POST.get('represent_estado_civil', '0'))
        if id_represent_estado_civil:
            represent_estado_civil_new = EstadoCivil.objects.get(id=id_represent_estado_civil)
        id_represent_nivel_estudio = int(request.POST.get('represent_nivel_estudio', '0'))
        if id_represent_nivel_estudio:
            represent_nivel_estudio_new = NivelEstudio.objects.get(id=id_represent_nivel_estudio)

        id_estado = int(request.POST.get('id_estado', '0'))
        estado_new = Estado.objects.get(id=id_estado)
        id_ciudad = int(request.POST.get('id_ciudad', '0'))
        ciudad_new = Ciudad.objects.get(id=id_ciudad)
        id_municipio = int(request.POST.get('id_municipio', '0'))
        municipio_new = Municipio.objects.get(id=id_municipio)
        id_parroquia = int(request.POST.get('id_parroquia', '0'))
        parroquia_new = Parroquia.objects.get(id=id_parroquia)

        if (request.POST.get('numero_historia') != paciente_old.numero_historia):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'N de Historia de la Institución del Convenio'
            historicoCambio.valor_anterior = paciente_old.numero_historia
            historicoCambio.valor_actual = request.POST.get('numero_historia')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('tipo_identificacion') != paciente_old.tipo_identificacion):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Tipo de Identificacion'
            historicoCambio.valor_anterior = paciente_old.tipo_identificacion
            historicoCambio.valor_actual = request.POST.get('tipo_identificacion')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('identificacion') is not None and paciente_old.identificacion is not None):
            if (request.POST.get('identificacion') != paciente_old.identificacion):
                historicoCambio = HistoricoCambio()
                historicoCambio.fecha = fecha
                historicoCambio.campo_modificado = 'Identificacion'
                historicoCambio.valor_anterior = paciente_old.identificacion
                historicoCambio.valor_actual = request.POST.get('identificacion')
                historicoCambio.paciente = paciente_old
                historicoCambio.usuario = request.user
                historicoCambio.save()

        if (request.POST.get('partida_nacimiento') is not None and paciente_old.partida_nacimiento is not None):
            if (request.POST.get('partida_nacimiento') != paciente_old.partida_nacimiento):
                historicoCambio = HistoricoCambio()
                historicoCambio.fecha = fecha
                historicoCambio.campo_modificado = 'Partida de Nacimiento'
                historicoCambio.valor_anterior = paciente_old.partida_nacimiento
                historicoCambio.valor_actual = request.POST.get('partida_nacimiento')
                historicoCambio.paciente = paciente_old
                historicoCambio.usuario = request.user
                historicoCambio.save()

        if (request.POST.get('nombre_primero') != paciente_old.nombre_primero):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Primer Nombre'
            historicoCambio.valor_anterior = paciente_old.nombre_primero
            historicoCambio.valor_actual = request.POST.get('nombre_primero')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('nombre_segundo') != paciente_old.nombre_segundo):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Segundo Nombre'
            historicoCambio.valor_anterior = paciente_old.nombre_segundo
            historicoCambio.valor_actual = request.POST.get('nombre_segundo')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('apellido_primero') != paciente_old.apellido_primero):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Primer Apellido'
            historicoCambio.valor_anterior = paciente_old.apellido_primero
            historicoCambio.valor_actual = request.POST.get('apellido_primero')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('apellido_segundo') != paciente_old.apellido_segundo):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Segundo Apellido'
            historicoCambio.valor_anterior = paciente_old.apellido_segundo
            historicoCambio.valor_actual = request.POST.get('apellido_segundo')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('fecha_nacimiento') != paciente_old.fecha_nacimiento):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Fecha de Nacimiento'
            historicoCambio.valor_anterior = paciente_old.fecha_nacimiento
            historicoCambio.valor_actual = request.POST.get('fecha_nacimiento')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('sexo') != paciente_old.sexo):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Sexo'
            historicoCambio.valor_anterior = paciente_old.sexo
            historicoCambio.valor_actual = request.POST.get('sexo')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('nacionalidad') != paciente_old.nacionalidad):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Nacionalidad'
            historicoCambio.valor_anterior = paciente_old.nacionalidad
            historicoCambio.valor_actual = request.POST.get('nacionalidad')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (estado_civil_new.nombre != paciente_old.estado_civil.nombre):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Estado Civil'
            historicoCambio.valor_anterior = paciente_old.estado_civil.nombre
            historicoCambio.valor_actual = estado_civil_new.nombre
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (nivel_estudio_new.nombre != paciente_old.nivel_estudio.nombre):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Nivel de Estudio'
            historicoCambio.valor_anterior = paciente_old.nivel_estudio.nombre
            historicoCambio.valor_actual = nivel_estudio_new.nombre
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('represent_nombre_primero') is not None and paciente_old.represent_nombre_primero is not None):
            if (request.POST.get('represent_nombre_primero') != paciente_old.represent_nombre_primero):
                historicoCambio = HistoricoCambio()
                historicoCambio.fecha = fecha
                historicoCambio.campo_modificado = 'Representante: Primer Nombre'
                historicoCambio.valor_anterior = paciente_old.represent_nombre_primero
                historicoCambio.valor_actual = request.POST.get('represent_nombre_primero')
                historicoCambio.paciente = paciente_old
                historicoCambio.usuario = request.user
                historicoCambio.save()

        if (request.POST.get('represent_nombre_segundo') is not None and paciente_old.represent_nombre_segundo is not None):
            if (request.POST.get('represent_nombre_segundo') != paciente_old.represent_nombre_segundo):
                historicoCambio = HistoricoCambio()
                historicoCambio.fecha = fecha
                historicoCambio.campo_modificado = 'Representante: Segundo Nombre'
                historicoCambio.valor_anterior = paciente_old.represent_nombre_segundo
                historicoCambio.valor_actual = request.POST.get('represent_nombre_segundo')
                historicoCambio.paciente = paciente_old
                historicoCambio.usuario = request.user
                historicoCambio.save()

        if (request.POST.get('represent_apellido_primero') is not None and paciente_old.represent_apellido_primero is not None):
            if (request.POST.get('represent_apellido_primero') != paciente_old.represent_apellido_primero):
                historicoCambio = HistoricoCambio()
                historicoCambio.fecha = fecha
                historicoCambio.campo_modificado = 'Representante: Primer Apellido'
                historicoCambio.valor_anterior = paciente_old.represent_apellido_primero
                historicoCambio.valor_actual = request.POST.get('represent_apellido_primero')
                historicoCambio.paciente = paciente_old
                historicoCambio.usuario = request.user
                historicoCambio.save()

        if (request.POST.get('represent_apellido_segundo') is not None and paciente_old.represent_apellido_segundo is not None):
            if (request.POST.get('represent_apellido_segundo') != paciente_old.represent_apellido_segundo):
                historicoCambio = HistoricoCambio()
                historicoCambio.fecha = fecha
                historicoCambio.campo_modificado = 'Representante: Segundo Apellido'
                historicoCambio.valor_anterior = paciente_old.represent_apellido_segundo
                historicoCambio.valor_actual = request.POST.get('represent_apellido_segundo')
                historicoCambio.paciente = paciente_old
                historicoCambio.usuario = request.user
                historicoCambio.save()

        if (request.POST.get('represent_tipo_identificacion') != paciente_old.represent_tipo_identificacion):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Representante: Tipo Identificación'
            historicoCambio.valor_anterior = paciente_old.represent_tipo_identificacion
            historicoCambio.valor_actual = request.POST.get('represent_tipo_identificacion')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('represent_identificacion') is not None and paciente_old.represent_identificacion is not None):
            if (request.POST.get('represent_identificacion') != paciente_old.represent_identificacion):
                historicoCambio = HistoricoCambio()
                historicoCambio.fecha = fecha
                historicoCambio.campo_modificado = 'Representante: Identificación'
                historicoCambio.valor_anterior = paciente_old.represent_identificacion
                historicoCambio.valor_actual = request.POST.get('represent_identificacion')
                historicoCambio.paciente = paciente_old
                historicoCambio.usuario = request.user
                historicoCambio.save()

        if (request.POST.get('represent_numero_hijo') != paciente_old.represent_numero_hijo):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Representante: Número de Hijo'
            historicoCambio.valor_anterior = paciente_old.represent_numero_hijo
            historicoCambio.valor_actual = request.POST.get('represent_numero_hijo')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('represent_sexo') != paciente_old.represent_sexo):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Representante: Sexo'
            historicoCambio.valor_anterior = paciente_old.represent_sexo
            historicoCambio.valor_actual = request.POST.get('represent_sexo')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('represent_fecha_nacimiento') != paciente_old.represent_fecha_nacimiento):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Representante: Fecha de Nacimiento'
            historicoCambio.valor_anterior = paciente_old.represent_fecha_nacimiento
            historicoCambio.valor_actual = request.POST.get('represent_fecha_nacimiento')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('represent_nacionalidad') != paciente_old.represent_nacionalidad):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Representante: Nacionalidad'
            historicoCambio.valor_anterior = paciente_old.represent_nacionalidad
            historicoCambio.valor_actual = request.POST.get('represent_nacionalidad')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if id_represent_estado_civil:
            if (represent_estado_civil_new.nombre != paciente_old.represent_estado_civil.nombre):
                historicoCambio = HistoricoCambio()
                historicoCambio.fecha = fecha
                historicoCambio.campo_modificado = 'Representante: Estado Civil'
                historicoCambio.valor_anterior = paciente_old.represent_estado_civil.nombre
                historicoCambio.valor_actual = estado_civil_new.nombre
                historicoCambio.paciente = paciente_old
                historicoCambio.usuario = request.user
                historicoCambio.save()

        if id_represent_nivel_estudio:
            if (represent_nivel_estudio_new.nombre != paciente_old.represent_nivel_estudio.nombre):
                historicoCambio = HistoricoCambio()
                historicoCambio.fecha = fecha
                historicoCambio.campo_modificado = 'Representante: Nivel de Estudio'
                historicoCambio.valor_anterior = paciente_old.represent_nivel_estudio.nombre
                historicoCambio.valor_actual = nivel_estudio_new.nombre
                historicoCambio.paciente = paciente_old
                historicoCambio.usuario = request.user
                historicoCambio.save()

        if (request.POST.get('telefono_local') != paciente_old.telefono_local):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Teléfono Local'
            historicoCambio.valor_anterior = paciente_old.telefono_local
            historicoCambio.valor_actual = request.POST.get('telefono_local')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('telefono_celular1') != paciente_old.telefono_celular1):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Teléfono Celular 1'
            historicoCambio.valor_anterior = paciente_old.telefono_celular1
            historicoCambio.valor_actual = request.POST.get('telefono_celular1')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('telefono_celular2') != paciente_old.telefono_celular2):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Teléfono Celular 2'
            historicoCambio.valor_anterior = paciente_old.telefono_celular2
            historicoCambio.valor_actual = request.POST.get('telefono_celular2')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('correo_electronico') != paciente_old.correo_electronico):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Correo Electrónico'
            historicoCambio.valor_anterior = paciente_old.correo_electronico
            historicoCambio.valor_actual = request.POST.get('correo_electronico')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('calle_avenida') != paciente_old.calle_avenida):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Calle / Avenida'
            historicoCambio.valor_anterior = paciente_old.calle_avenida
            historicoCambio.valor_actual = request.POST.get('calle_avenida')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('sector_barrio_urb') != paciente_old.sector_barrio_urb):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Sector / Barrio / Urbanización'
            historicoCambio.valor_anterior = paciente_old.sector_barrio_urb
            historicoCambio.valor_actual = request.POST.get('sector_barrio_urb')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (request.POST.get('casa_edificio') != paciente_old.casa_edificio):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Casa / Edificio'
            historicoCambio.valor_anterior = paciente_old.casa_edificio
            historicoCambio.valor_actual = request.POST.get('casa_edificio')
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (estado_new.nombre != paciente_old.ciudad.estado.nombre):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Estado'
            historicoCambio.valor_anterior = paciente_old.ciudad.estado.nombre
            historicoCambio.valor_actual = estado_new.nombre
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (ciudad_new.nombre != paciente_old.ciudad.nombre):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Ciudad'
            historicoCambio.valor_anterior = paciente_old.ciudad.nombre
            historicoCambio.valor_actual = estado_new.nombre
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (municipio_new.nombre != paciente_old.parroquia.municipio.nombre):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Municipio'
            historicoCambio.valor_anterior = paciente_old.parroquia.municipio.nombre
            historicoCambio.valor_actual = estado_new.nombre
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

        if (parroquia_new.nombre != paciente_old.parroquia.nombre):
            historicoCambio = HistoricoCambio()
            historicoCambio.fecha = fecha
            historicoCambio.campo_modificado = 'Parroquia'
            historicoCambio.valor_anterior = paciente_old.parroquia.nombre
            historicoCambio.valor_actual = estado_new.nombre
            historicoCambio.paciente = paciente_old
            historicoCambio.usuario = request.user
            historicoCambio.save()

class BusquedaView(View):
    """
    Clase Vista que permite consultar pacientes.

    template_name: Nombre de la plantilla.
    """

    template_name = 'busqueda.html'

#    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_medico', logger=logger)
    def get(self, request, *args, **kwargs):
        """
        Método get que consulta clientes.


        Args:
            request: El objeto HTTP Request.

        Returns:
            El objeto HTTP Response.
        """


        busqueda = request.GET.get('busqueda', '')
        if busqueda == '':
            pacientes = Paciente.objects.all()
        else:
            pacientes = Paciente.objects.filter(Q(identificacion__contains=busqueda) | Q(nombre_primero__contains=busqueda) | Q(nombre_segundo__contains=busqueda)
                                                | Q(apellido_primero__contains=busqueda) | Q(apellido_segundo__contains=busqueda) | Q(id__contains=busqueda)
                                                | Q(partida_nacimiento__contains=busqueda) | Q(represent_identificacion__contains=busqueda) | Q(represent_numero_hijo__contains=busqueda))
        data = []
        for paciente in pacientes:
            data.append({'id': paciente.id,
                         'paciente_id': paciente.id,
                         'partida_nacimiento': paciente.partida_nacimiento,
                         'identificacion': paciente.tipo_identificacion + ' ' + paciente.identificacion if paciente.tipo_identificacion else '',
                         'nombre': (paciente.nombre_primero if paciente.nombre_primero else '') + u' ' + (
                         paciente.nombre_segundo if paciente.nombre_segundo else ''),
                         'apellido': (paciente.apellido_primero if paciente.apellido_primero else '') + u' ' + (
                         paciente.apellido_segundo if paciente.apellido_segundo else ''),
                         'ciudad': paciente.ciudad.nombre,
                         'estado': paciente.ciudad.estado.nombre})
        tabla = PacientesTable(data)
        RequestConfig(request, paginate={ 'per_page': 5 }).configure(tabla)

        return render(request, self.template_name, { 'tabla': tabla })

class HistoricoCambioPacienteView(View):
    """
        Clase Vista que permite consultar los cambios realizados a los campos de un paciente.

        template_name: Nombre de la plantilla.
        """

    template_name = 'historico_cambio_paciente.html'

#    @ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.diagnostico_medico', logger=logger)
    def get(self, request, pk,  *args, **kwargs):
        """
            Método get que consulta los cambios.

            Args:
                request: El objeto HTTP Request.

            Returns:
                El objeto HTTP Response.
            """

        busqueda = request.GET.get('busqueda', '')
        if busqueda == '':
            historicoCambios = HistoricoCambio.objects.raw('select * from t_udm_historico_cambio where paciente_id =' + pk)
        else:
            historicoCambios = HistoricoCambio.objects.filter((
                Q(campo_modificado__contains=busqueda) | Q(valor_anterior__contains=busqueda)
                | Q(valor_actual__contains=busqueda) | Q(usuario__first_name__contains= busqueda)
                | Q(usuario__last_name__contains=busqueda)), paciente_id=pk)
        data = []
        for historicoCambio in historicoCambios:
            medico = UDMUser.objects.get(id= historicoCambio.usuario.id)
            data.append({'fecha': historicoCambio.fecha,
                         'campo_modificado': historicoCambio.campo_modificado,
                         'valor_anterior': historicoCambio.valor_anterior,
                         'valor_actual': historicoCambio.valor_actual,
                         'medico': medico.first_name + ' ' + medico.last_name})
        tabla = HistoricoCambiosTable(data)
        RequestConfig(request, paginate={'per_page': 10}).configure(tabla)

        return render(request, self.template_name, {'tabla': tabla, 'pk': pk})


class RegistrarUsuarioUdmView(View):
    """
    Clase Vista que permite consultar un usuario.

    template_name: reestablecer_clave.html
    """

    template_name = 'reestablecer_clave.html'

    #@ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.reestablecer_clave', logger=logger)
    def get(self, request, pk, *args, **kwargs):
        if len(request.GET.items()) > 0:
            udm_user_forma = UDMRegistroUserForm(request.GET)
            id_estado = int(request.GET.get('id_estado', '0'))
            id_ciudad = int(request.GET.get('id_ciudad', '0'))
            id_institucion = int(request.GET.get('id_institucion', '0'))
            id_unidad = int(request.GET.get('id_unidad', '0'))
        else:
            id_estado = 0
            id_ciudad = 0
            id_institucion = 0
            id_unidad = 0
            udm_user_forma = UDMRegistroUserForm()

        return render(request, self.template_name,
                  {'udm_user_forma': udm_user_forma,
                   'instituciones': Institucion.objects.all().order_by('nombre'),
                   'unidades': Unidad.objects.all().order_by('nombre'),
                   'estados': Estado.objects.all().order_by('nombre'),
                   'ciudades': Ciudad.objects.filter(estado_id=id_estado).order_by('nombre'),
                   'id_estado': id_estado, 'id_ciudad': id_ciudad, 'id_institucion': id_institucion,'id_unidad': id_unidad})

    def post(self, request, pk, *args, **kwargs):
        # se extrae la ubicacion del  colegio del form
        id_estado = int(request.POST.get('id_estado', '0'))
        id_ciudad = int(request.POST.get('id_ciudad', '0'))

        id_istitucion = int(request.POST.get('id_institucion', '0'))
        id_unidad = int(request.POST.get('id_unidad', '0'))

        #se crea el nombre de usuario tomando las iniciales del nombre
        username = request.POST.get('first_name')[0:1] + request.POST.get('nombre_segundo')[0:1] + request.POST.get('last_name')[0:1] + request.POST.get('apellido_segundo')[0:1]
        username = username.lower()

        #se verifica si el username está registrado en la Base de datos
        try:
            num_user = UDMUser.objects.filter(username__icontains=username).count()
        except UDMUser.DoesNotExist:
            num_user = 0

        ciudad = Ciudad.objects.get(id=id_ciudad)
        estado = ciudad.estado.nombre
        istitucion = Institucion.objects.get(id=id_istitucion)
        unidad = Unidad.objects.get(id=id_unidad)
        user = UDMUser()
        user.ciudad = ciudad

        #Si ya existe un usuario con el mismo username, se concatena un número secuencial al username
        if (num_user != 0):
            user.username = username + str(num_user + 1)
        else:
            user.username = username

        user.ubicacion_colegio = estado
        user.institucion = istitucion
        user.unidad = unidad
        user.fecha_ult_reest_clave = date.today().strftime('%Y-%m-%d')
        user.is_active = False
        user.is_clave_caducable = True

        #se extrae los datos del form
        udm_user_forma = UDMRegistroUserForm(request.POST, instance=user)

        if udm_user_forma.is_valid():
            id_ciudad = int(request.POST.get('id_ciudad', '0'))
            usuario = udm_user_forma.save()
            self.enviar_correo(usuario)
            return HttpResponseRedirect(
            settings.URL_PREFIX + '/login?mensaje=Se ha guardado su registro. Recibirá un correo del administrador con sus datos de usuario ')


        return render(request, self.template_name,
                      {'udm_user_forma': UDMRegistroUserForm()})

    def enviar_correo(self, usuario):
        contenido = u'<html><body><table border="0" width="100%"><tr><td align="left"><img src="{{ MEDIA_ROOT }}img/logo-j.png" width="79" height="60"/></td><td align="right"><img src="{{ MEDIA_ROOT }}img/logo-j.jpg" width="60" height="60"/></td></tr></table><p align="center"><b>SOLICITUD DE REGISTRO A LA UNIDAD DE DIAGNÓSTICO MOLECULAR</b></p><p>&nbsp;</p> '
        contenido += u'<p>Se ha registrado a un nuevo usuario con los siguientes datos:  <ul>'
        contenido += u' <li>Usuario: ' + usuario.username + u'</li>'
        contenido += u' <li>Nombre: ' + usuario.first_name + u'</li>'
        contenido += u' <li>Apellido: ' + usuario.last_name + u'</li>'
        contenido += u' <li>Cédula: ' + usuario.cedula_pasaporte + u'</li>'
        contenido += u' <li>Correo electrónico: ' + usuario.email + u'</li>'
        contenido += u' </ul>'
        contenido += u'</p><p>Fecha de Registro: '
        contenido += date.today().strftime('%d/%m/%Y')
        contenido += u'</p><p>Deberá revisar su información, asignarle una contraseña a través del portal del administrador y enviar al correo del nuevo usuario, su username y contraseña '
        contenido += u'</p><table border="0" width="100%"><tr><td valign="top"><table border="0" width="100%"<tr><td colspan="2">&nbsp;</td></tr>'

        mensaje = MIMEMultipart('alternative')
        mensaje.set_charset('utf8')
        mensaje['From'] = settings.EMAIL_SERVER_USERNAME
        mensaje['To'] = ['udm@jacintoconvit.org', 'ronick.a.ruiz@jacintoconvit.org'] #'udm@jacintoconvit.org'
        mensaje['Subject'] = u'Registro de nuevo usuario '
        mensaje.attach(MIMEText(contenido, 'html', 'utf8'))

        destinatarios = ['udm@jacintoconvit.org', 'ronick.a.ruiz@jacintoconvit.org']
        server = smtplib.SMTP(settings.EMAIL_SERVER_URL)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_SERVER_USERNAME, settings.EMAIL_SERVER_PASSWORD)
        #server.sendmail(settings.EMAIL_SERVER_USERNAME, 'udm@jacintoconvit.org', mensaje.as_string())
        server.sendmail(settings.EMAIL_SERVER_USERNAME, destinatarios, mensaje.as_string())
        server.quit()

class ReestablecerClaveView(View):
    """
    Clase Vista que permite consultar un usuario.

    template_name: reestablecer_clave.html
    """

    template_name = 'reestablecer_clave.html'

    #@ConvitLoggerExceptionDecorator(permisos='unidaddiagnosticomolecular.reestablecer_clave', logger=logger)


    def get(self, request, *args, **kwargs):
        busqueda = request.GET.get('busqueda', '')
        if busqueda != '':
            try:
                usuario = UDMUser.objects.get(username__iexact=busqueda)
            except UDMUser.DoesNotExist:
                return HttpResponseRedirect(
                    settings.URL_PREFIX + '/reestablecer_clave?mensaje=Usuario no registrado')

            formato_fecha = '%Y-%m-%d'

            fecha_actual = date.today().strftime(formato_fecha)
            fecha_usuario = usuario.fecha_ult_reest_clave.strftime(formato_fecha)
            fecha_fin_convenio = usuario.unidad_fecha_fin.strftime(formato_fecha)

            # se necesitan estas conversiones para realizar operaciones con fecha
            fecha_actual = datetime.strptime(fecha_actual, formato_fecha)
            fecha_usuario = datetime.strptime(fecha_usuario, formato_fecha)
            diferencia_dias = int((fecha_actual - fecha_usuario).days)
            fecha_fin_convenio = datetime.strptime(fecha_fin_convenio, formato_fecha)


            if (diferencia_dias < 90 or usuario.is_clave_caducable == False ) and fecha_fin_convenio < fecha_actual and usuario.is_active == True:
                request.session["usuario_reestabl"] = busqueda
                codigo = str(random.randint(1000, 10000))
                usuario.codigo_cambio_clave = codigo
                user_modificado = usuario.save()
                self.enviar_correo_codigo_clave(usuario)
                return HttpResponseRedirect(
                    settings.URL_PREFIX + '/recuperar_clave?mensaje= Le hemos enviado un código a su correo electrónico para que pueda recuperar su contraseña. Por favor ingrese el código')

            else:
                self.enviar_correo(usuario)
                return HttpResponseRedirect(
                    settings.URL_PREFIX + '/login?mensaje= Clave Vencida, se ha enviado un correo al administrador quien le asignará una nueva contraseña')


        return render(request, self.template_name)

    def enviar_correo(self, usuario):
        contenido = u'<html><body><table border="0" width="100%"><tr><td align="left"><img src="../html/static/img/logo-j.jpg" width="79" height="60"/></td><td align="right"><img src="../html/static/img/logo-j.jpg" width="60" height="60"/></td></tr></table><p align="center"><b>SOLICITUD DE REESTABLECIMIENTO DE CLAVE</b></p><p>&nbsp;</p> '
        contenido += u'<p>La contraseña del usuario:'
        contenido += usuario.first_name + u' ' + usuario.last_name
        contenido += u' ha vencido. Por favor verifique si esta persona actualmente labora en la unidad. '
        contenido += u'</p><p>Los datos del usuario son los siguientes: <ul>'
        contenido += u' <li>Id: ' + str(usuario.id) + u'</li>'
        contenido += u' <li>Nombre: ' + usuario.first_name + u'</li>'
        contenido += u' <li>Apellido: ' + usuario.last_name + u'</li>'
        contenido += u' <li>Usuario:' + usuario.username + u'</li>'
        contenido += u' <li>Correo electrónico: ' + usuario.email + u'</li>'
        contenido += u' </ul>'
        contenido += u'</p><p>Fecha de solicitud: '
        contenido += date.today().strftime('%d/%m/%Y')
        contenido += u'</p><table border="0" width="100%"><tr><td valign="top"><table border="0" width="100%"<tr><td colspan="2">&nbsp;</td></tr>'

        mensaje = MIMEMultipart('alternative')
        mensaje.set_charset('utf8')
        mensaje['From'] = settings.EMAIL_SERVER_USERNAME
        mensaje['To'] = ['udm@jacintoconvit.org', 'ronick.a.ruiz@jacintoconvit.org']  # 'udm@jacintoconvit.org'
        mensaje['Subject'] = u'Reestablecer contraseña'
        mensaje.attach(MIMEText(contenido, 'html', 'utf8'))

        destinatarios = ['udm@jacintoconvit.org', 'ronick.a.ruiz@jacintoconvit.org']
        server = smtplib.SMTP(settings.EMAIL_SERVER_URL)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_SERVER_USERNAME, settings.EMAIL_SERVER_PASSWORD)
        # server.sendmail(settings.EMAIL_SERVER_USERNAME, 'udm@jacintoconvit.org', mensaje.as_string())
        server.sendmail(settings.EMAIL_SERVER_USERNAME, destinatarios, mensaje.as_string())
        server.quit()

    def enviar_correo_codigo_clave(self, usuario):
        contenido = u'<html><body><table border="0" width="100%"><tr><td align="left"><img src="{{ STATIC_URL }}img/logo-j.jpg" width="79" height="60"/></td><td align="right"><img src="../html/static/img/logo-j.jpg" width="60" height="60"/></td></tr></table><p align="center"><b>SOLICITUD DE RECUPERACIÓN DE CLAVE</b></p><p>&nbsp;</p> '
        contenido += u'<p>Sr(a) ' + usuario.last_name + u'</p>'
        contenido += u'<p> &nbsp; </p>'
        contenido += u'<p>El código para reestablecer su contraseña es: ' + usuario.codigo_cambio_clave
        contenido += u'</p> '
        contenido += u'<table border="0" width="100%"><tr><td valign="top"><table border="0" width="100%"<tr><td colspan="2">&nbsp;</td></tr>'

        mensaje = MIMEMultipart('alternative')
        mensaje.set_charset('utf8')
        mensaje['From'] = settings.EMAIL_SERVER_USERNAME
        mensaje['To'] = usuario.email  # 'udm@jacintoconvit.org'
        mensaje['Subject'] = u'Recuperación de contraseña'
        mensaje.attach(MIMEText(contenido, 'html', 'utf8'))

        server = smtplib.SMTP(settings.EMAIL_SERVER_URL)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_SERVER_USERNAME, settings.EMAIL_SERVER_PASSWORD)
        # server.sendmail(settings.EMAIL_SERVER_USERNAME, 'udm@jacintoconvit.org', mensaje.as_string())
        server.sendmail(settings.EMAIL_SERVER_USERNAME, usuario.email, mensaje.as_string())
        server.quit()

class RecuperarClaveView(View):
    """
    Clase Vista que permite la recuperación de clave a través de un código enviado al correo
    del usuario

    template_name: recuperar_clave.html
    """
    template_name = 'recuperar_clave.html'

    def get(self, request, *args, **kwargs):
        """
        Método get que comprueba si un código de recuperación de calve es válido

        Args:
            request: El objeto HTTP Request.

        Returns:
            El objeto HTTP Response.
        """

        codigo = request.GET.get('codigo', '')
        if (codigo != '' and request.session["usuario_reestabl"]) :
            usuario = UDMUser.objects.get(username__iexact=request.session["usuario_reestabl"])

            if (codigo == usuario.codigo_cambio_clave):
                return HttpResponseRedirect(settings.URL_PREFIX + '/cambiar_clave')

            else:
                return HttpResponseRedirect(
                    settings.URL_PREFIX + '/recuperar_clave?mensaje= Código incorrecto')

        return render(request, self.template_name)

class CambiarClaveView(View):
    """
    Clase Vista que permite cambiar la clave de un usuario.

    template_name: cambiar_clave.html
    """

    template_name = 'cambiar_clave.html'

    def get(self, request, *args, **kwargs):
        if request.session["usuario_reestabl"]:
            return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        password_nueva = request.POST.get('pass_nueva', '0')
        usuario = UDMUser.objects.get(username__iexact=request.session["usuario_reestabl"])
        if usuario:
            usuario.set_password = password_nueva
            usuario.codigo_cambio_clave = None
            usuario.save()
            del request.session["usuario_reestabl"]
            return HttpResponseRedirect(
                settings.URL_PREFIX + '/login?mensaje=Su contraseña ha sido reestablecida con éxito ')