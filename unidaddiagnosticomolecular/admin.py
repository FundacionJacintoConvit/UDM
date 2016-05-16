# coding: utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unidaddiagnosticomolecular.models import UDMUser, Ciudad, Estado, Institucion, Unidad, EstadoCivil, NivelEstudio, TipoEnfermedad, TipoCancer, TipoAntecedente, TipoEstudio, TipoExamen, Parroquia, Municipio
from unidaddiagnosticomolecular.forms import UDMUserCreationForm, UDMUserChangeForm, CiudadForm, EstadoForm, InstitucionForm, UnidadForm, EstadoCivilForm, NivelEstudioForm, TipoEnfermedadForm, TipoCancerForm, TipoAntecedenteForm, TipoEstudioForm, TipoExamenForm, ParroquiaForm, MunicipioForm

class ParroquiaAdmin(admin.ModelAdmin):
    form = ParroquiaForm

class MunicipioAdmin(admin.ModelAdmin):
    form = MunicipioForm

class CiudadAdmin(admin.ModelAdmin):
    form = CiudadForm
	
class EstadoAdmin(admin.ModelAdmin):
    form = EstadoForm
	
class InstitucionAdmin(admin.ModelAdmin):
    form = InstitucionForm

class UnidadAdmin(admin.ModelAdmin):
    form = UnidadForm

class EstadoCivilAdmin(admin.ModelAdmin):
    form = EstadoCivilForm

class NivelEstudioAdmin(admin.ModelAdmin):
    form = NivelEstudioForm

class TipoEnfermedadAdmin(admin.ModelAdmin):
    form = TipoEnfermedadForm

class TipoCancerAdmin(admin.ModelAdmin):
    form = TipoCancerForm

class TipoAntecedenteAdmin(admin.ModelAdmin):
    form = TipoAntecedenteForm

class TipoExamenAdmin(admin.ModelAdmin):
    form = TipoExamenForm

class TipoEstudioAdmin(admin.ModelAdmin):
    form = TipoEstudioForm

class UDMUserAdmin(UserAdmin):
    add_form = UDMUserCreationForm
    form = UDMUserChangeForm
    fieldsets = (
        ( 'Información del Usuario', { 'fields': ( 'username', 'password' ) } ), 
        ( 'Información Personal', { 'fields': ( 'first_name', 'nombre_segundo', 'last_name', 'apellido_segundo', 'nacionalidad', 'cedula_pasaporte', 'edad', 'sexo' ) } ), 
        ( 'Información Profesional', { 'fields': ( 'profesion', 'especializacion', 'especializacion_culminada', 'numero_mpps', 'numero_colegio', 'ubicacion_colegio', 'email', 'telefono' ) } ),
        ( 'Información del Convenio', { 'fields': ( 'institucion', 'unidad', 'unidad_fecha_inicio', 'unidad_fecha_fin', 'unidad_director', 'unidad_director_telefono', 'unidad_director_email' ) } ),
        ( 'Información de Permisos', { 'fields': ( 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions' ) } ), 
    )

admin.site.register(Parroquia, ParroquiaAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Estado, EstadoAdmin)
admin.site.register(Institucion, InstitucionAdmin)
admin.site.register(Unidad, UnidadAdmin)
admin.site.register(EstadoCivil, EstadoCivilAdmin)
admin.site.register(NivelEstudio, NivelEstudioAdmin)
admin.site.register(TipoEnfermedad, TipoEnfermedadAdmin)
admin.site.register(TipoCancer, TipoCancerAdmin)
admin.site.register(TipoAntecedente, TipoAntecedenteAdmin)
admin.site.register(TipoExamen, TipoExamenAdmin)
admin.site.register(TipoEstudio, TipoEstudioAdmin)
admin.site.register(UDMUser, UDMUserAdmin)