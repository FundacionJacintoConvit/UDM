# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    estado = models.ForeignKey('Estado')

    def __unicode__(self):
        return unicode(self.nombre) + ' - ' + unicode(self.estado)

    class Meta:
        managed = False
        db_table = 't_udm_municipio'
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering = ['nombre']

class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    estado = models.ForeignKey('Estado')

    def __unicode__(self):
        return unicode(self.nombre) + ' - ' + unicode(self.estado)

    class Meta:
        managed = False
        db_table = 't_udm_ciudad'
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = [ 'nombre' ]

class Parroquia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    municipio = models.ForeignKey('Municipio')

    def __unicode__(self):
        return unicode(self.nombre) + ' - ' + unicode(self.municipio)

    class Meta:
        managed = False
        db_table = 't_udm_parroquia'
        verbose_name = 'Parroquia'
        verbose_name_plural = 'Parroquias'
        ordering = [ 'nombre' ]

class Institucion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
	
    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_institucion'
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
        ordering = [ 'nombre' ]

class Unidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_unidad'
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        ordering = [ 'nombre' ]

class EstadoCivil(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_estado_civil'
        verbose_name = 'Estado Civil'
        verbose_name_plural = 'Estados Civiles'
        ordering = [ 'nombre' ]

class NivelEstudio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_nivel_estudio'
        verbose_name = 'Nivel de Estudio'
        verbose_name_plural = 'Niveles de Estudio'
        ordering = [ 'nombre' ]
		
class TipoEnfermedad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_tipo_enfermedad'
        verbose_name = 'Tipo de Enfermedad'
        verbose_name_plural = 'Tipos de Enfermedad'
        ordering = [ 'orden' ]
		
class TipoCancer(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_tipo_cancer'
        verbose_name = 'Tipo de Cancer'
        verbose_name_plural = 'Tipos de Cancer'
        ordering = [ 'orden' ]

class TipoEstudio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_tipo_estudio'
        verbose_name = 'Tipo de Estudio'
        verbose_name_plural = 'Tipos de Estudio'
        ordering = [ 'orden' ]

class UDMUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    nombre_segundo = models.CharField(verbose_name='Segundo Nombre', max_length=255, blank=True)
    apellido_segundo = models.CharField(verbose_name='Segundo Apellido', max_length=255, blank=True)    
    nacionalidad = models.CharField(verbose_name='Nacionalidad', max_length=1, choices=(( 'V', 'Venezolano' ), ( 'E', 'Extranjero' )), blank=True, null=True)
    cedula_pasaporte = models.CharField(verbose_name='Número de Cédula o Pasaporte', max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', blank=True, null=True)
    edad = models.IntegerField(verbose_name='Edad', blank=True, null=True)
    sexo = models.CharField(verbose_name='Sexo', max_length=1, choices=(( 'M', 'Masculino' ), ( 'F', 'Femenino' )), blank=True, null=True)
    fecha_ult_reest_clave = models.DateField(verbose_name='Fecha del último reestablacimiento de clave', blank=True, null=True)
    is_clave_caducable = models.BooleanField(verbose_name='¿La contraseña tendrá caducidad?', blank=True)
    codigo_cambio_clave = models.CharField(verbose_name='Código de recuperación de clave', max_length=255, blank=True, null=True)
    profesion = models.CharField(verbose_name='Profesión', max_length=255, blank=True, null=True, choices=(('Médico','Médico'),('Biólogo','Biólogo'),('Bionalista','Bionalista')))
    especializacion = models.CharField(verbose_name='Especialización', max_length=255, blank=True, null=True)
    especializacion_culminada = models.CharField(verbose_name='Especialización Culminada?', max_length=1, choices=(( 'S', 'Si' ), ( 'N', 'No' )), blank=True, null=True)
    numero_mpps = models.CharField(verbose_name='N del MPPS', max_length=255, blank=True, null=True)
    numero_colegio = models.CharField(verbose_name='N del Colegio', max_length=255, blank=True, null=True)
    ubicacion_colegio = models.CharField(verbose_name='Ubicación del Colegio', max_length=255, blank=True, null=True)
    institucion = models.ForeignKey(Institucion, verbose_name='Institución', blank=True, null=True)
    unidad = models.ForeignKey(Unidad, verbose_name='Unidad', blank=True, null=True)
    unidad_fecha_inicio = models.DateField(verbose_name='Fecha de Inicio en la Unidad', blank=True, null=True)
    unidad_fecha_fin = models.DateField(verbose_name='Fecha de Finalización en la Unidad', blank=True, null=True)
    unidad_director = models.CharField(verbose_name='Director de la Unidad', max_length=255, blank=True, null=True)
    unidad_director_telefono = models.CharField(verbose_name='Teléfono del Director de la Unidad', max_length=255, blank=True, null=True)
    unidad_director_email = models.CharField(verbose_name='Correo electrónico del Director de la Unidad', max_length=255, blank=True, null=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=255, blank=True)
    ciudad = models.ForeignKey(Ciudad, verbose_name='Ciudad', null=True)
    firma = models.FileField(verbose_name='Firma', upload_to='../firmas', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_udm_usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Diagnostico(models.Model):
    id = models.AutoField(verbose_name='Número de Historia', primary_key=True)
    medico_tipo_diagnostico = models.CharField(verbose_name='Tipo de Diagnóstico', max_length=1, choices=(( 'C', 'Por Cancer' ), ( 'O', 'Por Otra Enfermedad' )), blank=True, null=True)
    medico_observaciones = models.CharField(verbose_name='Observaciones', max_length=4000, blank=True)
    medico_fecha_ini_signos = models.DateField(verbose_name='Fecha de Inicio de Signos', blank=True, null=True)
    medico_fecha_fin_signos = models.DateField(verbose_name='Fecha Fin Signos', blank=True, null=True)
    medico_fecha_ini_sintomas = models.DateField(verbose_name='Fecha de Inicio de Síntomas', blank=True, null=True)
    medico_fecha_fin_sintomas = models.DateField(verbose_name='Fecha Fin de Síntomas', blank=True, null=True)
    medico_signos = models.CharField(verbose_name='Signos', max_length=4000, blank=True)
    medico_sintomas = models.CharField(verbose_name='Sintomas', max_length=4000, blank=True)
    medico_diagnostico_presuntivo = models.CharField(verbose_name='Diagnóstico Presuntivo', max_length=4000, blank=True)
    medico_presencia_tumor = models.CharField(verbose_name='Presencia de Tumor', max_length=1, blank=True)
    medico_ubicacion_tumor = models.CharField(verbose_name='Ubicación del Tumor', max_length=4000, blank=True)
    medico_presencia_metastasis = models.CharField(verbose_name='Presencia de Metástasis', max_length=1, blank=True)
    medico_ubicacion_metastasis = models.CharField(verbose_name='Ubicación de Metástasis', max_length=4000, blank=True)
    medico_otros_estudios = models.CharField(verbose_name='Otros Estudios', max_length=4000, blank=True)
    medico_familiar_antecedente = models.NullBooleanField(verbose_name='Familiar con Antecedentes')
    medico_familiar_nexo = models.CharField(verbose_name='Familiar Nexo', max_length=255, blank=True)
    medico_familiar_tipo_enfermedad = models.ForeignKey(TipoEnfermedad, blank=True, null=True, db_column='medico_familiar_tipo_enferm_id')
    medico_familiar_tipo_cancer = models.ForeignKey(TipoCancer, blank=True, null=True)
    medico_familiar_enfermedad_otra = models.CharField(verbose_name='Familiar Enfermedad Otra', max_length=255, blank=True)
    medico_ubicacion_institucion = models.ForeignKey(Institucion, blank=True, null=True)
    medico_ubicacion_telefono = models.CharField(verbose_name='Ubicación Paciente Teléfono', max_length=255, blank=True)
    medico_ubicacion_piso = models.DecimalField(verbose_name='Ubicación Paciente Piso', max_digits=3, decimal_places=0, blank=True, null=True)
    medico_ubicacion_habitacion = models.CharField(verbose_name='Ubicación Paciente Habitación', max_length=255, blank=True)
    medico_paciente_cumplio_condiciones = models.CharField(verbose_name='Paciente Cumplió con Condiciones', max_length=1, blank=True, db_column='medico_paciente_cumplio_cond')
    medico_paciente_cumplio_ayuno_12 = models.NullBooleanField(verbose_name='Paciente Cumplió con 12 horas de Ayuno', db_column='medico_paciente_cumplio_ayuno12')
    medico_paciente_cumplio_ayuno_3 = models.NullBooleanField(verbose_name='Paciente Cumplió con 3 horas de Ayuno', db_column='medico_paciente_cumplio_ayuno3')
    medico_paciente_cumplio_observaciones = models.CharField(verbose_name='Observaciones', max_length=4000, blank=True, db_column='medico_paciente_cumplio_observa')
    patologo_tipo_muestra = models.CharField(verbose_name='Tipo de Muestra', max_length=4000, blank=True)
    patologo_resultado = models.CharField(verbose_name='Resultado', max_length=4000, blank=True)
    patologo_marcadores = models.CharField(verbose_name='Marcadores', max_length=4000, blank=True)
    patologo_observaciones = models.CharField(verbose_name='Observaciones', max_length=4000, blank=True)
    udm_observaciones = models.CharField(verbose_name='Observaciones', max_length=4000, blank=True)
    udm_tipo_muestra = models.CharField(verbose_name='Tipo de Muestra', choices=(( 'Sangre', 'Sangre' ), ( 'Tejido Fresco', 'Tejido Fresco' ), ( 'Tejido en Parafina', 'Tejido en Parafina' ), ( 'Tejido en Formaldehido', 'Tejido en Formaldehido' ), ( 'Esputo', 'Esputo' ), ( 'Lavado Gástrico', 'Lavado Gástrico' ), ( 'Heces', 'Heces' ), ( 'Orina', 'Orina' ), ( 'Líquido Cefalorraquídeo', 'Líquido Cefalorraquídeo' ), ( 'Hisopados Faringeos', 'Hisopados Faringeos' ), ( 'Mucosas', 'Mucosas' ), ( 'Otros', 'Otros' )), max_length=255, blank=True)
    udm_tipo_muestra_otro = models.CharField(verbose_name='Tipo de Muestra Otro', max_length=255, blank=True, null=True)
    udm_tecnica_deteccion = models.CharField(verbose_name='Técnica de Detección', choices=(( 'Pirosecuenciación', 'Pirosecuenciación' ), ( 'PCR Tiempo Real', 'PCR Tiempo Real' ), ( 'PCR Punto Final', 'PCR Punto Final' ), ( 'ELISA', 'ELISA' )), max_length=255, blank=True)
    paciente = models.ForeignKey('Paciente', null=True)
    creacion_usuario = models.ForeignKey(UDMUser, related_name='creacion_usuario', db_column='creacion_usuario_id', null=True)
    creacion_fecha = models.DateTimeField(verbose_name='Fecha de Creación', blank=True, null=True)
    medico_modificacion_usuario = models.ForeignKey(UDMUser, related_name='medico_modificacion_usuario', db_column='medico_modificacion_usuario_id', null=True)
    patologo_modificacion_usuario = models.ForeignKey(UDMUser, related_name='patologo_modificacion_usuario', db_column='patologo_modificacion_usuario_i', null=True)
    udm_modificacion_usuario = models.ForeignKey(UDMUser, related_name='udm_modificacion_usuario', db_column='udm_modificacion_usuario_id', null=True)
    medico_modificacion_fecha = models.DateTimeField(verbose_name='Fecha de Modificación', blank=True, null=True)
    patologo_modificacion_fecha = models.DateTimeField(verbose_name='Fecha de Modificación', blank=True, null=True)
    udm_modificacion_fecha = models.DateTimeField(verbose_name='Fecha de Modificación', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 't_udm_diagnostico'
        permissions = (( 'diagnostico_medico', 'Acceso Médico'), ( 'diagnostico_patologo', 'Acceso Patólogo' ), ( 'diagnostico_udm', 'Acceso UDM' ),)

class TipoExamen(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    tipo = models.CharField(verbose_name='Tipo', max_length=255)
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_tipo_examen'
        verbose_name = 'Tipo de Exámen'
        verbose_name_plural = 'Tipos de Exámen'
        ordering = [ 'orden' ]

class DiagnosticoTrasladoMuestra(models.Model):
    id = models.AutoField(primary_key=True)
    ruta = models.FileField(upload_to='archivos', max_length=255, blank=True, null=True)
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)
    diagnostico = models.ForeignKey(Diagnostico, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 't_udm_diagnostico_trasl_muestra'
        ordering = [ 'orden' ]

class DiagnosticoEstudio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    link = models.CharField(verbose_name='Link', max_length=255, blank=True, null=True)
    ruta = models.FileField(upload_to='archivos', max_length=255, blank=True, null=True)
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)
    diagnostico = models.ForeignKey(Diagnostico, blank=True, null=True)
    tipo_estudio = models.ForeignKey(TipoEstudio, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 't_udm_diagnostico_estudio'
        ordering = [ 'orden' ]

class DiagnosticoExamen(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Medicamento', max_length=255, blank=True, null=True)
    presente = models.BooleanField(verbose_name='Presente', default=False)
    resultado = models.NullBooleanField(verbose_name='Resultado')
    tipo = models.CharField(verbose_name='Tipo', max_length=255, blank=True, null=True)
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)
    diagnostico = models.ForeignKey(Diagnostico, blank=True, null=True)
    tipo_examen = models.ForeignKey(TipoExamen, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 't_udm_diagnostico_examen'
        ordering = [ 'orden' ]

class DiagnosticoSintoma(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    presente = models.BooleanField(verbose_name='¿Si?', default=False)
    cuantos = models.DecimalField(verbose_name='¿Cuántos?', max_digits=3, decimal_places=0, blank=True, null=True)
    personas = models.CharField(verbose_name='¿Quién?', max_length=255, blank=True, null=True)
    tipos = models.CharField(verbose_name='¿Qué tipo?', max_length=255, blank=True, null=True)
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)
    diagnostico = models.ForeignKey(Diagnostico, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 't_udm_diagnostico_sintoma'
        ordering = [ 'orden' ]

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_estado'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = [ 'nombre' ]

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_primero = models.CharField(verbose_name='Primer Nombre', max_length=255)
    nombre_segundo = models.CharField(verbose_name='Segundo Nombre', max_length=255)
    apellido_primero = models.CharField(verbose_name='Primer Apellido', max_length=255)
    apellido_segundo = models.CharField(verbose_name='Segundo Apellido', max_length=255)
    tipo_identificacion = models.CharField(verbose_name='', max_length=1, choices=(( 'V', 'V'), ( 'E', 'E' ), ( 'P', 'P')), blank=True, null=True)
    identificacion = models.CharField(verbose_name='C.I. / Pasaporte', max_length=20, blank=True, null=True, unique=True)
    partida_nacimiento = models.CharField(verbose_name='Partida de Nacimiento', max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', blank=True, null=True)
    edad_anios = models.DecimalField(verbose_name='Años', max_digits=3, decimal_places=0, blank=True, null=True)
    edad_meses = models.DecimalField(verbose_name='Meses', max_digits=3, decimal_places=0, blank=True, null=True)
    sexo = models.CharField(verbose_name='Sexo', max_length=1, choices=(( 'M', 'M' ), ( 'F', 'F' )), blank=True, null=True)
    nacionalidad = models.CharField(verbose_name='Nacionalidad', max_length=1, choices=(( 'V', 'V' ), ( 'E', 'E' )), blank=True, null=True)
    represent_nombre_primero = models.CharField(verbose_name='Primer Nombre', max_length=255, blank=True, null=True)
    represent_nombre_segundo = models.CharField(verbose_name='Segundo Nombre', max_length=255, blank=True, null=True)
    represent_apellido_primero = models.CharField(verbose_name='Primer Apellido', max_length=255, blank=True, null=True)
    represent_apellido_segundo = models.CharField(verbose_name='Segundo Apellido', max_length=255, blank=True, null=True)
    represent_tipo_identificacion = models.CharField(verbose_name='', max_length=1, choices=(( 'V', 'V' ), ( 'E', 'E' ), ( 'P', 'P')), blank=True, null=True)
    represent_identificacion = models.CharField(verbose_name='C.I. / Pasaporte', max_length=255, blank=True, null=True)
    represent_numero_hijo = models.DecimalField(verbose_name='Número de Hijos', max_digits=3, decimal_places=0, blank=True, null=True)
    represent_sexo = models.CharField(verbose_name='Sexo', max_length=1, choices=(( 'M', 'M' ), ( 'F', 'F' )), blank=True, null=True)
    represent_fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', blank=True, null=True)
    represent_nacionalidad = models.CharField(verbose_name='Nacionalidad', max_length=1, choices=(( 'V', 'V' ), ( 'E', 'E' )), blank=True, null=True)
    telefono_local = models.CharField(verbose_name='Teléfono Local', max_length=255, blank=True, null=True)
    telefono_celular1 = models.CharField(verbose_name='Teléfono Celular', max_length=255, blank=True, null=True)
    telefono_celular2 = models.CharField(verbose_name='Teléfono Móvil', max_length=255, blank=True, null=True)
    correo_electronico = models.CharField(verbose_name='Correo Electrónico', max_length=255, blank=True, null=True)
    calle_avenida = models.CharField(verbose_name='Calle / Avenida', max_length=255, blank=True, null=True)
    sector_barrio_urb = models.CharField(verbose_name='Sector / Barrio / Urbanización', max_length=255, blank=True, null=True)
    casa_edificio = models.CharField(verbose_name='Casa / Edificio', max_length=255, blank=True, null=True)
    familiares_observaciones = models.CharField(verbose_name='Observaciones', max_length=4000, blank=True, null=True)
    numero_historia = models.CharField(verbose_name='Casa / Edificio', max_length=255, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, null=True)
    parroquia = models.ForeignKey(Parroquia, null=True)
    estado_civil = models.ForeignKey(EstadoCivil, related_name='estado_civil', null=True)
    nivel_estudio = models.ForeignKey(NivelEstudio, related_name='nivel_estudio', null=True)
    represent_estado_civil = models.ForeignKey(EstadoCivil, related_name='represent_estado_civil', blank=True, null=True)
    represent_nivel_estudio = models.ForeignKey(NivelEstudio, related_name='represent_nivel_estudio', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 't_udm_paciente'

class HistoricoCambio(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(verbose_name='Fecha', blank=True, null=True)
    campo_modificado = models.CharField(verbose_name='Campo modificado', max_length=255)
    valor_anterior = models.CharField(verbose_name='Valor anterior', max_length=255)
    valor_actual = models.CharField(verbose_name='Valor actual', max_length=255)
    paciente = models.ForeignKey(Paciente, related_name='paciente', null=True)
    usuario = models.ForeignKey(UDMUser, related_name='usuario', null=True)
    class Meta:
        managed = False
        db_table = 't_udm_historico_cambio'

class TipoAntecedente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        managed = False
        db_table = 't_udm_tipo_antecedente'
        verbose_name = 'Tipo de Antecedente'
        verbose_name_plural = 'Tipos de Antecedente'
        ordering = [ 'orden' ]

class DiagnosticoAntecedente(models.Model):
    id = models.AutoField(primary_key=True)
    antecedente = models.CharField(verbose_name='Antecedente', max_length=255, blank=True, null=True)
    nexo_familiar = models.CharField(verbose_name='Nexo Familiar', max_length=255, blank=True, null=True)
    presente = models.NullBooleanField(verbose_name='Hay presente')
    otro = models.NullBooleanField(verbose_name='Es otro')
    orden = models.IntegerField(verbose_name='Órden', blank=True, null=True)
    tipo_antecedente = models.ForeignKey(TipoAntecedente, blank=True, null=True)
    paciente = models.ForeignKey(Paciente, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 't_udm_diagnostico_antecedente'
        ordering = [ 'orden' ]