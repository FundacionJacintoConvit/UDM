# coding: utf-8

from datetime import date, datetime
import os
import logging
import smtplib
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
from unidaddiagnosticomolecular.models import Paciente, Diagnostico, DiagnosticoExamen, DiagnosticoSintoma, DiagnosticoEstudio, DiagnosticoAntecedente, DiagnosticoTrasladoMuestra, Ciudad, Estado, TipoAntecedente, TipoEstudio, TipoExamen
from unidaddiagnosticomolecular.forms import PacienteForm, PacienteMostrarForm, DiagnosticoMedicoForm, DiagnosticoPatologoForm, DiagnosticoUDMForm, DiagnosticoExamenForm, DiagnosticoSintomaForm, DiagnosticoEstudioForm, DiagnosticoExamenForm, DiagnosticoAntecedenteForm, DiagnosticoTrasladoMuestraForm, UDMUserForm, DiagnosticoExamenFormSet, DiagnosticoSintomaFormSet, DiagnosticoEstudioFormSet, DiagnosticoExamenFormSet, DiagnosticoAntecedenteFormSet, DiagnosticoTrasladoMuestraFormSet

logger = logging.getLogger(__name__)

class LinkDateTimeColumn(LinkColumn):
    def __init__(self, viewname, format, *args, **extra):
        super(LinkDateTimeColumn, self).__init__(viewname, *args, **extra)
        self.format = format

    def render(self, value, record, bound_column):  
        if value != None:
            value = value.strftime(self.format)

        return super(LinkDateTimeColumn, self).render(value, record, bound_column)
		
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

        if request.user.has_perms(( 'unidaddiagnosticomolecular.diagnostico_medico', )):
            return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda_diagnostico_medico')
        elif request.user.has_perms(( 'unidaddiagnosticomolecular.diagnostico_patologo', )):
            return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda_diagnostico_patologo')
        elif request.user.has_perms(( 'unidaddiagnosticomolecular.diagnostico_udm', )):
            return HttpResponseRedirect(settings.URL_PREFIX + '/busqueda_diagnostico_udm')
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